"""Enhanced Streamlit UI for RAG Application with custom components."""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import tempfile
from datetime import datetime

from rag.rag_pipeline import RAGPipeline
from ui_components import (
    metric_card, info_card, document_card, chat_message,
    source_document_card, status_badge, feature_card
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        padding: 0rem 1rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .upload-section {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }

    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }

    h2 {
        color: #1e3a8a;
        font-weight: 700;
    }

    h3 {
        color: #334155;
        font-weight: 600;
    }

    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = None
    if 'vectorstore_loaded' not in st.session_state:
        st.session_state.vectorstore_loaded = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'indexed_files' not in st.session_state:
        st.session_state.indexed_files = []
    if 'show_sources' not in st.session_state:
        st.session_state.show_sources = True
    if 'total_queries' not in st.session_state:
        st.session_state.total_queries = 0


def load_pipeline():
    """Load or initialize the RAG pipeline."""
    if st.session_state.pipeline is None:
        try:
            st.session_state.pipeline = RAGPipeline()
            return True
        except Exception as e:
            st.error(f"Failed to initialize pipeline: {e}")
            return False
    return True


def sidebar():
    """Render the enhanced sidebar."""
    with st.sidebar:
        # Logo/Header
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">📚</div>
            <div style="font-size: 1.5rem; font-weight: 700; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;">
                RAG Assistant
            </div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
                Powered by AI
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick Stats
        st.subheader("📊 Quick Stats")

        col1, col2 = st.columns(2)
        with col1:
            metric_card("Files", str(len(st.session_state.indexed_files)), "📄", "#667eea")
        with col2:
            metric_card("Queries", str(st.session_state.total_queries), "💬", "#764ba2")

        st.markdown("<br>", unsafe_allow_html=True)

        # Status
        if st.session_state.vectorstore_loaded:
            status_badge("success", "Vector Store Active")
        else:
            status_badge("warning", "No Vector Store")

        st.markdown("---")

        # Configuration
        with st.expander("⚙️ Configuration", expanded=False):
            config_file = st.text_input(
                "Config Path",
                value="config/config.yaml",
                key="config_path"
            )

            if st.button("🔄 Reload Config", use_container_width=True):
                st.session_state.pipeline = None
                st.session_state.vectorstore_loaded = False
                if load_pipeline():
                    st.success("✅ Reloaded!")
                    st.rerun()

        # Options
        with st.expander("🎛️ Display Options", expanded=True):
            st.session_state.show_sources = st.checkbox(
                "Show Source Documents",
                value=st.session_state.show_sources
            )

            theme = st.selectbox(
                "Theme Accent",
                ["Purple (Default)", "Blue", "Green", "Red"],
                index=0
            )

        # Actions
        st.markdown("---")
        st.subheader("🔧 Actions")

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("📂 Load Vector Store", use_container_width=True):
            if load_pipeline():
                try:
                    st.session_state.pipeline.load_vectorstore()
                    st.session_state.vectorstore_loaded = True
                    st.success("✅ Loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        st.markdown("---")

        # Info
        with st.expander("ℹ️ About & Help"):
            st.markdown("""
            **RAG Document Assistant v2.0**

            A powerful tool for:
            - 📥 Indexing PDF documents
            - 💬 Natural language queries
            - 🔍 Source-based answers

            **Quick Start:**
            1. Upload PDFs in Index tab
            2. Click "Index Documents"
            3. Ask questions in Chat tab

            **Tech Stack:**
            - LangChain 0.3
            - OpenAI GPT-4
            - ChromaDB
            - Streamlit
            """)

        # Footer
        st.markdown("---")
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.markdown("🔑 <span style='color: #4CAF50;'>API Connected</span>", unsafe_allow_html=True)
        else:
            st.markdown("🔑 <span style='color: #F44336;'>API Missing</span>", unsafe_allow_html=True)


def home_tab():
    """Render the home/welcome tab."""
    st.header("🏠 Welcome to RAG Document Assistant")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 2rem; border-radius: 12px; margin: 1rem 0;">
        <h3 style="margin-top: 0;">Get Started with AI-Powered Document Q&A</h3>
        <p style="font-size: 1.1rem; color: #555; line-height: 1.8;">
            Transform your PDF documents into an intelligent knowledge base. 
            Upload documents, ask questions, and get accurate answers with source references.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "📥",
            "Easy Upload",
            "Drag and drop PDF files or select from your computer. Support for multiple files."
        )

    with col2:
        feature_card(
            "🔍",
            "Smart Search",
            "Advanced vector search finds the most relevant information from your documents."
        )

    with col3:
        feature_card(
            "💬",
            "Natural Chat",
            "Ask questions in plain English and get detailed, contextual answers."
        )

    st.markdown("---")

    # Quick Stats Overview
    st.markdown("### 📈 Your Activity")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2.5rem; color: #667eea;">📄</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e3a8a;">
                {len(st.session_state.indexed_files)}
            </div>
            <div style="color: #666;">Indexed Files</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2.5rem; color: #764ba2;">💬</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e3a8a;">
                {st.session_state.total_queries}
            </div>
            <div style="color: #666;">Total Queries</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2.5rem; color: #4CAF50;">💾</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e3a8a;">
                {"Active" if st.session_state.vectorstore_loaded else "Inactive"}
            </div>
            <div style="color: #666;">Vector Store</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2.5rem; color: #FF9800;">🔥</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e3a8a;">
                {len(st.session_state.chat_history) // 2}
            </div>
            <div style="color: #666;">Conversations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Getting Started
    st.markdown("### 🚀 Quick Start Guide")

    info_card(
        "Step 1: Index Documents",
        "Go to the 'Index Documents' tab and upload your PDF files. The system will process and store them.",
        "1️⃣",
        "#667eea"
    )

    info_card(
        "Step 2: Ask Questions",
        "Switch to the 'Chat' tab and start asking questions about your documents.",
        "2️⃣",
        "#764ba2"
    )

    info_card(
        "Step 3: Review Sources",
        "Check the source documents to verify the information and dive deeper into the content.",
        "3️⃣",
        "#4CAF50"
    )


def index_tab():
    """Render the enhanced index tab."""
    st.header("📥 Document Indexing")

    info_card(
        "How It Works",
        "Upload PDF documents to create a searchable knowledge base. Documents are split into chunks and stored with embeddings for efficient retrieval.",
        "💡",
        "#2196F3"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # File uploader with custom styling
    uploaded_files = st.file_uploader(
        "📤 Choose PDF files to upload",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files (Max 200MB per file)",
        label_visibility="visible"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")

    st.markdown("<br>", unsafe_allow_html=True)

    # Action buttons
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("🚀 Index Documents", type="primary", disabled=not uploaded_files, use_container_width=True):
            if not load_pipeline():
                st.error("Failed to load pipeline")
                return

            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                indexed_count = 0
                total_files = len(uploaded_files)

                for idx, uploaded_file in enumerate(uploaded_files):
                    status_text.markdown(f"**Processing:** {uploaded_file.name}")

                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_file_path = tmp_file.name

                    try:
                        st.session_state.pipeline.index_documents(tmp_file_path)
                        st.session_state.indexed_files.append({
                            'name': uploaded_file.name,
                            'size': uploaded_file.size,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.session_state.vectorstore_loaded = True
                        indexed_count += 1
                    finally:
                        os.unlink(tmp_file_path)

                    progress_bar.progress((idx + 1) / total_files)

                status_text.empty()
                progress_bar.empty()

                st.success(f"🎉 Successfully indexed {indexed_count} document(s)!")
                st.balloons()
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error during indexing: {e}")

    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Display indexed documents
    if st.session_state.indexed_files:
        st.markdown("---")
        st.subheader("📚 Indexed Document Library")

        st.markdown(f"**Total Documents:** {len(st.session_state.indexed_files)}")

        for file_info in reversed(st.session_state.indexed_files[-10:]):  # Show last 10
            document_card(
                file_info['name'],
                file_info['size'],
                file_info['date']
            )
    else:
        st.markdown("---")
        info_card(
            "No Documents Yet",
            "Upload and index your first PDF document to get started with intelligent document search.",
            "📭",
            "#FF9800"
        )


def query_tab():
    """Render the enhanced query tab."""
    st.header("💬 Ask Questions")

    if not st.session_state.vectorstore_loaded:
        info_card(
            "Vector Store Not Loaded",
            "Please index documents first or load an existing vector store from the sidebar.",
            "⚠️",
            "#FF9800"
        )
        return

    # Chat history
    for message in st.session_state.chat_history:
        chat_message(message['role'], message['content'])

        if message['role'] == 'assistant' and st.session_state.show_sources and 'sources' in message:
            with st.expander(f"📄 View {len(message['sources'])} Source Document(s)", expanded=False):
                for idx, doc in enumerate(message['sources'], 1):
                    source = doc.metadata.get('source', 'Unknown')
                    page = doc.metadata.get('page', 'N/A')
                    source_document_card(source, page, doc.page_content)

    # Input section
    st.markdown("---")

    with st.form(key="query_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            query = st.text_input(
                "Your Question",
                placeholder="What would you like to know about your documents?",
                label_visibility="collapsed"
            )

        with col2:
            submit = st.form_submit_button("🔍 Ask", use_container_width=True)

    if submit and query:
        if not load_pipeline():
            st.error("Failed to load pipeline")
            return

        st.session_state.chat_history.append({
            'role': 'user',
            'content': query
        })

        with st.spinner("🤔 Analyzing documents..."):
            try:
                result = st.session_state.pipeline.query(query)

                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': result['answer'],
                    'sources': result['source_documents']
                })

                st.session_state.total_queries += 1
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Sample questions
    if not st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 💡 Try These Sample Questions")

        samples = [
            "What are the main topics discussed?",
            "Summarize the key findings",
            "What methodology was used?",
            "What are the conclusions?"
        ]

        cols = st.columns(2)
        for idx, question in enumerate(samples):
            with cols[idx % 2]:
                if st.button(f"💭 {question}", use_container_width=True, key=f"sample_{idx}"):
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': question
                    })
                    st.rerun()


def main():
    """Main application."""
    initialize_session_state()

    # Sidebar
    sidebar()

    # Header
    st.title("📚 RAG Document Assistant")
    st.markdown("*Intelligent Document Q&A powered by LangChain & OpenAI*")

    # API Key check
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        st.stop()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "💬 Chat", "📥 Index"])

    with tab1:
        home_tab()

    with tab2:
        query_tab()

    with tab3:
        index_tab()


if __name__ == "__main__":
    main()