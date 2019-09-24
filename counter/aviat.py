import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from .dialogFileOpener import File_Opener

style.use('fivethirtyeight')


class Aviat(File_Opener):
    def convert_to_year(self, date_in_some_format):

        date_in_some_format = date_in_some_format.split()[1].replace('-', '/') \
                              + " " + date_in_some_format.split()[2].split('.')[0]
        #year_as_string = date_in_some_format[-4:]  # last four characters
        return date_in_some_format


    def get_events_count(self):
        df = pd.read_csv(self.archivo, index_col=0)
        df['DATE/TIME'] = df['DATE/TIME'].apply(self.convert_to_year)
        #print(df['DATE/TIME'])
        # Convertir la fecha a datetime
        df['DATE/TIME'] = pd.to_datetime(df['DATE/TIME'])
        dd5 = df.set_index("DATE/TIME")
        conteo_eventos_por_fecha = dd5.resample('D').apply({'NAME': 'count'})
        conteo, conteo_agrupado = df['NAME'].value_counts(), df.groupby(['NAME', 'SEVERITY'])['STATE'].count()

        ruta, nombre = self.detalle_archivo()
        writer = pd.ExcelWriter(ruta + '/resultados_aviat_' + str(nombre) + '.xlsx', engine='xlsxwriter')
        conteo.to_frame().to_excel(writer, sheet_name='Conteo de Eventos')
        conteo_agrupado.to_frame().to_excel(writer, sheet_name='Conteo de Eventos2')
        conteo_eventos_por_fecha.to_excel(writer, sheet_name='Conteo por fecha')
        writer.save()
        writer.close()

        return conteo, conteo_agrupado


