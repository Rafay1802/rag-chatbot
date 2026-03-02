import streamlit as st
from rag.scraper import scrape_url
from rag.embedder import store_embeddings
from rag.retriever import query_rag

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")
st.caption("Enter a URL and ask questions about it")

if "url_loaded" not in st.session_state:
    st.session_state.url_loaded = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "namespace" not in st.session_state:
    st.session_state.namespace = "default"

with st.sidebar:
    st.header("📄 Load a Website")
    url = st.text_input("Enter URL", placeholder="https://example.com")
    if st.button("Load URL", type="primary"):
        if url:
            with st.spinner("Scraping and storing..."):
                try:
                    chunks = scrape_url(url)
                    namespace = url.replace("https://", "").replace("/", "-")[:50]
                    store_embeddings(chunks, namespace=namespace)
                    st.session_state.url_loaded = True
                    st.session_state.namespace = namespace
                    st.session_state.messages = []
                    st.success(f"✅ Loaded {len(chunks)} chunks!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a URL")

if st.session_state.url_loaded:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask a question about the website..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = query_rag(prompt, namespace=st.session_state.namespace)
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("👈 Enter a URL in the sidebar to get started!")