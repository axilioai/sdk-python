"""Workflows resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..types import NodeVariableInfo, WorkflowExecuteResponse, WorkflowVariablesResponse

if TYPE_CHECKING:
    from .._http import HTTPClient


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
        variables: dict[str, Any] | None = None,
        schedule_time: str | None = None,
    ) -> WorkflowExecuteResponse:
        """
        Execute a workflow run.

        Args:
            workflow_id: The ID of the workflow to execute.
            variables: Optional dict mapping node_id to variable value.
                       For nodes requiring input, provide the value as a string.
            schedule_time: Optional ISO datetime string for scheduled execution.
                          If not provided, runs immediately.

        Returns:
            WorkflowExecuteResponse containing the created run IDs.

        Example:
            >>> # Run immediately with variables
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     variables={"node_xyz": "my_username", "node_abc": "my_password"}
            ... )
            >>> print(f"Created run: {result.run_ids[0]}")

            >>> # Schedule for later
            >>> result = client.workflows.execute(
            ...     workflow_id="abc123",
            ...     variables={"node_xyz": "value"},
            ...     schedule_time="2024-01-15T10:00:00"
            ... )
        """
        # Build variable config for each node
        variable_configs: dict[str, dict[str, Any]] = {}
        if variables:
            for node_id, value in variables.items():
                variable_configs[node_id] = {
                    "value": str(value),
                    "type": self._detect_variable_type(value),
                    "nodeId": node_id,
                    "request_at_runtime": False,
                }

        # Build request body
        is_scheduled = schedule_time is not None
        request_body = {
            "numberOfRuns": 1,
            "runTime": {
                "isImmediate": not is_scheduled,
                "isScheduled": is_scheduled,
                "scheduleTime": schedule_time,
            },
            "runs": [{"variables": [variable_configs] if variable_configs else [{}]}],
        }

        response = self._http.post(f"/api/v1/runs/{workflow_id}", json=request_body)
        return WorkflowExecuteResponse(run_ids=response["run_ids"])

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
