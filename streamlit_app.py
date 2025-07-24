import streamlit as st
import pandas as pd

st.title("Análise de Acessos Reconhecidos")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o arquivo Excel de acessos reconhecidos", type=["xlsx"])

if uploaded_file:
    # Leitura do Excel
    df = pd.read_excel(uploaded_file)

    # Filtrando categorias indesejadas
    categorias_excluir = ["MULTICLUBES - DAY-USE", "ECO LOUNGE", "EcoVip s/ Cadastro", "CASA DA ÁRVORE"]
    df = df[~df["Categoria"].isin(categorias_excluir)]

    # Criando resumo por categoria e preço com total na coluna
    resumo_preco = df.groupby(["Categoria", "Preço"]).agg(
        Quantidade=("Categoria", "count"),
        Total=("Preço", lambda x: f"R$ {x.sum():,.2f}".replace(".", ","))
    ).reset_index()

    # Formatando o preço individual
    resumo_preco["Preço"] = resumo_preco["Preço"].map(lambda x: f"R$ {x:,.2f}".replace(".", ","))

    st.subheader("Resumo de Acessos por Categoria e Preço")
    st.dataframe(resumo_preco)

    # Total geral
    total_reconhecido = df["Preço"].sum()
    total_acessos = df.shape[0]
    percapta_geral = total_reconhecido / total_acessos if total_acessos > 0 else 0

    # Calculando per capta sem bebês (assumindo que a categoria de bebês contém "BEBÊ" no nome)
    df_sem_bebes = df[~df["Categoria"].str.contains("BEBÊ", case=False)]
    total_sem_bebes = df_sem_bebes["Preço"].sum()
    acessos_sem_bebes = df_sem_bebes.shape[0]
    percapta_sem_bebes = total_sem_bebes / acessos_sem_bebes if acessos_sem_bebes > 0 else 0

    st.markdown(f"**Faturamento Total Reconhecido:** R$ {total_reconhecido:,.2f}".replace(".", ","))
    st.markdown(f"**Total de Acessos:** {total_acessos}")
    st.markdown(f"**Per Capta Geral:** R$ {percapta_geral:,.2f}".replace(".", ","))
    st.markdown(f"**Per Capta sem Bebês:** R$ {percapta_sem_bebes:,.2f}".replace(".", ","))
    st.markdown(f"*(Baseado em {acessos_sem_bebes} acessos sem bebês)*")

    # Exibição dos dados brutos abaixo do resumo
    st.subheader("Dados Brutos")
    st.dataframe(df)
