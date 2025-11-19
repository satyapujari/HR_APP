"""Vector Store Factory implementation."""
from typing import Any, Dict, List, Optional
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from .base_factory import BaseFactory
from utils.config_types import VectorDBType

DEFAULT_PERSISTENT_DIR = './indexes/chroma_db'
DEFAULT_COLLECTION_NAME = 'rag_documents'

class VectorStoreFactory(BaseFactory):
    """Factory for creating vector store instances."""

    def create(
            self,
            config: Dict[str, Any],
            embedding: Embeddings,
            documents: Optional[List[Document]] = None
    ) -> Any:
        """
        Create a vector store instance based on configuration.

        Args:
            config: Vector store configuration dictionary
            embedding: Embedding model instance
            documents: Optional list of documents to add to the vector store

        Returns:
            Vector store instance

        Raises:
            ValueError: If unsupported vector store type is specified
        """
        vectorstore_type = config.get('type', '').lower()

        if vectorstore_type == VectorDBType.CHROMA:
            return self._create_chroma_vectorstore(config, embedding, documents)
        else:
            raise ValueError(f"Unsupported vector store type: {vectorstore_type}")

    def _create_chroma_vectorstore(
            self,
            config: Dict[str, Any],
            embedding: Embeddings,
            documents: Optional[List[Document]] = None
    ) -> Chroma:
        """
        Create a Chroma vector store instance.

        Args:
            config: Chroma configuration
            embedding: Embedding model instance
            documents: Optional list of documents to add

        Returns:
            Chroma instance
        """
        persist_directory = config.get('persist_directory', DEFAULT_PERSISTENT_DIR)
        collection_name = config.get('collection_name', DEFAULT_COLLECTION_NAME)

        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        if documents:
            # Create new vector store with documents
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=embedding,
                persist_directory=persist_directory,
                collection_name=collection_name
            )
        else:
            # Load existing vector store
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embedding,
                collection_name=collection_name
            )

        return vectorstore