"""Embedding Factory implementation."""
from typing import Any, Dict
from langchain_openai import OpenAIEmbeddings
from .base_factory import BaseFactory
from utils.config_types import EmbeddingModelType

DEFAULT_MODEL_NAME = 'text-embedding-3-small'

class EmbeddingFactory(BaseFactory):
    """Factory for creating embedding model instances."""

    def create(self, config: Dict[str, Any]) -> Any:
        """
        Create an embedding model instance based on configuration.

        Args:
            config: Embedding configuration dictionary

        Returns:
            Embedding model instance

        Raises:
            ValueError: If unsupported embedding type is specified
        """
        embedding_type = config.get('type', '').lower()

        if embedding_type == EmbeddingModelType.OPENAI:
            return self._create_openai_embedding(config)
        else:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")

    def _create_openai_embedding(self, config: Dict[str, Any]) -> OpenAIEmbeddings:
        """
        Create an OpenAI embedding instance.

        Args:
            config: OpenAI embedding configuration

        Returns:
            OpenAIEmbeddings instance
        """
        return OpenAIEmbeddings(
            model=config.get('model_name', DEFAULT_MODEL_NAME)
        )