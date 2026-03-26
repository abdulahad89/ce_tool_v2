import streamlit as st
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="Marketing RAG Agent")

st.title("📊 Campaign Intelligence RAG Agent")

rag = RAGPipeline()

llm_choice = st.selectbox(
    "Choose LLM",
    ["openai", "gemini", "deepseek"]
)

query = st.text_input("Ask a question about campaigns")

if st.button("Run Analysis"):
    if query:
        with st.spinner("Analyzing..."):
            response = rag.generate_response(query, llm=llm_choice)

        st.subheader("📈 Insights")
        st.write(response)
