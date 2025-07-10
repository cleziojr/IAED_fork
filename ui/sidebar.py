import streamlit as st
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils.file_loader import get_user_text


def render_sidebar() -> tuple[str, bool]:
    """
    Renderiza a barra lateral para entrada de texto ou arquivo e botão de envio.

    retorna:
        user_text: texto do usuário (upload ou input)
        submit: True se o botão foi pressionado
    """
    st.sidebar.title("Entrada de Redação")
    uploaded_file: Optional[UploadedFile] = st.sidebar.file_uploader(
        "Envie seu arquivo (.txt ou .json)",
        type=['txt', 'json']
    )
    direct_input: str = st.sidebar.text_area(
        "Ou cole sua redação aqui", height=200
    )
    submit: bool = st.sidebar.button("Enviar para correção")

    # obtém texto final do usuário
    user_text: str = get_user_text(uploaded_file, direct_input)
    return user_text, submit
