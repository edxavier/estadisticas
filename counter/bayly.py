import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from PyQt5 import QtWidgets
from .dialogFileOpener import File_Opener


class Bayly(File_Opener):

    def procesar_archivo(self):
        # Leer el txt y generar un array de valores separados por coma
        lineas = [line.rstrip('\n') for line in open(self.archivo, encoding='latin-1')]

        new_list = []
        for linea in lineas:
            """"['01/09/2019', '10:10:04.755', 'Alarm', '#225:', 'Redundancy overload']"""
            #print(linea)
            if linea.strip().__len__() > 0:
                divicion = linea.split(' ', 2)
                fecha_hora = divicion[0] + ' ' + divicion[1]
                #print([fecha_hora, divicion[2].lstrip().rstrip()])
                new_list.append([fecha_hora, divicion[2].lstrip().rstrip()])

        # Crear un dataframe con la lista de lineasxcolumnas
        table = pd.DataFrame(new_list)
        table.columns = ["Fecha", "Evento"]
        table['Fecha'] = pd.to_datetime(table['Fecha'], format='%y/%m/%d %H:%M:%S')


        table = table.set_index("Fecha")

        conteo_eventos = table.groupby(['Evento'])['Evento'].count()
        conteo_eventos_por_dia = table.resample('D').apply({'Evento': 'count'})
        conteo_eventos_por_fecha = table.groupby(table.index.date).count()['Evento']
        # conteo_eventos_por_fecha_detalle = table.groupby(table.index.date)['descripcion'].value_counts()

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_bayly_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        conteo_eventos.to_frame().to_excel(writer, sheet_name='Conteo de Eventos')
        conteo_eventos_por_dia.to_excel(writer, sheet_name='Conteo por fecha')
        conteo_eventos_por_fecha.to_excel(writer, sheet_name='Conteo por fecha2')
        writer.save()
        writer.close()
        self.graficar(conteo_eventos_por_dia, 'Historial de eventos por dia', 'Fecha', 'Total')
        self.graficar_bar(conteo_eventos.to_frame(), 'Historial de eventos por dia', 'Evento', 'Total')

        return conteo_eventos, conteo_eventos_por_fecha





