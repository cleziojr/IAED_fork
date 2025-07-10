# ui/chat_window.py

import streamlit as st
from typing import List, Tuple

def render_chat_window(chat_history: List[Tuple[str, str]]) -> None:
    """
    Exibe o histórico de correções no formato:
      - texto original
      - correção / feedback
    """
    st.header("Chat de Correção")
    if not chat_history:
        st.info("Nenhuma correção realizada ainda.")
        return

    for i, (orig, corr) in enumerate(chat_history, start=1):
        st.subheader(f"Interação {i}")
        st.markdown("**Texto original:**")
        st.write(orig)
        st.markdown("**Correção e Feedback:**")
        st.write(corr)
        st.markdown("---")
