import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from .dialogFileOpener import File_Opener

import plotly.graph_objs as go
from plotly.offline import plot

style.use('fivethirtyeight')

class Ups(File_Opener):

    def procesar_ups_lnb(self):
        # Leer el txt y generar un array de valores separados por coma
        lineas = [line.rstrip('\n') for line in open(self.archivo)]

        new_list = []
        for linea in lineas:
            """"['01/09/2019', '10:10:04.755', 'Alarm', '#225:', 'Redundancy overload']"""
            divicion = linea.split(' ', 4)
            #print(divicion)
            fecha_hora = divicion[0] + ' ' + divicion[1].split('.')[0]

            new_list.append([fecha_hora, divicion[3].replace('#', '').replace(':', ''), divicion[4]])


        # Crear un dataframe con la lista de lineasxcolumnas
        table = pd.DataFrame(new_list)
        table.columns = ["Fecha", "Codigo_evento", "Evento"]
        table['Fecha'] = pd.to_datetime(table['Fecha'], format='%m/%d/%Y %H:%M:%S')
        table = table.set_index("Fecha")


        conteo_eventos = table.groupby(['Codigo_evento', 'Evento'])['Evento'].count()
        conteo_eventos_por_dia = table.resample('D').apply({'Evento': 'count'})
        conteo_eventos_por_fecha = table.groupby(table.index.date).count()['Evento']
        #conteo_eventos_por_fecha_detalle = table.groupby(table.index.date)['descripcion'].value_counts()

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_ups_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        conteo_eventos.to_frame().to_excel(writer, sheet_name='Conteo de Eventos')
        conteo_eventos_por_dia.to_excel(writer, sheet_name='Conteo por fecha')
        conteo_eventos_por_fecha.to_excel(writer, sheet_name='Conteo por fecha2')

        writer.save()
        writer.close()
        self.graficar(conteo_eventos_por_dia, 'Historial de eventos por día', 'Fecha', 'Total')
        #self.graficar_bar(conteo_eventos.to_frame(), 'Historial de eventos por dia', 'Evento', 'Total')

        return conteo_eventos, conteo_eventos_por_dia

    def procesar_ups_ccr(self):
        # Leer el txt y generar un array de valores separados por coma
        lineas = [line.rstrip('\n') for line in open(self.archivo)]

        new_list = []
        for linea in lineas:
            """"['01/09/2019', '10:10:04.755', 'Alarm', '#225:', 'Redundancy overload']"""
            divicion = linea.split(' ', 5)
            #print(divicion)
            fecha_hora = divicion[0] + ' ' + divicion[1].split('.')[0]

            new_list.append([fecha_hora, divicion[3], divicion[5].replace(':', '')])


        # Crear un dataframe con la lista de lineasxcolumnas
        table = pd.DataFrame(new_list)
        table.columns = ["Fecha", "Codigo_evento", "Evento"]
        table['Fecha'] = pd.to_datetime(table['Fecha'], format='%d/%m/%Y %H:%M:%S')
        table = table.set_index("Fecha")


        conteo_eventos = table.groupby(['Codigo_evento', 'Evento'])['Evento'].count()
        conteo_eventos_por_dia = table.resample('D').apply({'Evento': 'count'})
        conteo_eventos_por_fecha = table.groupby(table.index.date).count()['Evento']
        #conteo_eventos_por_fecha_detalle = table.groupby(table.index.date)['descripcion'].value_counts()

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_ups_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        conteo_eventos.to_frame().to_excel(writer, sheet_name='Conteo de Eventos')
        conteo_eventos_por_dia.to_excel(writer, sheet_name='Conteo por fecha')
        conteo_eventos_por_fecha.to_excel(writer, sheet_name='Conteo por fecha2')
        writer.save()
        writer.close()

        self.graficar(conteo_eventos_por_dia, 'Historial de eventos por día', 'Fecha', 'Total')

        return conteo_eventos, conteo_eventos_por_dia