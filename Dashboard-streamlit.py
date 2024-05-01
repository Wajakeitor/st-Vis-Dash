import streamlit as st
import pandas as pd

df1 = pd.read_csv("animes.csv")
# df2 = pd.read_csv(profiles)
# df3 = pd.read_csv(reviews)

columnas = st.columns((2,1,1))

columnas[0].title("Hello world")

columnas[1].title("Hola mundo")

columnas[2].title("que pasó carnales, viva México")


df1.loc[df1["genre"] == "[]", "genre"] = "['No Etiquetado']"
df1["genero_2"] = df1["genre"].map(lambda x: x[:-1].split(",")).map(lambda x: list(map(lambda y: y[2:-1],x)))
df1["Primer_Genero"] = df1["genero_2"].map(lambda x: x[0])
continuas = ["uid","episodes", "members", "popularity", "ranked", "score"]
generos = df1["Primer_Genero"].unique()



def top10(genero):

    df = df1["Primer_Genero"] == genero
    df1[["title", "popularity"]].sort_values(by="popularity", ascending= False).head(10).reset_index(drop=True)

