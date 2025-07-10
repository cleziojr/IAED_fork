import streamlit as st
import numpy as np
import faiss
from openai import OpenAI
from openai import OpenAIError

import config
from rag.embeddings import init_vector_store

client = OpenAI(api_key=config.OPENAI_API_KEY)

@st.cache_resource
def retrieve_context(user_text: str, k: int = config.K_NEIGHBORS) -> str:
    df_rubric, index = init_vector_store()
    try:
        res = client.embeddings.create(input=user_text, model=config.EMBEDDING_MODEL)
        emb = np.array(res["data"][0]["embedding"], dtype="float32")
        faiss.normalize_L2(emb)
    except OpenAIError as e:
        st.error(f"Erro ao gerar embedding do usuário: {e}")
        return ""

    _, I = index.search(np.array([emb]), k)
    contexts = df_rubric.iloc[I[0]]["criteria"].tolist()
    return "\n".join(contexts)
