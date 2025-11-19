"""RAG Pipeline implementation."""
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from factories import LLMFactory, EmbeddingFactory, VectorStoreFactory
from components import DocumentLoader, TextSplitter, Retriever
from utils import ConfigLoader


class RAGPipeline:
    """Main RAG pipeline for document indexing and querying."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the RAG pipeline.

        Args:
            config_path: Path to configuration file
        """
        self.config_loader = ConfigLoader(config_path)
        self.config_loader.load_config()

        # Initialize factories
        self.llm_factory = LLMFactory()
        self.embedding_factory = EmbeddingFactory()
        self.vectorstore_factory = VectorStoreFactory()

        # Create instances from configuration
        self.llm = self.llm_factory.create(self.config_loader.get_llm_config())
        self.embedding = self.embedding_factory.create(self.config_loader.get_embedding_config())

        # Text splitter
        self.text_splitter = TextSplitter(self.config_loader.get_document_processing_config())

        # Vector store and retriever (initialized when needed)
        self.vectorstore = None
        self.retriever = None

        # RAG chain
        self.rag_chain = None

    def index_documents(self, file_path: str) -> None:
        """
        Index documents from a PDF file or directory.

        Args:
            file_path: Path to PDF file or directory containing PDFs
        """
        print(f"Loading documents from: {file_path}")

        # Load documents
        from pathlib import Path
        path = Path(file_path)

        if path.is_file():
            documents = DocumentLoader.load_pdf(file_path)
        elif path.is_dir():
            print(f"Loading PDF from directory: {file_path}")
            documents = DocumentLoader.load_directory(file_path)
        else:
            raise ValueError(f"Invalid path: {file_path}")

        #print(f"Loaded {len(documents)} document(s)")

        # Split documents
        print("Splitting documents into chunks...")
        split_docs = self.text_splitter.split_documents(documents)
        print(f"Created {len(split_docs)} chunks")

        # Create vector store
        print("Creating vector store and indexing documents...")
        self.vectorstore = self.vectorstore_factory.create(
            self.config_loader.get_vectorstore_config(),
            self.embedding,
            split_docs
        )

        print("Indexing complete!")

    def load_vectorstore(self) -> None:
        """Load existing vector store from disk."""
        print("Loading existing vector store...")
        self.vectorstore = self.vectorstore_factory.create(
            self.config_loader.get_vectorstore_config(),
            self.embedding
        )
        print("Vector store loaded!")

    def _initialize_rag_chain(self) -> None:
        """Initialize the RAG chain with retriever and LLM."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call index_documents() or load_vectorstore() first.")

        # Create retriever
        self.retriever = Retriever(
            self.vectorstore,
            self.config_loader.get_retrieval_config()
        )

        # Create RAG prompt template
        template = """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""

        prompt = ChatPromptTemplate.from_template(template)
        # print(prompt)

        # Create RAG chain
        def format_docs(docs: List[Document]) -> str:
            #print(f"Context: {docs}")
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
                {
                    "context": lambda x: format_docs(self.retriever.retrieve(x["question"])),
                    "question": lambda x: x["question"]
                }
                | prompt
                | self.llm
                | StrOutputParser()
        )

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system.

        Args:
            question: Question to ask

        Returns:
            Dictionary containing answer and source documents
        """
        if self.rag_chain is None:
            self._initialize_rag_chain()

        # Retrieve relevant documents
        relevant_docs = self.retriever.retrieve(question)

        # Generate answer
        answer = self.rag_chain.invoke({"question": question})

        return {
            "question": question,
            "answer": answer,
            "source_documents": relevant_docs
        }