# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

class CMD(object):
    def process_global_stats(self, file):
        print("tu mama, la tuya")

        dd = pd.read_csv(file, header=None, encoding="latin-1")

        dd.columns = ["Fecha", "Posicion", "Evento"]
        dd['Fecha'] = pd.to_datetime(dd['Fecha'], format='%d/%m/%Y %H:%M')
        #filter only RDCU eventos
        dd = dd[dd['Posicion'].isin(['RDCU-1', 'RDCU-2'])]
        dd2 = dd['Evento'].str.split(":", expand=True)
        dd['Radar'] = dd2[0]
        dd2 = dd2[1].str.split("Asterix", expand=True)
        dd['Evento'] = dd2[0]



        eventos = dd['Radar'].value_counts().to_frame()
        pos = dd['Posicion'].value_counts().to_frame()
        pos_grouped = dd.groupby(['Radar', "Evento"])['Evento'].count().to_frame()
        event_grouped = dd.groupby(['Posicion',"Radar","Evento", 'Fecha' ])['Evento'].count().to_frame()
        event_grouped.columns = ["Total"]
        pos_grouped.columns = ["Total"]
        dd = dd.set_index("Fecha")
        event_by_day_resampled = dd.resample('12H').apply({'Evento': 'count'})
        event_by_24 = dd.resample('24H').apply({'Evento': 'count'})

        #filtrar eventos por radar
        dd_mng = dd[dd['Radar'].isin(['RADAR MANAGU'])].resample('24H').apply({'Evento': 'count'})
        dd_rpza = dd[dd['Radar'].isin(['RADAR RPZA'])].resample('24H').apply({'Evento': 'count'})
        dd_mcrudo = dd[dd['Radar'].isin(['RADAR MCRUDO'])].resample('24H').apply({'Evento': 'count'})
        dd_rmat = dd[dd['Radar'].isin(['RADAR RMAT'])].resample('24H').apply({'Evento': 'count'})
        dd_met = dd[dd['Radar'].isin(['RADAR RDRMET'])].resample('24H').apply({'Evento': 'count'})
        dd_blf = dd[dd['Radar'].isin(['RADAR RBLU'])].resample('24H').apply({'Evento': 'count'})


        return eventos, pos, pos_grouped, event_grouped, event_by_day_resampled, dd_mng, dd_rpza, dd_mcrudo, dd_rmat, dd_met, dd_blf, event_by_24
