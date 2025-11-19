"""Text splitting component."""
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:
    """Handles splitting documents into chunks."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the text splitter.

        Args:
            config: Document processing configuration
        """
        self.chunk_size = config.get('chunk_size', 1000)
        self.chunk_overlap = config.get('chunk_overlap', 200)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.

        Args:
            documents: List of Document objects to split

        Returns:
            List of split Document objects
        """
        if not documents:
            return []

        split_docs = self.splitter.split_documents(documents)
        return split_docs