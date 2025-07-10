import streamlit as st
import pandas as pd
import plotly.express as px

from utils.metrics import collect_metrics

def render_dashboard(chat_history: list[tuple[str, str]]) -> None:
    st.header("Dashboard de Métricas")
    if not chat_history:
        st.info("Nenhuma métrica para exibir.")
        return

    rows = []
    for idx, (orig, corr) in enumerate(chat_history, start=1):
        m0 = collect_metrics(orig)
        m1 = collect_metrics(corr)
        rows.append({
            "Interação":          idx,
            "Palavras (antes)":   m0["words"],
            "Palavras (depois)":  m1["words"],
            "Erros corrigidos":   (m0["grammar_errors"] or 0) - (m1["grammar_errors"] or 0),
            "Leitura (min)":      round(m1["reading_time_min"], 2),
            "Avg. sent. length":  round(m1["avg_sentence_length"], 2)
        })

    df = pd.DataFrame(rows)

    st.subheader("Contagem de Palavras")
    fig1 = px.bar(
        df,
        x="Interação",
        y=["Palavras (antes)", "Palavras (depois)"],
        barmode="group",
        labels={"value":"Quantidade","variable":"Métrica"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Erros Corrigidos por Interação")
    fig2 = px.line(
        df,
        x="Interação",
        y="Erros corrigidos",
        markers=True,
        labels={"Erros corrigidos":"Erros corrigidos"}
    )
    st.plotly_chart(fig2, use_container_width=True)
