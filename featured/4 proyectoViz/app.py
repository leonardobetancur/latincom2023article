#importando las librerias para server dash+flask
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

#importando las librerias para trabajar con los datos y los modelos
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import sys

#inializando las variables para las bases de datos
db_radiacion = 'radiacion.db'
db_temperatura = 'temperatura.db'
db_humedad = 'humedad.db'

class Sensor():
    def __init__(self):
        self.sensorID = []
        self.sensorTime = []
        self.values = []
        self.sensorLat = []
        self.sensorLon = []

def leerdb_sensor(sensorid, db):
    con = sqlite3.connect(db)
    curs = con.cursor()
    sensorID = []
    sensorTime = []
    sensorVal = []
    sensorLat = []
    sensorLon = []
    for fila in curs.execute("SELECT * FROM data WHERE idsensor='" + sensorid + "'"):
        sensorID.append(fila[0])
        sensorTime.append(fila[1])
        sensorVal.append(fila[2])
        sensorLat.append(fila[3])
        sensorLon.append(fila[4])
    con.close()
    datasensor = Sensor()
    datasensor.sensorID = sensorID
    datasensor.sensorTime = sensorTime
    datasensor.values = sensorVal
    datasensor.Lat = sensorLat
    datasensor.Lon = sensorLon
    return datasensor
#leer sensor de radiacion (es uno solo)
s_rad = leerdb_sensor("S_RS_ext_C01",db_radiacion)
#leer los sensores de humedad y radiación (son 5x10) en una matriz
w, h = 5, 10; #calculando el x,y
#inicializando matrices
Temp = [[0 for y in range(h)] for x in range(w)]
Hum = [[0 for y in range(h)] for x in range(w)]
#leyendo de la base de datos y asignando a la matriz
for x in range(w):
    for y in range(h):
        Temp[x][y] = leerdb_sensor("s_inv_" + str(x) +"_cam_" + str(y),db_temperatura)
        Hum[x][y] = leerdb_sensor("s_inv_" + str(x) +"_cam_" + str(y),db_humedad)

# Initialize the app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

dict_list = []
dict_list.append({'label': 'radiacion', 'value': 'radiacion'})
dict_list.append({'label': 'temperatura', 'value': 'temperatura'})
dict_list.append({'label': 'humedad', 'value': 'humedad'})

#mostrando los invernaderos como Cards del formato de dash
def create_invernadero(title, Crad, Ctemp, Chum):
    invernadero = dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody(
            [
                html.P("Radiación = "+Crad +" W/m2"),
                html.P("Temperatura = "+Ctemp + " ºC"),
                html.P("Humedad = "+Chum + " %"),
                ]
        )],
        color="secondary", inverse=True
    )
    return(invernadero)


invernadero00 = create_invernadero("Invernadero 1 Cama 1",str(s_rad.values[-1]), str(Temp[0][0].values[-1]),str(Hum[0][0].values[-1]))
invernadero10 = create_invernadero("Invernadero 2 Cama 1",str(s_rad.values[-1]), str(Temp[1][0].values[-1]),str(Hum[1][0].values[-1]))
invernadero20 = create_invernadero("Invernadero 3 Cama 1",str(s_rad.values[-1]), str(Temp[2][0].values[-1]),str(Hum[2][0].values[-1]))

graphRow0 = dbc.Row([dbc.Col(invernadero00, width=3),
                     dbc.Col(invernadero10, width=3),
                     dbc.Col(invernadero20, width=3),], className = "mb-4",)

graphRow1 = dbc.Row([dbc.Col(dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True),width=6),
                     dbc.Col(dcc.Dropdown(id='varselector', options=dict_list,
                                  multi=False,
                                  value='humedad',
                                  style={'backgroundColor': '#1E1E1E'},
                                  className='stockselector'
                                  ),width=3)], className = "mb-4")

app.layout = html.Div([
   html.Div([]),
   html.H1('Visualizar una dB para toma de decisiones'),
   html.Div([html.P('Aplicación que muestra el tablero de control y modelos de un invernadero de flores '),
      html.P('Trabajo elaborado por: Autores + Profesor: Leonardo Betancur A. PhD'),
      html.P('la carreta que quiera poner.. en este ejemplo como mostrar una card + grafica de tiempo')]),
   graphRow0,
   graphRow1
])

@app.callback(Output('timeseries', 'figure'), [Input('varselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1=[]
    if (selected_dropdown_value == 'temperatura'):
        trace1.append(go.Scatter(x=list(range(1,len(Temp[0][0].values))),y=Temp[0][0].values,mode='lines',opacity=0.7,name='grafica',textposition='bottom center'))
    elif (selected_dropdown_value == 'humedad'):
        trace1.append(go.Scatter(x=list(range(1,len(Hum[0][0].values))),y=Hum[0][0].values,mode='lines',opacity=0.7,name='grafica',textposition='bottom center'))
    elif (selected_dropdown_value == 'radiacion'):
        trace1.append(go.Scatter(x=list(range(1,len(s_rad.values))),y=s_rad.values,mode='lines',opacity=0.7,name='grafica',textposition='bottom center'))

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=['#FF4F00', "#5E0DAC", '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': selected_dropdown_value, 'font': {'color': 'white'}, 'x': 0.5},

              ),

              }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=80)
