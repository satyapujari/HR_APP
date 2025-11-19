import os, json, time
import streamlit as st
from rag.rag_pipeline import RAGPipeline
from dotenv import load_dotenv

st.set_page_config(page_title="RAG App (Complete)", layout="wide", initial_sidebar_state="expanded")

load_dotenv()

# Sidebar
with st.sidebar:
    st.title("RAG Config")

    reindex = st.button("Re-index data/ (re-ingest)")
    return_sources = st.checkbox("Return source documents", value=True)
    st.subheader("Query history")
    #history = load_query_history()
    # for q in history[-10:][::-1]:
    #     st.write(q)

st.title("TECHNOSPHERE INDIA PRIVATE LIMITED - HR APP")

left, right = st.columns([3,1])

with left:
    st.subheader("Ask a question")
    query = st.text_area("Your question", height=120)
    ask_btn = st.button("Ask")

    if ask_btn and query.strip():
        pipeline = RAGPipeline()
        #save_query_history(query.strip())
        with st.spinner("Loading vectorstore..."):
            # Load existing vector store
            pipeline.load_vectorstore()

        result = pipeline.query(query)
        answer_area = st.empty()
        meta_area = st.empty()
        combined = ""
        answer_area.markdown(result['answer'])

        st.download_button("Download JSON", data=json.dumps(result['answer'], indent=2), file_name="chat_response.json", mime="application/json")


