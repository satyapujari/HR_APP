"""Configuration loader utility."""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages configuration from YAML file."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the configuration loader.

        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self._config = None

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Dictionary containing configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)

        return self._config

    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the loaded configuration.

        Returns:
            Configuration dictionary
        """
        if self._config is None:
            self.load_config()
        return self._config

    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return self.config.get('llm', {})

    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding configuration."""
        return self.config.get('embedding', {})

    def get_vectorstore_config(self) -> Dict[str, Any]:
        """Get vector store configuration."""
        return self.config.get('vectorstore', {})

    def get_document_processing_config(self) -> Dict[str, Any]:
        """Get document processing configuration."""
        return self.config.get('document_processing', {})

    def get_retrieval_config(self) -> Dict[str, Any]:
        """Get retrieval configuration."""
        return self.config.get('retrieval', {})