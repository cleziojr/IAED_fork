import streamlit as st
from openai import OpenAI
from openai import OpenAIError

from config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

@st.cache_resource
def correct_text(user_text: str, system_context: str) -> str:
    messages = [
        {
          "role":    "system",
          "content": f"Você é um tutor de redação do ENEM. Considere o seguinte contexto:\n{system_context}"
        },
        {
          "role":    "user",
          "content": f"Por favor, corrija, avalie e forneça feedback detalhado para esta redação:\n{user_text}"
        }
    ]
    try:
        resp = client.chat.completions.create(model=CHAT_MODEL, messages=messages)
        return resp.choices[0].message.content
    except OpenAIError as e:
        st.error(f"Erro na API de chat: {e}")
        return ""
