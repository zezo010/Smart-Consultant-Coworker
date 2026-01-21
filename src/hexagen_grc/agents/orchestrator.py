"""Orchestrator agent for coordinating multi-agent execution."""

from typing import Any, Dict, List

from ..common.schemas import (
    AgentStatus,
    ClientProfile,
    DocumentType,
    Framework,
    GRCTaskRequest,
    Language,
    TaskType,
)
from .base import BaseAgent


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator agent that coordinates other agents.

    Responsibilities:
    - Classify task type
    - Determine required frameworks
    - Route to appropriate agents
    - Coordinate agent execution
    """

    def __init__(self):
        """Initialize orchestrator agent."""
        super().__init__("orchestrator")

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute orchestration logic.

        Args:
            inputs: Contains GRCTaskRequest

        Returns:
            Orchestration plan and agent sequence
        """
        request: GRCTaskRequest = inputs.get("request")

        if not request:
            raise ValueError("GRCTaskRequest is required")

        self.add_message(f"Processing task: {request.task_type}")

        # Determine agent sequence based on task type
        agent_sequence = self._determine_agent_sequence(request.task_type)
        self.add_message(f"Agent sequence: {' -> '.join(agent_sequence)}")

        # Prepare execution context
        context = {
            "client_profile": request.client_profile,
            "frameworks": request.frameworks,
            "language": request.language,
            "output_type": request.output_type,
            "parameters": request.parameters,
            "template_name": request.template_name,
        }

        return {
            "agent_sequence": agent_sequence,
            "context": context,
            "status": "ready"
        }

    def _determine_agent_sequence(self, task_type: TaskType) -> List[str]:
        """
        Determine the sequence of agents to execute.

        Args:
            task_type: Type of GRC task

        Returns:
            List of agent names in execution order
        """
        sequences = {
            TaskType.POLICY: [
                "knowledge",
                "policy",
                "document",
                "qa"
            ],
            TaskType.PROCEDURE: [
                "knowledge",
                "procedure",
                "document",
                "qa"
            ],
            TaskType.STANDARD: [
                "knowledge",
                "policy",  # Reuse policy agent for standards
                "document",
                "qa"
            ],
            TaskType.GAP_ANALYSIS: [
                "knowledge",
                "gap",
                "document",
                "qa"
            ],
            TaskType.RISK_ASSESSMENT: [
                "knowledge",
                "risk",
                "document",
                "qa"
            ],
            TaskType.EVIDENCE_REQUEST: [
                "knowledge",
                "evidence",
                "document"
            ],
            TaskType.STRATEGY_PACK: [
                "knowledge",
                "strategy",
                "document",
                "qa"
            ],
            TaskType.COMPLIANCE_CHECK: [
                "knowledge",
                "qa"
            ]
        }

        return sequences.get(task_type, ["knowledge", "document"])

    def validate_request(self, request: GRCTaskRequest) -> bool:
        """
        Validate GRC task request.

        Args:
            request: GRC task request

        Returns:
            True if valid, raises ValueError otherwise
        """
        if not request.client_profile:
            raise ValueError("Client profile is required")

        if not request.frameworks:
            raise ValueError("At least one framework is required")

        if request.language not in [Language.ARABIC, Language.ENGLISH]:
            raise ValueError("Invalid language")

        return True
