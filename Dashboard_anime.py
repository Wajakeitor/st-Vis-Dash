import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import cufflinks as cf

cf.go_offline()

#DATOS
df = pd.read_csv("animes.csv")
columnas = {
    "score":"Puntaje",
    "ranked":"Rango",
    'uid':"Id",
    'title':"Titulo",
    'synopsis':"Sinopsis",
    'genre':"Genero",
    'aired':"Transmitido",
    'episodes':"Episodios",
    'members':"Miembros",
    'popularity':"Popularidad",
    "img_url":"img"
}
df.rename(columns=columnas, inplace=True)
df.drop_duplicates(inplace=True)
def convertir_con_comillas(cadena):
    elementos = cadena.replace("'", "").strip("[]").split(",")
    return elementos

df['aux_gen'] = df['Genero'].apply(convertir_con_comillas)
df['Primer_genero'] =df['aux_gen'].apply(lambda x: x[0])
df.drop(columns=["Genero"], inplace=True)










# Título de la aplicación
st.title('Animes')

# Barra Lateral - Sidebar
with st.sidebar:
    st.title('Generos')
 
    opciones = ['Comedy','Drama','Sci-Fi','Action','Adventure','Mystery','Slice,of,Life','Fantasy','Romance','Ecchi','Military','School','Magic','Cars','Music''Horror','Historical','Game','Sports','Psychological','Kids','Dementia','Josei','Harem','Space','','Thriller','Demons','Supernatural','Mecha','Parody','Super,Power','Shounen','Hentai','Vampire','Yaoi','Shounen,Ai','Police','Martial,Arts','Shoujo','Seinen','Samurai']
    opcion_seleccionada = st.selectbox('Selecciona una opción:', opciones)

    dfS = df[df["Primer_genero"] == opcion_seleccionada]

    st.write('Genero: ', opcion_seleccionada)




ops = ["Miembros","Popularidad","Rango","Puntaje"]
ops_sel = st.selectbox('Filtar por:', ops)
st.subheader(f"Grafico de {ops_sel} por genero")
if ops_sel in ["Popularidad","Rango","Puntaje"]:
    df_ops = df[["Primer_genero",f"{ops_sel}"]].groupby("Primer_genero").mean()
else:
    df_ops = df.groupby("Primer_genero").sum()
fig = px.pie(df_ops, 
            names=df_ops.index,  
            values=ops_sel,  
            title=f'Distribución de {ops_sel} de Películas por Género')

# Mostramos el gráfico en Streamlit
st.plotly_chart(fig)


st.subheader(f"Top 10 animes del genero: {opcion_seleccionada}")
st.table(dfS[["Titulo","Puntaje"]].sort_values(by="Puntaje", ascending = False, ignore_index=True).head(10))
