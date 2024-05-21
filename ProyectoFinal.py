import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.animation as animation
import numpy as np

# Configurar el ancho de la página
st.set_page_config(layout="wide")

# Lectura de los datos
df = pd.read_csv("Data/Empleos.csv")
df = df[["Age", "Sex", "Occupation", "Industry Group", "Year", "Workforce", "Worked Hours Week", "Monthly Wage"]]

df["Años agrupados"] = pd.cut(df['Age'], bins=range(15, 106, 5), right=False).apply(lambda x: x.left)

st.title("Población laboralmente activa en México")

# Agregar un menú desplegable en la barra lateral
opcionplt = st.sidebar.selectbox("Seleccione una opción",
                                 ["Barrenderos y Trabajadores de Limpieza (Excepto en Hoteles y Restaurantes)",
                                  "Trabajadores de Apoyo en Actividades Administrativas Diversas",
                                  "Empleados de Ventas, Despachadores y Dependientes en Comercios",
                                  "Vigilantes y Guardias en Establecimientos",
                                  "Comerciantes en Establecimientos",
                                  "Legisladores",
                                  "Altas Autoridades Gubernamentales y Jurisdiccionales",
                                  "Directores y Gerentes en Centros de Investigación y Desarrollo Tecnológico",
                                  "Directores y Gerentes en Producción Minera, Petrolera y Gas",
                                  "Investigadores y Especialistas en Física",
                                  "Capitanes, Tenientes y Jefes de Área de las Fuerzas Armadas",
                                  "Comandantes de las Fuerzas Armadas",
                                  "Caucheros, Chicleros, Resineros y Similares",
                                  "Trabajadores de la Fuerza Armada Terrestre",
                                  "Oficiales Maquinistas de Transporte Marítimo",
                                  "Secretarias",
                                  "Directores y Gerentes en Informática"])

# Graficos de matplotlib
columns = st.columns((2,3))

with columns[0]:
    st.markdown("### Brecha Salarial")
    
    df0 = df[df["Occupation"] == opcionplt].groupby("Sex").agg({"Monthly Wage": 'mean'}).reset_index().rename(columns={"Monthly Wage": "Salario Mensual", "Sex": "Sexo"})
    X = df0["Sexo"].values
    Y = df0["Salario Mensual"].values

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(3,3))
    ax.bar(X, Y, color=['blue', 'pink'], width = 0.5)

    # Añadir etiquetas y título
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Salario')
    st.markdown(f"##### Salario promedio mensual de \n ##### {opcionplt}")

    # Mostrar el gráfico
    st.pyplot(fig)

    st.write(f"###### La diferencia es de ${abs(Y[0]-Y[1]):.02f} que es un {Y[0]/Y[1]*100-100:2f}%")


with columns[1]:
    st.markdown("### Horas de trabajo semanales")

    df0 = df.groupby(["Year", "Años agrupados"], observed=False).agg({"Worked Hours Week": 'mean'}).reset_index().rename(columns={"Worked Hours Week": "Chamba Semanal"})

    # Crear la figura y los ejes
    fig, ax = plt.subplots()
    ax.set_xlim((df0["Year"].min(), df0["Year"].max()))
    ax.set_ylim((df0["Chamba Semanal"].min(), df0["Chamba Semanal"].max()))
    lines = [ax.plot([], [])[0] for _ in range(17)]
    texts = [ax.text(1,1,f"{i*5 + 15}") for i in range(17)]

    x_data = [0 for _ in range(17)]
    y_data = [0 for _ in range(17)]
    x_1 = [0 for _ in range(17)]
    y_1 = [0 for _ in range(17)]

    for i in range(17):
            x_data[i] = df0[df0["Años agrupados"] == 5*i + 15]["Year"]
            y_data[i] = df0[df0["Años agrupados"] == 5*i + 15]["Chamba Semanal"]
            x_1[i] = np.linspace(x_data[i].min(), x_data[i].max(), 6*(x_data[i].max()-x_data[i].min()))
            y_1[i] = np.interp(x_1[i], x_data[i].values, y_data[i].values)
    
    # Añadir etiquetas de colores para cada grupo de edad

    # Inicializar la línea
    def init():
        for text in texts:
            text.set_position((0, 0))

        for line in lines:
            line.set_data([], [])
        return lines + texts

    # Función de actualización para la animación
    def update(frame):
        for i, line in enumerate(lines):
            line.set_data(x_1[i][:frame], y_1[i][:frame])
            texts[i].set_position((x_1[i][frame-1], y_1[i][frame-1]))
        return lines + texts

    # Crear la animación
    ani = animation.FuncAnimation(fig, update, frames=len(x_1[0]), init_func=init, blit=True, interval=1000/60, repeat=True)

    # Guardar la animación como un archivo GIF
    ani.save("animation.gif", writer='pillow')

    # Mostrar la animación en Streamlit
    st.image("animation.gif", use_column_width=True)

st.columns(1)

df

st.markdown("###### Datos recopilados de: https://www.economia.gob.mx/datamexico/es/vizbuilder?booleans=64&cube=inegi_enoe&drilldowns%5B0%5D=Age+Group.Age&drilldowns%5B1%5D=Sex&drilldowns%5B2%5D=Occupation+Actual+Job.Occupation.Occupation&drilldowns%5B3%5D=Industry+Actual+Job.Industry.Industry+Group&drilldowns%5B4%5D=Date.Year&locale=es&measures%5B0%5D=Workforce&measures%5B1%5D=Worked+Hours+Week&measures%5B2%5D=Monthly+Wage")