from tkinter import Tk
import pandas as pd
import tkinter.ttk as ttk
from tkinter.ttk import Button, Style
from tkinter.filedialog import *
from tkinter.messagebox import showerror
from counter.aviat import Aviat
from counter.bayly import Bayly
import os


import matplotlib.pyplot as plt
from matplotlib import style
from counter.tmcs import TMCS
from counter.ups import Ups
from counter.cmd import CMD



style.use('ggplot')


class MyApp(Tk):
    aviat_global = None
    aviat_date = None
    aviat_date_sampled = None

    bayly_global = None
    bayly_date = None
    bayly_date_sampled = None

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #print(plt.style.available)

        self.title("Estadisticas MO, UPS, Bayly")
        #self.style = Style()
        #self.style.theme_use('vista')
        #print(self.style.theme_names())
        
    
        self.menubar = Menu(self)
        self.menu_archivo = Menu(self, tearoff=0)
        self.menu_archivo.add_command(label='Eventos Aviat', command=self.open_aviat_files)
        self.menu_archivo.add_command(label='Eventos Bayly', command=self.open_bayly_files)
        self.menu_archivo.add_command(label='Eventos UPS LNB', command=self.open_ups_files)
        self.menu_archivo.add_command(label='Eventos UPS CCR', command=self.open_ups_files2)
        self.menu_archivo.add_command(label='Mensajes en cola TMCS', command=self.open_tmcs_msgs)
        self.menu_archivo.add_command(label='Estadistica global TMCS', command=self.open_tmcs_global_stats)

        self.menu_archivo.add_command(label='Estadisticas CMD', command=self.open_cmd_stats)

        self.menubar.add_cascade(label='Abrir', menu=self.menu_archivo)
        self.menubar.add_command(label='Limpiar datos', command=self.clear_data)



        self.menu_statistics = Menu(self, tearoff=0)
        self.menu_statistics.add_command(label='Generar grafico eventos aviat', command=self.graficar_evento_aviat)
        self.menu_statistics.add_command(label='Generar grafico eventos aviat por fecha', command=self.graficar_evento_aviat_por_fecha)
        self.menu_statistics.add_command(label='Generar grafico eventos bayly', command=self.graficar_bayly)
        self.menu_statistics.add_command(label='Generar grafico eventos bayly por fecha', command=self.graficar_bayly_por_fecha)

        self.menu_statistics.entryconfig(0, state="disabled")
        self.menu_statistics.entryconfig(1, state="disabled")
        self.menu_statistics.entryconfig(2, state="disabled")
        self.menu_statistics.entryconfig(3, state="disabled")

        self.bind('<3>', lambda e: self.menu_statistics.post(e.x_root, e.y_root))

        self.config(menu=self.menubar)

        self.res = Text(self)
        self.res2 = Text(self)
        self.s = ttk.Scrollbar(self, orient=VERTICAL, command=self.res2.yview)
        self.s2 = ttk.Scrollbar(self, orient=VERTICAL, command=self.res.yview)

        self.res2.configure(yscrollcommand=self.s.set)
        self.res.configure(yscrollcommand=self.s2.set)

        self.lb1 = Label(text="Contenido")
        self.lb2 = Label(text="Resultado")

        self.btn = ttk.Button(self, text="Graficar evetos aviat por fecha", command=self.graficar_evento_aviat_por_fecha)
        self.btn.configure(state=DISABLED)

        self.btn2 = ttk.Button(self, text="Graficar evetos aviat", command=self.graficar_evento_aviat)
        self.btn2.configure(state=DISABLED)

        self.lb1.grid(column=0, row=0, pady=10,padx=10)
        self.res.grid(column=0, row=3, pady=10, padx=10)

        self.lb2.grid(column=1, row=0, pady=10, padx=10)
        self.res2.grid(column=1, row=3, pady=10)
        #self.btn.grid(column=1, row=1)

        self.s.grid(column=2, row=3, rowspan=2,  sticky='ns')
        self.s2.grid(columnspan=2, row=3, rowspan=2, sticky='ns')

    def clear_data(self):
        self.res.delete('1.0', END)
        self.res2.delete('1.0', END)
        self.menu_statistics.entryconfig(0, state="disabled")
        self.menu_statistics.entryconfig(1, state="disabled")
        self.menu_statistics.entryconfig(2, state="disabled")
        self.menu_statistics.entryconfig(3, state="disabled")

    def graficar_evento_aviat_por_fecha(self):
        ax = self.aviat_date_sampled.plot()
        plt.xlabel('Fecha')
        plt.ylabel('Numero de eventos')
        plt.title('Eventos por dia')
        #plt.legend()
        plt.show()

    def graficar_evento_aviat(self):
        ax = self.aviat_global.plot.barh()
        for p in ax.patches:
            #for horizontal bars:
            ax.annotate("%.0f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10),
                        textcoords='offset points')
            #Vertical bar labels
            #ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center',
            #       xytext=(0, 10), textcoords='offset points')
        #plt.legend()

        plt.show()

    def graficar_bayly(self):
        ax = self.bayly_global.plot.barh()
        for p in ax.patches:
            # for horizontal bars:
            ax.annotate("%.0f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10),
                        textcoords='offset points')
            # Vertical bar labels
            # ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center',
            #       xytext=(0, 10), textcoords='offset points')
        # plt.legend()
        plt.show()

    def graficar_bayly_por_fecha(self):
        ax = self.bayly_date_sampled.plot()
        # plt.legend()
        plt.show()

    def open_bayly_files(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("TXT", "*.txt"),("All files", "*.*")))
        if fname:
            try:
                print(os.path.dirname(fname))
                dir_path = os.path.dirname(fname)
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                bayly = Bayly()
                self.bayly_date, self.bayly_global, self.bayly_date_sampled = bayly.process_file(fname)
                self.res2.insert(INSERT,
                             "***********Conteo Global de eventos******** \n\n" + str(self.bayly_global)+
                                 "\n\n ------Resumen conteo global-----\n\n"+ str(self.bayly_global.describe()) + "\n\n\n")
                self.res2.insert(INSERT,
                             "***********Conteo de eventos por fecha*****\n\n" + str(self.bayly_date) +
                                 "\n\n-------- Resumen conteo por fecha ------ \n"+ str(self.bayly_date.describe()) +"\n\n\n")
                self.menu_statistics.entryconfig(2, state="normal")
                self.menu_statistics.entryconfig(3, state="normal")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path+'/resultados_bayly.xlsx', engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                self.bayly_global.to_frame().to_excel(writer, sheet_name='Conteo Global')
                # Convert the dataframe to an XlsxWriter Excel object.
                self.bayly_date.to_excel(writer, sheet_name='Conteo de eventos por fecha')

                # Close the Pandas Excel writer and output the Excel file.
                writer.save()

            except Exception as e:  # <- naked except is a bad idea
                print(e)
                showerror("ERROR", "Error al procesar archivo ")
            return


    def open_aviat_files(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"),("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                print(os.path.basename(fname))
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                self.btn.configure(state=NORMAL)

                self.menu_statistics.entryconfig(0, state="normal")
                self.menu_statistics.entryconfig(1, state="normal")

                aviat = Aviat()

                self.aviat_global = aviat.get_events_count(fname)
                self.csev = aviat.get_events_detail_count(fname)
                self.aviat_date, self.aviat_date_sampled = aviat.event_count_by_date(fname)

                self.res2.insert(INSERT,
                                 "*************Conteo Global de eventos:*********** \n\n" + str(self.aviat_global) + "\n\n\n")
                self.res2.insert(END, "\n\n\n**********Resumen Global:******* \n\n" + str(self.aviat_global.to_frame().describe().loc[['count','min','max']]))

                self.res2.insert(END,
                                 "***********Conteo de evento por severidad:*********** \n\n" + str(self.csev))
                self.res2.insert(END, "\n\n\n**********Resumen por severidad:******* \n\n" + str(self.csev.to_frame().describe().loc[['count','min','max']]))

                self.res2.insert(END, "\n\n\n*********Conteo de eventos por fecha: **************\n\n" + str(self.aviat_date))
                self.res2.insert(END, "\n\n\n**********Resumen por fecha:******* \n\n" + str(self.aviat_date.to_frame().describe().loc[['count','min','max']]))

                self.res2.insert(END, "\n\n\n**********Conteo de evento por fecha detallado:******* \n\n" + str(aviat.event_count_by_date_detail(fname)))


                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_aviat_'+str(just_file_name)+'.xlsx', engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                self.aviat_global.to_frame().to_excel(writer, sheet_name='Conteo Global')
                self.csev.to_frame().to_excel(writer, sheet_name='Conteo por severidad')

                # Convert the dataframe to an XlsxWriter Excel object.
                self.aviat_date.to_frame().to_excel(writer, sheet_name='Conteo por fecha')
                aviat.event_count_by_date_detail(fname).to_frame().to_excel(writer, sheet_name='Conteo por fecha detallado')



                # Close the Pandas Excel writer and output the Excel file.
                writer.save()

            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return


    def open_ups_files(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                print(os.path.basename(fname))
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                self.btn.configure(state=NORMAL)

                ups = Ups()
                self.ups_events, self.ups_bydate, self.ups_by_date_resampled,  self.ups_bydate_detail = ups.process_file(fname)
                self.res2.insert(INSERT,
                             "*************Conteo Global de eventos:*********** \n\n" + str(
                                 self.ups_events) + "\n\n\n")

                self.res2.insert(INSERT,
                             "*************Conteo Global de eventos por fecha:*********** \n\n" + str(
                                 self.ups_bydate) + "\n\n\n")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_ups_' + str(just_file_name) + '.xlsx',
                                        engine='xlsxwriter')

                #Convert the dataframe to an XlsxWriter Excel object.
                self.ups_events.to_frame().to_excel(writer, sheet_name='Conteode Eventos')
                self.ups_by_date_resampled.to_excel(writer, sheet_name='Conteo por fecha 1')
                self.ups_bydate.to_frame().to_excel(writer, sheet_name='Conteo por fecha 2')
                self.ups_bydate_detail.to_frame().to_excel(writer, sheet_name='Conteo por fecha detallado')
		# Close the Pandas Excel writer and output the Excel file.
                writer.save()


            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return

    def open_ups_files2(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                print(os.path.basename(fname))
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                self.btn.configure(state=NORMAL)

                ups = Ups()
                self.ups_events, self.ups_bydate, self.ups_by_date_resampled, self.ups_bydate_detail = ups.process_ups_ccr_file(fname)


                self.res2.insert(INSERT,
                                 "*************Conteo Global de eventos:*********** \n\n" + str(
                                     self.ups_events) + "\n\n\n")

                self.res2.insert(INSERT,
                                 "*************Conteo Global de eventos por fecha:*********** \n\n" + str(
                                     self.ups_bydate) + "\n\n\n")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_ups_' + str(just_file_name) + '.xlsx',
                                        engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                self.ups_events.to_frame().to_excel(writer, sheet_name='Conteode Eventos')
                self.ups_by_date_resampled.to_excel(writer, sheet_name='Conteo por fecha 1')
                self.ups_bydate.to_frame().to_excel(writer, sheet_name='Conteo por fecha 2')
                self.ups_bydate_detail.to_frame().to_excel(writer, sheet_name='Conteo por fecha detallado')
		# Close the Pandas Excel writer and output the Excel file.
                writer.save()

            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return


    def open_tmcs_msgs(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                tmcs = TMCS()
                ecount, ecweek, egbyddate, cbydate, cbyday = tmcs.process_msgs(fname)

                self.res2.insert(INSERT,
                             "*************Conteo Global de eventos:*********** \n\n" + str(
                                 ecount) + "\n\n\n")

                self.res2.insert(INSERT,
                                 "*************Conteo por semana de eventos:*********** \n\n" + str(
                                     ecweek) + "\n\n\n")

                self.res2.insert(INSERT,
                                 "*************Conteo  agrupado por evento, fecha:*********** \n\n" + str(
                                     egbyddate) + "\n\n\n")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_tmcs_' + str(just_file_name) + '.xlsx',
                                        engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                ecount.to_frame().to_excel(writer, sheet_name='Conteo de eventos')
                egbyddate.to_excel(writer, sheet_name='Conteo agrupado por evento')
                cbydate.to_frame().to_excel(writer, sheet_name='Conteo agrupado por fecha')
                ecweek.to_excel(writer, sheet_name='Conteo por semana')
                cbyday.to_excel(writer, sheet_name='Conteo por día')
                cbyday.columns = ['Eventos por día']


                cbyday.plot().set_title('Conteo de eventos por día')
                plt.show()
                writer.close()
            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return


    def open_tmcs_global_stats(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                tmcs = TMCS()
                result = tmcs.process_global_stats(fname)
                self.res2.insert(INSERT,
                                 "*************Conteo Global de eventos:*********** \n\n" + str(
                                     result) + "\n\n\n")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_tmcs_' + str(just_file_name) + '.xlsx',
                                        engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                result.to_excel(writer, sheet_name='Conteo de Eventos')
                writer.close()


            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return

    def open_cmd_stats(self):
        self.clear_data()
        fname = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                dir_path = os.path.dirname(fname)
                just_file_name = os.path.basename(fname)
                just_file_name = just_file_name.split('.')[0]
                f = open(fname)
                content = f.read()
                self.res.insert(INSERT, content)
                cmd = CMD()
                eventos, pos, pos_grouped, event_grouped, event_by_day_resampled, dd_mng, dd_rpza, dd_mcrudo, dd_rmat, dd_met, dd_blf, global_events = cmd.process_global_stats(fname)

                self.res2.insert(INSERT,
                                 "*************Media diario de eventos en el periodo:*********** \n\n" + str(
                                     event_by_day_resampled['Evento'].mean()) + "\n\n\n")

                self.res2.insert(INSERT,
                                 "*************Desviacion estandar de eventos en el periodo:*********** \n\n" + str(
                                     event_by_day_resampled['Evento'].std()) + "\n\n\n")
                self.res2.insert(INSERT,
                                 "*************Conteo Global de eventos:*********** \n\n" + str(
                                     eventos) + "\n\n\n")

                self.res2.insert(INSERT,
                                 "*************Conteo por RDCU:*********** \n\n" + str(
                                     pos) + "\n\n\n")

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                writer = pd.ExcelWriter(dir_path + '/resultados_CMD_' + str(just_file_name) + '.xlsx',
                                        engine='xlsxwriter')

                # Convert the dataframe to an XlsxWriter Excel object.
                eventos.to_excel(writer, sheet_name='Conteo de eventos')
                pos.to_excel(writer, sheet_name='Conteo por RDCU')
                event_grouped.to_excel(writer, sheet_name='Conteo agrupado por Radar')
                pos_grouped.to_excel(writer, sheet_name='Conteo agrupado por Radar2')
                event_by_day_resampled.to_excel(writer, sheet_name='Conteo por día')
                std = event_by_day_resampled['Evento'].std()
                mean = event_by_day_resampled['Evento'].mean()


                event_by_day_resampled = event_by_day_resampled.assign(media=mean)
                #event_by_day_resampled = event_by_day_resampled.assign(Managua=dd_mng)
                #event_by_day_resampled = event_by_day_resampled.assign(limite_superior=mean+std)
                #event_by_day_resampled = event_by_day_resampled.assign(limite_inferior=mean-std)
                global_events.columns  = ['TOTAL']
                global_events = global_events.assign(RMNG=dd_mng)
                global_events = global_events.assign(RMCRUD=dd_mcrudo)
                global_events = global_events.assign(RBLF=dd_blf)
                global_events = global_events.assign(RMET=dd_met)
                global_events = global_events.assign(RMAT=dd_rmat)
                global_events = global_events.assign(RPZA=dd_rpza)
                global_events = global_events.fillna(0)
                print (global_events)
                #dd_mng.plot()
                p2 = global_events.plot(ylim=[0,global_events['TOTAL'].max()+1], style=[':',])
                p2.set_title('Conteo por radar c/24H')
                #plt.plot(event_by_day_resampled.index, event_by_day_resampled['Evento'])
                #plt.plot(event_by_day_resampled.index, event_by_day_resampled['media'], 'c-.', grid=True,)
                p = event_by_day_resampled.plot(ylim=[0,event_by_day_resampled['Evento'].max()+1],
                                                color = ['b', 'y', 'm', 'm'], style=['-','-.',':',':',])
                p.set_title('Conteo de eventos por día c/12H')


                plt.show()



                writer.close()

            except Exception as e:  # <- naked except is a bad idea
                showerror("ERROR", "Error al procesar archivo " + str(e))
            return


app = MyApp()

app.mainloop()


"""
window = tk.Tk()
window.title("Estadisticas MO, UPS, Bayly")
#window.geometry("700x300")
entryText = tk.StringVar()

def open_file():
    fname = askopenfilename(filetypes=(("CSV", "*.cvs"),
                                       ("TXT", "*.txt"),
                                       ("All files", "*.*")))
    if fname:
        try:
            print(fname)
            f = open(fname)
            content = f.read()
            print(content)
            window.res.insert(tk.INSERT,content)

        except:  # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return





menubar = tk.Menu(window)
menu_archivo = tk.Menu(menubar,  tearoff=0)
menu_archivo.add_command(label='Archivo UPS', command=open_file)
menu_archivo.add_command(label='Archivo MO')
menu_archivo.add_command(label='Archivo Bayly')
menubar.add_cascade(label='Abrir', menu=menu_archivo)


menu_statistics = tk.Menu(window)
menu_statistics.add_command(label='Generar graficos')

window.bind('<3>', lambda e: menu_statistics.post(e.x_root, e.y_root))

window.config(menu=menubar)

window.res = tk.Text(window).grid(column=0, row=1, pady=10,padx=10)
res2 = tk.Text(window).grid(column=1, row=1, pady=10,padx=10)

lb1 = ttk.Label(text="Contenido").grid(column=0, row=0, pady=10,padx=10)
lb2 = ttk.Label(text="Resultado").grid(column=1, row=0, pady=10,padx=10)
window.mainloop()
"""
