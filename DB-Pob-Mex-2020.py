import plotly.express as px
import requests
import pandas as pd
import streamlit as st

repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json' 
#Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()

st.title("Población de México en el 2020")
columnas = st.columns((2,4.5,2), gap='medium')

df = pd.read_csv("datos/Estados-2020.csv")



with columnas[0]:
    st.markdown("### Relaciones proporcionales")

with columnas[1]:
    st.markdown("###  Población de los estados")
    fig = px.choropleth(data_frame=df, 
                    geojson=mx_regions_geo, 
                    locations=df['NOM_ENT'], # nombre de la columna del Dataframe
                    featureidkey='properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    color=df['POBTOT'], #El color depende de las cantidades
                    color_continuous_scale="magma",
                   )

    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    st.plotly_chart(fig, use_container_width=False)

with columnas[2]:
    st.markdown("Hola mundo")