import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

RUTA = 'dataset/BASE DE DATOS JULIO.xlsx'

try:
    df = pd.read_excel(RUTA, header=1)
except FileNotFoundError:
    print("El archivo para el control de calidad no se encuentra no se encuentra disponible.")
else:
    print("El archivo para el control de calidad se ha cargado correctamente.")


new_columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
df.columns = new_columns

# Convertimos la columna 'codigo' a tipo string
df['codigo'] = df['codigo'].astype(str)

# Obtenemos la lista de puestos de salud
eess = df['eess'].unique().tolist()

suma_por_eess = df.query("codigo == '99801' and edad >= 60")

# Crear encabezado para la aplicación en Streamlit
st.header('Control de calidad - Adulto mayor')

puesto_salud = st.pills("Elige puestos de salud", eess,
                        selection_mode="multi", default=eess)
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

st.dataframe(grouped)
st.bar_chart(data=grouped, x='Puesto de salud', y='Cantidad',
             use_container_width=True, height=400)
