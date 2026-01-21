"""Base agent class for HexaGen GRC agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..common.config import settings
from ..common.logging import get_logger
from ..common.schemas import AgentMessage, AgentStatus


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str):
        """
        Initialize base agent.

        Args:
            name: Agent name
        """
        self.name = name
        self.logger = get_logger(f"agents.{name}")
        self.status = AgentStatus.PENDING
        self.messages: List[AgentMessage] = []
        self.context: Dict[str, Any] = {}

    def add_message(self, message: str, level: str = "info") -> None:
        """
        Add a message to the agent's message log.

        Args:
            message: Message text
            level: Message level (info, warning, error)
        """
        self.messages.append(
            AgentMessage(agent=self.name, message=message, level=level)
        )
        self.logger.log(
            getattr(self.logger, level.upper(), self.logger.info),
            message
        )

    def set_context(self, context: Dict[str, Any]) -> None:
        """
        Set agent context.

        Args:
            context: Context dictionary
        """
        self.context = context

    def update_context(self, updates: Dict[str, Any]) -> None:
        """
        Update agent context.

        Args:
            updates: Dictionary of updates
        """
        self.context.update(updates)

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.

        Args:
            inputs: Input parameters

        Returns:
            Agent execution results
        """
        pass

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent with error handling.

        Args:
            inputs: Input parameters

        Returns:
            Agent execution results
        """
        self.status = AgentStatus.RUNNING
        self.add_message(f"Starting {self.name}")

        try:
            results = await self.execute(inputs)
            self.status = AgentStatus.COMPLETED
            self.add_message(f"Completed {self.name}")
            return results

        except Exception as e:
            self.status = AgentStatus.FAILED
            self.add_message(f"Failed: {str(e)}", level="error")
            raise


class LLMAgent(BaseAgent):
    """Base class for agents that use LLM."""

    def __init__(self, name: str):
        """
        Initialize LLM agent.

        Args:
            name: Agent name
        """
        super().__init__(name)
        self.ollama_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.temperature = settings.agent_temperature
        self.max_tokens = settings.agent_max_tokens

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            Generated text
        """
        try:
            import httpx

            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature or self.temperature,
                        "num_predict": max_tokens or self.max_tokens,
                    }
                }

                if system_prompt:
                    payload["system"] = system_prompt

                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")

        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            raise

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate chat completion using LLM.

        Args:
            messages: List of chat messages
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            Generated response
        """
        try:
            import httpx

            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature or self.temperature,
                        "num_predict": max_tokens or self.max_tokens,
                    }
                }

                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result.get("message", {}).get("content", "")

        except Exception as e:
            self.logger.error(f"Error generating chat: {e}")
            raise
