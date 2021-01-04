# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from .dialogFileOpener import File_Opener


import plotly.graph_objs as go
from plotly.offline import plot


class TMCS(File_Opener):

    def process_global_stats(self):
        """dd = pd.read_csv(self.archivo, header=None, encoding="latin-1")
        dd.columns = ["inicio", "fin", "tiempo", "status", "elemento", "tipo"]
        #dd['inicio'] = pd.to_datetime(dd['inicio'], format='%d/%m/%Y %H:%M:%S')
        #dd['inicio'] = pd.to_datetime(dd['inicio'], format='%d/%m/%Y %H:%M')
        event_grouped = dd.groupby(['elemento', "tipo", "status"])['status'].count().to_frame()
        event_grouped.columns = ["Total"]
        event_grouped.index.names = ['Elemento', 'Tipo', 'Estado']

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_tmcs_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        event_grouped.to_excel(writer, sheet_name='Conteo de Eventos')

        writer.save()
        writer.close()

        return event_grouped"""
        lines = [line.rstrip('\n') for line in open(self.archivo)]
        rows = []
        for line in lines:
            if(line.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))):
                line = line.strip() #Limiar espacios al inicio y final de la linea
                #Eliminar multiples espacios
                line = ' '.join(line.split())
                #dividiar por espacios por un maximo de hasta 10 columnas
                words = line.split(' ', 10)
                rows.append([
                    words[0] + ' ' + words[1], # Inicio
                    words[2] + ' ' + words[3], # Fin
                    words[9], # Elemento
                    words[10], # Tipo
                    words[8], # Estado
                ])
        # Crear un dataframe con la lista de lineasxcolumnas
        table = pd.DataFrame(rows)
        table.columns = ["Inicio", "Fin", "Elemento", "Tipo", "Estado"]
        table['Inicio'] = pd.to_datetime(table['Inicio'], format='%d/%m/%Y %H:%M:%S')
        table['Fin'] = pd.to_datetime(table['Fin'], format='%d/%m/%Y %H:%M:%S')
        status_duration = (table["Fin"] - table["Inicio"]).astype('timedelta64[s]')
        table['Duracion'] = status_duration

        plt.clf()
        #event_grouped = table.groupby(['Elemento', "Tipo", "Estado",]).agg({'Estado':['count'], 'Duracion':['sum'],})
        # Filtrar filas que la columna Tipo sean diferente a GW_INDRA y PUESTO
        grouped_gw = table[(table.Tipo != "GW_INDRA") & (table.Tipo != "PUESTO")].groupby(['Elemento', "Tipo", "Estado",]).agg({'Estado':['count'], 'Duracion':['sum'],})
        grouped_pos_count = table[(table.Elemento != "GW1") & (table.Elemento != "GW2")].groupby(['Elemento', "Estado",]).agg({'Estado':['count'],})
        grouped_pos_duration = table[(table.Elemento != "GW1") & (table.Elemento != "GW2")].groupby(['Elemento', "Estado",]).agg({'Duracion':['sum'],})
        grouped_pos_duration = (grouped_pos_duration / grouped_pos_duration.groupby(level=0).sum()) * 100

        #event_grouped.columns = ["Total"]
        #event_grouped.index.names = ['Elemento', 'Tipo', 'Estado']
        # Calcular porcentaje de duracion por grupo
        #print((event_grouped / event_grouped.groupby(level=0).sum()) * 100)

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_tmcs_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        grouped_gw.to_excel(writer, sheet_name='Conteo Eventos GW')
        grouped_pos_count.to_excel(writer, sheet_name='Conteo Eventos Puesto')
        grouped_pos_duration.to_excel(writer, sheet_name='Porc. Duracion Evento Puesto')

        writer.save()
        writer.close()
        
        return grouped_gw



    def procesar_msg_en_cola(self):
        # Leer el txt y generar un array de valores separados por coma
        lineas = [line.rstrip('\n') for line in open(self.archivo, encoding='latin-1')]

        new_list = []
        for linea in lineas:
            """"['01/09/2019', '10:10:04.755', 'Alarm', '#225:', 'Redundancy overload']"""
            divicion = linea.split(' ', 2)
            #print(divicion)
            fecha_hora = divicion[0] + ' ' + divicion[1][:-1]
            #print([fecha_hora, divicion[2]])
            new_list.append([fecha_hora, divicion[2].replace(':', '').lstrip().rstrip()])

        # Crear un dataframe con la lista de lineasxcolumnas
        table = pd.DataFrame(new_list)
        table.columns = ["Fecha", "Evento"]
        table['Fecha'] = pd.to_datetime(table['Fecha'], format='%d/%m/%Y %H:%M:%S')
        table = table.set_index("Fecha")

        conteo_eventos = table.groupby(['Evento'])['Evento'].count()


        conteo_eventos_por_dia = table.resample('D').apply({'Evento': 'count'})
        conteo_eventos_por_fecha = table.groupby(table.index.date).count()['Evento']

        conteo_fecha_evento = table.groupby([table.index.date ,'Evento'])['Evento'].count()
        # conteo_eventos_por_fecha_detalle = table.groupby(table.index.date)['descripcion'].value_counts()

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_tmcs_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        conteo_eventos.to_frame().to_excel(writer, sheet_name='Conteo de Eventos')
        conteo_fecha_evento.to_frame().to_excel(writer, sheet_name='Conteo de Fecha-Evento')
        conteo_eventos_por_dia.to_excel(writer, sheet_name='Conteo por fecha')
        conteo_eventos_por_fecha.to_excel(writer, sheet_name='Conteo por fecha2')

        writer.save()
        writer.close()

        self.graficar(conteo_eventos_por_dia, 'Historial de eventos por día', 'Fecha', 'Total')
        #self.graficar_bar(conteo_eventos.to_frame(), 'Historial de eventos por dia', 'Evento', 'Total')

        return conteo_eventos, conteo_eventos_por_dia
