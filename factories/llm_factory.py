"""LLM Factory implementation."""
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from .base_factory import BaseFactory
from utils.config_types import LLMType

DEFAULT_MODEL_NAME = 'gpt-4o-mini'
DEFAULT_MODEL_TEMPERATURE = 0.7
DEFAULT_MODEL_TOKEN_SIZE = 500

class LLMFactory(BaseFactory):
    """Factory for creating LLM instances."""

    def create(self, config: Dict[str, Any]) -> Any:
        """
        Create an LLM instance based on configuration.

        Args:
            config: LLM configuration dictionary

        Returns:
            LLM instance

        Raises:
            ValueError: If unsupported LLM type is specified
        """
        llm_type = config.get('type', '').lower()

        if llm_type == LLMType.OPENAI:
            return self._create_openai_llm(config)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    def _create_openai_llm(self, config: Dict[str, Any]) -> ChatOpenAI:
        """
        Create an OpenAI LLM instance.

        Args:
            config: OpenAI configuration

        Returns:
            ChatOpenAI instance
        """
        return ChatOpenAI(
            model = config.get('model_name', DEFAULT_MODEL_NAME),
            temperature = config.get('temperature', DEFAULT_MODEL_TEMPERATURE),
            max_tokens = config.get('max_tokens', DEFAULT_MODEL_TOKEN_SIZE)
        )