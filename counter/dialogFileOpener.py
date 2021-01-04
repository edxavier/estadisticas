# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import os
import plotly.graph_objs as go
from plotly.offline import plot
from PyQt5.QtWidgets import QFileDialog
import plotly.express as px


class File_Opener(object):
    archivo = None

    def abrir_archivo(self, filtros):
        self.archivo = QFileDialog.getOpenFileName(
            caption='Abrir archivo', filter=filtros,
            directory="/home/eradar/"
        )[0]
        if self.archivo:
            f = open(self.archivo, 'r', encoding='latin-1')
            with f:
                return f.read()
        else:
            return None

    def detalle_archivo(self):
        ruta_archivo = os.path.dirname(self.archivo)
        nombre_archivo = os.path.basename(self.archivo)
        nombre_archivo = nombre_archivo.split('.')[0]
        return ruta_archivo, nombre_archivo

    def graficar(self, dframe, titulo, descX, descY):
        # conteo_por_dia = conteo_por_dia.to_frame()
        #data = [go.Scatter(x=dframe.index, y=dframe['Evento'])]
        ruta, nombre = self.detalle_archivo()
        layout = go.Layout(
            title=titulo,
            yaxis=dict(title=descY, range=[-2,dframe['Evento'].max()+50]),
            xaxis=dict(title=descX),
        )
        #fig = go.Figure(data=data, layout=layout)
        fig = go.Figure(layout=layout)

        fig.add_trace(go.Scatter(
            x=dframe.index, y=dframe['Evento'],
            line_color='#456987',
            #line = dict(dash = 'dot'),
            name='Eventos',
        ))
        fig.update_traces(mode='lines')
        #fig.show()
        plot(fig, filename=ruta + '/grafico_' + nombre + '.html', auto_open=True)

    def graficar_bar(self, dframe, titulo, descX, descY):
        # conteo_por_dia = conteo_por_dia.to_frame()
        #print(dframe)
        data = [go.Bar(x=dframe['Evento'], y=dframe.index, orientation='h')]
        ruta, nombre = self.detalle_archivo()
        layout = go.Layout(
                    title=titulo,
                    yaxis=dict(title=''),
                    xaxis=dict(title=descY),
                    margin=dict(l=200, r=80, b=80, t=80, pad=12)
                )
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=ruta + '/grafico_' + nombre + '.html', auto_open=True)
