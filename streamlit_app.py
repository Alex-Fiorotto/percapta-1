import streamlit as st
import pandas as pd

st.title("Análise de Vendas de Ingressos")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o arquivo Excel de vendas", type=["xlsx"])

if uploaded_file:
    # Leitura do Excel
    df = pd.read_excel(uploaded_file)

    # Filtrando categorias indesejadas
    categorias_excluir = ["MULTICLUBES - DAY-USE", "ECO LOUNGE", "EcoVip s/ Cadastro", "CASA DA ÁRVORE"]
    df = df[~df["Categoria"].isin(categorias_excluir)]

    # Novo resumo: por categoria e preço
    resumo_preco = df.groupby(["Categoria", "Preço"]).agg(
        Quantidade=("Categoria", "count")
    ).reset_index()

    # Formata valores com duas casas decimais e vírgula como separador decimal
    resumo_preco["Preço"] = resumo_preco["Preço"].map(lambda x: f"R$ {x:,.2f}".replace(".", ","))

    st.subheader("Resumo por Categoria e Preço")
    st.dataframe(resumo_preco)

    # Total geral
    total_vendido = df["Preço"].sum()
    total_ingressos = df.shape[0]
    percapta_geral = total_vendido / total_ingressos if total_ingressos > 0 else 0

    st.markdown(f"**Total Geral Vendido:** R$ {total_vendido:,.2f}".replace(".", ","))
    st.markdown(f"**Total de Ingressos:** {total_ingressos}")
    st.markdown(f"**Per Capta Geral:** R$ {percapta_geral:,.2f}".replace(".", ","))

    # Exibição dos dados brutos abaixo do resumo
    st.subheader("Dados Brutos")
    st.dataframe(df)
