import pandas as pd
import numpy as np
import faiss
import streamlit as st
from openai import OpenAI
from openai.error import OpenAIError

from config import OPENAI_API_KEY, EMBEDDING_MODEL, RUBRIC_CSV_PATH, K_NEIGHBORS

# inicializa client da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@st.cache_resource
def load_rubric_embeddings(
    rubric_csv_path: str = RUBRIC_CSV_PATH,
    embed_model: str = EMBEDDING_MODEL
) -> tuple[pd.DataFrame, faiss.Index]:
    """
    Carrega critérios de avaliação a partir de um CSV, gera embeddings via OpenAI e inicializa um índice FAISS.

    retorna:
        df: DataFrame com coluna 'criteria'
        index: FAISS indexL2 com embeddings normalizados
    """
    # carrega CSV de critérios
    df = pd.read_csv(rubric_csv_path)
    texts = df['criteria'].astype(str).tolist()

    # gera embeddings para cada critério
    embeddings = []
    for text in texts:
        try:
            res = client.embeddings.create(input=text, model=embed_model)
            emb = np.array(res['data'][0]['embedding'], dtype='float32')
            embeddings.append(emb)
        except OpenAIError as e:
            st.error(f"Erro ao gerar embedding para: '{text[:30]}...' -> {e}")
            embeddings.append(np.zeros((len(embeddings[0]) if embeddings else 1536,), dtype='float32'))

    # empilha e normaliza
    emb_matrix = np.vstack(embeddings)
    faiss.normalize_L2(emb_matrix)

    # cria índice e adiciona embeddings
    dim = emb_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(emb_matrix)

    return df, index

@st.cache_resource
def init_vector_store() -> tuple[pd.DataFrame, faiss.Index]:
    """
    Atalho para carregar rubrica e índice FAISS.
    """
    return load_rubric_embeddings(RUBRIC_CSV_PATH, EMBEDDING_MODEL)
