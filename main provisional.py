# Objetivos de l proyecto: poder hacer un código que nos transmita datos en tiempo real para poder ver:
# - Trayectoria de Despegue, desarrollo del vuelo y landing. (Launching-Landing)
# - Poder recibir mediciones en tiempo real de los sensores y conseguir un mission status.
# - Explorar nuevos tipos de datos que podamos recolectar?


import plotly.graph_objs as go
import numpy as np
import requests

# Función para obtener la elevación del terreno en un punto dado utilizando la API de Google Maps
def get_elevation(lat, lon):
    api_key = 'TU_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['results'][0]['elevation']
    else:
        return None

# Generar datos de ejemplo de trayectoria (latitud, longitud, altitud)
# Aquí deberías reemplazar esta generación de datos con los datos reales del lanzamiento del satélite
num_points = 100
latitudes = np.random.uniform(0, 90, num_points)
longitudes = np.random.uniform(0, 180, num_points)
altitudes = [get_elevation(lat, lon) for lat, lon in zip(latitudes, longitudes)]

# Crear el trazado 3D de la trayectoria
trace = go.Scatter3d(
    x=longitudes,
    y=latitudes,
    z=altitudes,
    mode='lines',
    line=dict(color='blue', width=5),
    name='Trayectoria del Satélite'
)

# Diseñar el diseño del trazado
layout = go.Layout(
    title='Trayectoria del Satélite',
    scene=dict(
        xaxis=dict(title='Longitud'),
        yaxis=dict(title='Latitud'),
        zaxis=dict(title='Altitud')
    )
)

# Crear la figura
fig = go.Figure(data=[trace], layout=layout)

# Visualizar la figura
fig.show()

