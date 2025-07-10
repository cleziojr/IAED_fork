import os, sys

# garante que a raiz do projeto esteja no PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

from utils.file_loader     import get_user_text
from rag.embeddings        import init_vector_store
from rag.retriever         import retrieve_context
from rag.chat              import correct_text
from ui.sidebar            import render_sidebar
from ui.chat_window        import render_chat_window
from ui.dashboard          import render_dashboard

def main():
    # entrada de texto / upload
    user_text, submit = render_sidebar()

    # inicializa FAISS + rubrica (cacheado)
    df_rubric, index = init_vector_store()

    # ao enviar, corrige a redação
    if submit and user_text.strip():
        context   = retrieve_context(user_text)
        corrected = correct_text(user_text, context)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append((user_text, corrected))

    # exibe chat e métricas
    chat_history = st.session_state.get("chat_history", [])
    render_chat_window(chat_history)
    render_dashboard(chat_history)

if __name__ == "__main__":
    main()
