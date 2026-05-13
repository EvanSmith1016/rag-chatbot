import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title = "RAG chatbot",
    page_icon = ":speech_balloon:",
    layout = "centered"
)

if "document_id" not in st.session_state:
    st.session_state["document_id"] = None

if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = None

st.title("Rag Chatbot")
st.write("Upload a text document and ask questions about it.")

st.header("1. Upload a document")

uploaded_file = st.file_uploader(
    "choose a .txt file",
    type = ["txt"],
)

if uploaded_file is not None:
    if st.button("Upload Document"):
        try:
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")
            }

            response = requests.post(
                f"{BACKEND_URL}/documents/upload",
                files = files,
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["document_id"] = data["document_id"]
                st.session_state["uploaded_filename"] = uploaded_file.name

                st.success(
                    f"Uploaded '{uploaded_file.name}' successfully. "
                    f"Document ID: {data['document_id']}, "
                    f"Chunks: {data['num_chunks']}"
                )
            else:
                st.error(f"Upload failed: {response.text}")
        except requests.exceptions.RequestException:
            st.error("Could not connect to the backend. Make sure FastAPI is running.")
if st.session_state["document_id"] is not None:
    st.info(
        f"Current document: {st.session_state['uploaded_filename']}"
        f"(ID: {st.session_state['document_id']})"
    )

st.header("2. Ask a question")

if st.session_state["document_id"] is None:
    st.warning("Upload a document before asking questions.")
else:
    question = st.text_input("Enter your question")

    if st.button("Ask Question"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                payload = {
                    "document_id": st.session_state["document_id"],
                    "question": question,
                }

                with st.spinner("Generating answer..."):
                    response = requests.post(
                        f"{BACKEND_URL}/chat/",
                        json=payload,
                    )

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("Answer")
                    st.write(data["answer"])

                    with st.expander("Retrieved Chunks"):
                        for chunk in data["retrieved_chunks"]:
                            st.write(chunk)

                else:
                    st.error(f"Chat request failed: {response.text}")

            except requests.exceptions.RequestException:
                st.error("Could not connect to the backend.")
