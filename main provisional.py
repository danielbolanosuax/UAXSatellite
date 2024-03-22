# Objetivos de l proyecto: poder hacer un código que nos transmita datos en tiempo real para poder ver:
# - Trayectoria de Despegue, desarrollo del vuelo y landing. (Launching-Landing) al poder der con una api de google maps.
# - Poder recibir mediciones en tiempo real de los sensores y conseguir un mission status.
# - Explorar nuevos tipos de datos que podamos recolectar?


import plotly.graph_objs as go
import numpy as np
import requests
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import threading
import time

# Cache para almacenar las elevaciones y reducir las solicitudes a la API
elevation_cache = {}

# Función mejorada para obtener la elevación
def get_elevation(lat, lon):
    cache_key = f"{lat},{lon}"
    if cache_key in elevation_cache:
        return elevation_cache[cache_key]
    
    api_key = 'TU_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        elevation = data['results'][0]['elevation']
        elevation_cache[cache_key] = elevation
        return elevation
    else:
        return None

# Simular datos de sensores en tiempo real
def simulate_sensor_data():
    while True:
        num_points = 100
        latitudes = np.random.uniform(0, 90, num_points)
        longitudes = np.random.uniform(0, 180, num_points)
        altitudes = []
        for lat, lon in zip(latitudes, longitudes):
            elevation = get_elevation(lat, lon)
            if elevation is not None:
                altitude = elevation + np.random.uniform(0, 1000)  # Añade altitud aleatoria para simular el vuelo
            else:
                altitude = np.random.uniform(0, 1000)  # Usa solo la altitud aleatoria si no hay datos de elevación
            altitudes.append(altitude)

        # Aquí deberías actualizar los datos del trazado (esto puede requerir ajustes adicionales en tu código)
        global trace
        trace.x = longitudes
        trace.y = latitudes
        trace.z = altitudes

        time.sleep(10)  # Simula recibir datos cada 10 segundos


# Iniciar la simulación de datos de sensores en un hilo separado
threading.Thread(target=simulate_sensor_data, daemon=True).start()

# Crear el trazado 3D de la trayectoria
trace = go.Scatter3d(
    x=[],
    y=[],
    z=[],
    mode='lines',
    line=dict(color='blue', width=2),
    name='Trayectoria del Satélite'
)

# Crear la figura inicial
fig = go.Figure(data=[trace])

# Iniciar Dash app
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-update-graph', figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # en milisegundos
        n_intervals=0
    )
])

# Callback para actualizar el gráfico en tiempo real
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    return go.Figure(data=[trace], layout=go.Layout(
        title='Trayectoria del Satélite',
        scene=dict(
            xaxis=dict(title='Longitud'),
            yaxis=dict(title='Latitud'),
            zaxis=dict(title='Altitud')
        )
    ))

if __name__ == '__main__':
    app.run_server(debug=True)
