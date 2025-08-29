import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

RUTA = 'https://docs.google.com/spreadsheets/d/1z_vCJml9NvRVCU-RO8SCMFBrfoeQDM6j/export?format=xlsx'
# Crear encabezado para la aplicación en Streamlit
st.header('Control de calidad - Adulto mayor')

try:
    # uploaded_file = st.file_uploader("Elige archivo excel")
    # if uploaded_file is not None:
    #     df = pd.read_excel(uploaded_file, header=1)
    # else:
    #     st.warning("Por favor, sube un archivo para continuar.")
    #     st.stop()
    df = pd.read_excel(RUTA, header=1)
except FileNotFoundError:
    print("El archivo para el control de calidad no se encuentra no se encuentra disponible.")
    st.write('Problemas con el archivo, intente más tarde')

# Normalizamos los nombres de las columnas
new_columns = [col.strip().lower().replace(' ', '_')
               for col in df.columns]
df.columns = new_columns
# Convertimos la columna 'codigo' a tipo string
df['codigo'] = df['codigo'].astype(str)
# Obtenemos la lista de puestos de salud
eess = df['eess'].unique().tolist()

# Filtramos los datos para el personal con código '99801' y edad mayor o igual a 60
suma_por_eess = df.query("codigo == '99801' and edad >= 60")

puesto_salud = st.pills("Elige puestos de salud", eess,
                        selection_mode="multi", default=['CHALAMARCA'])
filtro = suma_por_eess[suma_por_eess['eess'].isin(puesto_salud)]

st.write("Conteo por puesto de salud y personal 'Código 99801'")
grouped = filtro.groupby(
    ['eess', 'personal']).size().reset_index(name='cantidad')

# Renombrar los encabezados de las columnas
grouped = grouped.rename(columns={
    'eess': 'Puesto de salud',
    'personal': 'Personal',
    'cantidad': 'Cantidad'
})
# Mostrar gráfico de barras y tabla de datos
st.bar_chart(grouped, x="Puesto de salud",
             y="Cantidad", color="Personal", stack=True)
st.dataframe(grouped)
