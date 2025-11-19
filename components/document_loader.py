"""Document loader component."""
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


class DocumentLoader:
    """Handles loading documents from various sources."""

    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """
        Load documents from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of Document objects

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a PDF
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() != '.pdf':
            raise ValueError(f"File must be a PDF: {file_path}")

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        return documents

    @staticmethod
    def load_directory(directory_path: str) -> List[Document]:
        """
        Load all PDF documents from a directory.

        Args:
            directory_path: Path to the directory

        Returns:
            List of Document objects

        Raises:
            FileNotFoundError: If the directory doesn't exist
        """
        path = Path(directory_path)

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        if not path.is_dir():
            raise ValueError(f"Path must be a directory: {directory_path}")

        documents = []
        loader = DirectoryLoader(
            path=path,
            glob='*.pdf',
            loader_cls=PyPDFLoader
        )
        documents = loader.lazy_load()

        #pdf_files = list(path.glob('*.pdf'))

        # for pdf_file in pdf_files:
        #     try:
        #         docs = DocumentLoader.load_pdf(str(pdf_file))
        #         documents.extend(docs)
        #     except Exception as e:
        #         print(f"Warning: Failed to load {pdf_file}: {e}")

        return documents