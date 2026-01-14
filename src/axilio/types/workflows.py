"""Workflow type definitions."""

from __future__ import annotations

from pydantic import BaseModel


class NodeVariableInfo(BaseModel):
    """Information about a node that requires variable input at runtime."""

    node_id: str
    label: str
    order: int
    variable_name: str | None = None


class WorkflowVariablesResponse(BaseModel):
    """Response containing all nodes that require variable input."""

    workflow_id: str
    variables: dict[str, NodeVariableInfo]


class WorkflowExecuteResponse(BaseModel):
    """Response from executing a workflow."""

    run_ids: list[str]

