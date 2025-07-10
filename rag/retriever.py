import streamlit as st
from openai import OpenAI
from openai.error import OpenAIError
from config import OPENAI_API_KEY, CHAT_MODEL

# inicializa cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@st.cache_resource
async def correct_text(user_text: str, system_context: str) -> str:
    """
    Envia prompt ao modelo de chat da OpenAI para correção e feedback de redação.

    monta um prompt com system + user e retorna o conteúdo da resposta.
    """
    messages = [
        {"role": "system", "content": f"Você é um tutor de redação do ENEM. Considere o seguinte contexto:\n{system_context}"},
        {"role": "user", "content": f"Por favor, corrija, avalie e forneça feedback detalhado para esta redação: Ola tudo bem? \n{user_text}"}
    ]
    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"Erro na API de chat: {e}")
        return ""  
