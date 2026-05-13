import streamlit as st

st.set_page_config(
    page_title = "RAG chatbot",
    page_icon = ":speech_balloon:",
    layout = "centered"
)

st.title("RAG Chatbot")
st.write("Upload a text document and ask questions about it.")

st.header("1. Upload a docuement")
st.info("Document upload UI will go here.")

st.header("Ask a question")
st.info("Questrion input UI will go here.")