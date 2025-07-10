import streamlit as st

##from utils.file_loader import get_user_text
from rag.embeddings import init_vector_store
from rag.retriever import retrieve_context
from rag.chat import correct_text
from ui.sidebar import render_sidebar
from ui.chat_window import render_chat_window
from ui.dashboard import render_dashboard

def main():
    # renderiza a sidebar e captura input
    user_text, submit = render_sidebar()

    # inicializa rubrica + índice FAISS (cacheado)
    df_rubric, index = init_vector_store()

    # ao submeter, processa correção
    if submit and user_text.strip():
        context = retrieve_context(user_text)
        corrected = correct_text(user_text, context)
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append((user_text, corrected))

    # exibe chat e dashboard
    chat_history = st.session_state.get('chat_history', [])
    render_chat_window(chat_history)
    render_dashboard(chat_history)

if __name__ == '__main__':
    main()
