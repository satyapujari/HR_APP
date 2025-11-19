"""Retriever component."""
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore


class Retriever:
    """Handles document retrieval from vector store."""

    def __init__(self, vectorstore: VectorStore, config: Dict[str, Any]):
        """
        Initialize the retriever.

        Args:
            vectorstore: Vector store instance
            config: Retrieval configuration
        """
        self.vectorstore = vectorstore
        self.top_k = config.get('top_k', 4)
        self.search_type = config.get('search_type', 'similarity')

        self.retriever = self.vectorstore.as_retriever(
            search_type=self.search_type,
            search_kwargs={'k': self.top_k}
        )

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Query string

        Returns:
            List of relevant Document objects
        """
        documents = self.retriever.invoke(query)
        return documents