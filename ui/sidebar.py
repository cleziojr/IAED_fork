import streamlit as st

def render_sidebar():
    st.sidebar.title("Correção de Redações")
    user_text = st.sidebar.text_area("Digite sua redação aqui:")
    submit = st.sidebar.button("Enviar para correção")
    return user_text, submit
