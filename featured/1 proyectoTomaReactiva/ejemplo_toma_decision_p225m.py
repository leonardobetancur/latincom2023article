#ejemplo del modelo de toma de decision para la contaminacion
import pandas as pd
import numpy as np
import time
#Graficar los estados
import matplotlib.pyplot as plt

#pasos
#1 toma de los datos de la base de Datos_SIATA_Aire_pm25
#2 transformacion de los datos ETL para darlo al modelo
#3 aplicar el modelo (modelo para toma de decision ON-OFF)
#3.1 ejecutar el modelo
#3.2 calcular el estimador
#3.3 aplicar la hipotesis de solucion
#4 notificar la decision + visualizacion

#paso 1 toma de los datos de la base de Datos_SIATA_Aire_pm25
customer_json_file ='Datos_SIATA_Aire_pm25.json'
customers_json = pd.read_json(customer_json_file, convert_dates=True)
latitudes = customers_json.latitud.values.tolist()
longitudes = customers_json.longitud.values.tolist()

cantidad_registros=len(customers_json.datos[1])
ysuperior=max(latitudes)
yinferior=min(latitudes)
xinferior=min(longitudes)
xsuperior=max(longitudes)
grid_x, grid_y = np.meshgrid(np.linspace(xinferior,xsuperior,100), np.linspace(yinferior,ysuperior,100))
#construyo la interpolacion
from scipy.interpolate import griddata

for k in range(0, 8760):#8760):
    fecha = customers_json.datos[1][k].get('fecha')
    m=[]
    for i in range(21):
        m.append(customers_json.datos[i][k].get('valor'))

    m=np.array(m)

    grid_z0 = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='nearest')
    grid_z2 = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='cubic')

#llenar los datos NaN con el valor de nearest para completar los datos en z1 y z2
    # rows = grid_z0.shape[0]
    # cols = grid_z0.shape[1]
    #
    # for x in range(0, cols - 1):
    #     for y in range(0, rows -1):
    #         if np.isnan(grid_z2[x,y]):
    #             grid_z2[x,y]=grid_z0[x,y]
    plt.contourf(grid_x, grid_y, grid_z2)
    plt.plot(longitudes, latitudes, 'r.', ms=1)
    plt.title(fecha)
    plt.pause(0.01)
plt.colorbar()
plt.show()
#Paso 3 aplicar el modelo (modelo para toma de decision ON-OFF)

#Paso 3.1 ejecutar el modelo

#Paso 3.2 calcular el estimador

#Paso 3.3 aplicar la hipotesis de solucion

#Paso 4 notificar la decision + visualizacion
