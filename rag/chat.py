import streamlit as st
import json
from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

@st.cache_resource
def correct_text(user_text: str, system_context: str) -> str:
    system_prompt = f"""
Sua tarefa é analisar a redação abaixo e retornar apenas um JSON no seguinte formato:
{{
  "nota_final": valor,
  "nota_c1": valor,
  "nota_c2": valor,
  "nota_c3": valor,
  "nota_c4": valor,
  "nota_c5": valor,
  "metrica_um": quantidade_de_erros_pontuacao,
  "metrica_dois": quantidade_de_erros_acentuacao,
  "metrica_tres": quantidade_de_erros_grafia,
  "metrica_quatro": quantidade_de_erros_concordancia_verbal,
  "metrica_cinco": quantidade_de_erros_concordancia_nominal,
  "metrica_seis": nota_coerencia_textual,
  "metrica_sete": quantidade_conectivos_usados,
  "metrica_oito": variedade_vocabular,
  "metrica_nove": quantidade_geral_erros_gramaticais,
  "metrica_dez": comprimento_texto_palavras,
  "metrica_onze": sentimento_texto
}}

Atenção:
- Não inclua explicações ou justificativas.
- Retorne apenas o JSON.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text}
    ]

    try:
        resp = client.chat.completions.create(model=CHAT_MODEL, messages=messages)
        return resp.choices[0].message.content.strip()
    except (OpenAIError, json.JSONDecodeError) as e:
        st.error(f"Erro na API ou na conversão do JSON: {e}")
        return "{}"
