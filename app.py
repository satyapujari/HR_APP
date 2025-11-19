import os, json, time
import streamlit as st
from ingestion import ingest_folder
from chains import QAChain
from vectordb import get_vectorstore
from config.config_loader1 import load_config
from config.factories import FactoryManager
from utils import save_query_history, load_query_history
from langchain_community.vectorstores import Chroma

st.set_page_config(page_title="RAG App (Complete)", layout="wide", initial_sidebar_state="expanded")

config = load_config()
fm = FactoryManager(config)

# Sidebar
with st.sidebar:
    st.title("RAG Config")
    db_choice = "Vector DB"
    top_k = 1
    chunk_size = 1000
    chunk_overlap = 200
    reindex = st.button("Re-index data/ (re-ingest)")
    return_sources = st.checkbox("Return source documents", value=True)
    st.subheader("Query history")
    history = load_query_history()
    for q in history[-10:][::-1]:
        st.write(q)

st.title("Retrieval-Augmented Generation (RAG) — Complete Demo")

left, right = st.columns([3,1])

with left:
    st.subheader("Ask a question")
    query = st.text_area("Your question", height=120)
    ask_btn = st.button("Ask")
    embedder = fm.get_embedder()
    if ask_btn and query.strip():
        save_query_history(query.strip())
        with st.spinner("Loading vectorstore..."):
            vs = Chroma(
                collection_name="chroma_db",
                embedding_function=embedder,
                persist_directory="indexes"  # folder on disk
            )
        chain = QAChain(vectorstore=vs, top_k=top_k, return_source_documents=return_sources)
        prepared = chain.prepare_prompt(query)
        if prepared.get('fallback'):
            st.warning("I don't have enough information in the provided documents to answer that. Try adding more documents or broadening your query.")
        else:
            prompt = prepared['prompt']
            sources = prepared['retrieved']
            with st.expander("Retrieved source snippets", expanded=False):
                for s in sources:
                    st.markdown(f"**{s.get('id')}** — (score: {s.get('score'):.4f})")
                    st.write(s.get('page_content') or s.get('metadata', {}).get('text', '[no snippet]'))
                    st.markdown('---')
            st.subheader("Answer (streaming if OPENAI_API_KEY set)")
            answer_area = st.empty()
            meta_area = st.empty()
            combined = ""
            start = time.time()
            for chunk in chain.generate_stream(prompt):
                if isinstance(chunk, dict) and chunk.get('_final'):
                    end = time.time()
                    duration = chunk.get('duration', end-start)
                    final_text = chunk.get('text', combined)
                    answer_area.markdown(final_text)
                    meta_area.markdown(f"**Model**: {chunk.get('model')}  **Duration**: {duration:.2f}s")
                    break
                else:
                    combined += str(chunk)
                    answer_area.markdown(combined + "▌")
            st.markdown("---")
            st.subheader("Sources")
            for s in sources:
                st.write(f"- {s.get('id')} (score: {s.get('score'):.4f})")
            payload = {"question": query, "answer": combined, "sources": sources}
            st.download_button("Download JSON", data=json.dumps(payload, indent=2), file_name="chat_response.json", mime="application/json")


