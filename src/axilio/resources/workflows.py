"""Workflows resource."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Literal

from ..types.runs import Run, RunConfig, RunStatus
from ..types.workflows import (
    NodeVariableInfo,
    WorkflowExecuteResponse,
    WorkflowVariablesResponse,
)

if TYPE_CHECKING:
    from .._http import HTTPClient

# Terminal run statuses that indicate the run has finished
_TERMINAL_STATUSES = {RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELLED}


class Workflows:
    """Workflows API resource."""

    def __init__(self, http: HTTPClient):
        self._http = http

    def get_variables(self, *, workflow_id: str) -> WorkflowVariablesResponse:
        """
        Get all nodes that require variable input at runtime for a workflow.

        Args:
            workflow_id: The ID of the workflow.

        Returns:
            WorkflowVariablesResponse containing a mapping of node_id to variable info.

        Example:
            >>> variables = client.workflows.get_variables(workflow_id="abc123")
            >>> for node_id, info in variables.variables.items():
            ...     print(f"{info.label}: {info.variable_name}")
        """
        response = self._http.get(f"/api/v1/workflows/{workflow_id}/variables")
        # Convert nested dicts to NodeVariableInfo objects
        variables = {
            node_id: NodeVariableInfo(**var_data)
            for node_id, var_data in response.get("variables", {}).items()
        }
        return WorkflowVariablesResponse(
            workflow_id=response["workflow_id"],
            variables=variables,
        )

    def execute(
        self,
        *,
        workflow_id: str,
        runs: list[RunConfig],
        schedule_time: str | None = None,
    ) -> WorkflowExecuteResponse:
        """
        Execute workflow runs.

        Args:
            workflow_id: The ID of the workflow to execute.
            runs: List of RunConfig objects, each containing variables for one run.
            schedule_time: Optional ISO datetime string for scheduled execution.
                          If not provided, runs immediately.

        Returns:
            WorkflowExecuteResponse containing the created run IDs.

        Example:
            >>> # Single run with variables
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     runs=[RunConfig(variables=[{"node_xyz": "my_value"}])]
            ... )
            >>> print(f"Created run: {result.run_ids[0]}")

            >>> # Multiple runs with different variables
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     runs=[
            ...         RunConfig(variables=[{"node_xyz": "value1"}]),
            ...         RunConfig(variables=[{"node_xyz": "value2"}]),
            ...     ]
            ... )

            >>> # Schedule for later
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     runs=[RunConfig(variables=[{"node_xyz": "value"}])],
            ...     schedule_time="2024-01-15T10:00:00"
            ... )
        """
        is_scheduled = schedule_time is not None
        request_body = {
            "numberOfRuns": len(runs),
            "runTime": {
                "isImmediate": not is_scheduled,
                "isScheduled": is_scheduled,
                "scheduleTime": schedule_time,
            },
            "runs": [run.model_dump() for run in runs],
        }

        response = self._http.post(f"/api/v1/runs/{workflow_id}", json=request_body)
        return WorkflowExecuteResponse(run_ids=response["run_ids"])

    def get_run(self, *, run_id: str) -> Run:
        """
        Get a run by ID.

        Args:
            run_id: The ID of the run.

        Returns:
            Run object with current status and details.

        Example:
            >>> run = client.workflows.get_run(run_id="run_abc123")
            >>> print(f"Status: {run.status}")
        """
        response = self._http.get(f"/api/v1/runs/user/{run_id}")
        return Run(**response)

    def wait(
        self,
        *,
        run_id: str,
        poll_interval: float = 2.0,
        timeout: float | None = None,
    ) -> Run:
        """
        Wait for a run to complete by polling its status.

        Polls the run status until it reaches a terminal state
        (COMPLETED, FAILED, or CANCELLED).

        Args:
            run_id: The ID of the run to wait for.
            poll_interval: Seconds between status checks (default: 2.0).
            timeout: Maximum seconds to wait before raising TimeoutError.
                    If None, waits indefinitely.

        Returns:
            Run object with final status and details.

        Raises:
            TimeoutError: If timeout is reached before run completes.

        Example:
            >>> # Execute and wait for completion
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     runs=[RunConfig(variables=[{"node_id": "value"}])]
            ... )
            >>> run = client.workflows.wait(run_id=result.run_ids[0])
            >>> if run.status == RunStatus.COMPLETED:
            ...     print("Workflow completed successfully!")
            ... else:
            ...     print(f"Workflow {run.status}: {run.error_message}")

            >>> # With timeout
            >>> try:
            ...     run = client.workflows.wait(run_id="run_xyz", timeout=60.0)
            ... except TimeoutError:
            ...     print("Run did not complete within 60 seconds")
        """
        start_time = time.monotonic()

        while True:
            run = self.get_run(run_id=run_id)

            if run.status in _TERMINAL_STATUSES:
                return run

            # Check timeout
            if timeout is not None:
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(
                        f"Run {run_id} did not complete within {timeout} seconds. "
                        f"Current status: {run.status}"
                    )

            time.sleep(poll_interval)

    def _detect_variable_type(
        self, value: Any
    ) -> Literal["string", "number", "boolean", "array", "object"]:
        """Detect the type of a variable value."""
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "object"
        return "string"
