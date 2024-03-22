import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from dash import Dash, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Función para leer los datos del CSV y convertirlos en un GeoDataFrame
def read_data_from_csv():
    df = pd.read_csv(r"C:\Users\Daniel Bolaños\Downloads\data_2024-03-22_10-02-47.csv", delimiter=';')
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['NEO-M9N Longitude'], df['NEO-M9N Latitude']))
    return gdf

# Inicializa el GeoDataFrame global con los datos del CSV
gdf = read_data_from_csv()

# Crear la aplicación Dash
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Visualización 3D de Datos Satelitales en España"),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Intervalo de actualización en milisegundos
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global gdf
    gdf = read_data_from_csv()

    # Crea la figura utilizando Plotly Graph Objects para una visualización en 3D
    fig = go.Figure(data=[go.Scatter3d(
        x=gdf['NEO-M9N Longitude'],
        y=gdf['NEO-M9N Latitude'],
        z=gdf['BMP Altitude (m)'],  # Usa la altitud como la dimensión Z, ajusta según tu columna
        mode='markers',
        marker=dict(
            size=5,
            color=gdf['BMP Altitude (m)'],  # Color por altitud, ajusta según necesites
            colorscale='Viridis',  # Escala de colores
            opacity=0.8
        )
    )])

    # Ajusta el layout del gráfico
    fig.update_layout(
        scene=dict(
            xaxis_title='Longitud',
            yaxis_title='Latitud',
            zaxis_title='Altitud',
        ),
        margin=dict(r=0, l=0, b=0, t=30)  # Ajusta los márgenes si es necesario
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


# NOTA: Recuerda que el código de visualización no debe estar dentro de un bucle infinito en el script principal.
# En una aplicación real, podrías tener una función de visualización que se actualice periódicamente, por ejemplo, usando una interfaz gráfica de usuario (GUI) con un temporizador o un callback.
