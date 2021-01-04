#!/usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/tmp/estadisticaApppapDxQ.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from counter.bayly import Bayly
from counter.aviat import Aviat
from counter.ups import Ups
from counter.tmcs import TMCS
import matplotlib.pyplot as plt


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 500))
        MainWindow.setMaximumSize(QtCore.QSize(1500, 600))
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame.setGeometry(QtCore.QRect(0, 0, 1200, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.horizontalFrame.setAutoFillBackground(False)
        self.horizontalFrame.setStyleSheet("background-color: rgb(0, 124, 186);\n"
                                           "color: rgb(255, 255, 255);")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalFrame)
        self.label_2.setStyleSheet("font: 75 14pt \"Noto Sans\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.horizontalFrame)
        self.label.setStyleSheet("font: 75 14pt \"Noto Sans\";")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalFrame1 = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame1.setGeometry(QtCore.QRect(0, 50, 1200, 410))
        self.horizontalFrame1.setStyleSheet("")
        self.horizontalFrame1.setObjectName("horizontalFrame1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalFrame1)
        self.horizontalLayout_2.setContentsMargins(8, -1, 8, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtContenido = QtWidgets.QTextEdit(self.horizontalFrame1)
        self.txtContenido.setObjectName("txtContenido")
        self.horizontalLayout_2.addWidget(self.txtContenido)
        self.txtResultado = QtWidgets.QTextEdit(self.horizontalFrame1)
        self.txtResultado.setObjectName("txtResultado")
        self.horizontalLayout_2.addWidget(self.txtResultado)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")

        self.menuAbrir = QtWidgets.QMenu(self.menubar)
        self.menuAbrir.setObjectName("menuAbrir")
        self.menuUPS = QtWidgets.QMenu(self.menuAbrir)
        self.menuUPS.setObjectName("menuUPS")
        self.menuTMCS = QtWidgets.QMenu(self.menuAbrir)
        self.menuTMCS.setObjectName("menuTMCS")
        MainWindow.setMenuBar(self.menubar)
        self.menuAviat = QtWidgets.QAction(MainWindow)
        self.menuAviat.setObjectName("menuAviat")
        self.menuBayly = QtWidgets.QAction(MainWindow)
        self.menuBayly.setObjectName("menuBayly")
        self.actionLNB = QtWidgets.QAction(MainWindow)
        self.actionLNB.setObjectName("actionLNB")
        self.actionCCR = QtWidgets.QAction(MainWindow)
        self.actionCCR.setObjectName("actionCCR")
        self.actionMensajes_en_cola = QtWidgets.QAction(MainWindow)
        self.actionMensajes_en_cola.setObjectName("actionMensajes_en_cola")
        self.actionGlobal = QtWidgets.QAction(MainWindow)
        self.actionGlobal.setObjectName("actionGlobal")
        self.menuUPS.addAction(self.actionLNB)
        self.menuUPS.addAction(self.actionCCR)
        self.menuTMCS.addAction(self.actionMensajes_en_cola)
        self.menuTMCS.addAction(self.actionGlobal)
        self.menuAbrir.addAction(self.menuAviat)
        self.menuAbrir.addAction(self.menuBayly)
        self.menuAbrir.addAction(self.menuUPS.menuAction())
        self.menuAbrir.addAction(self.menuTMCS.menuAction())
        self.menubar.addAction(self.menuAbrir.menuAction())

        self.menuBayly.triggered.connect(self.abrir_bayly)
        self.menuAviat.triggered.connect(self.abrir_aviat)

        self.actionLNB.triggered.connect(self.abrir_ups_crucero)
        self.actionCCR.triggered.connect(self.abrir_ups_ccr)

        self.actionMensajes_en_cola.triggered.connect(self.abrir_msg_en_cola)
        self.actionGlobal.triggered.connect(self.abrir_tmcs_global)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Estadisticas"))
        self.label_2.setText(_translate("MainWindow", "Contenido"))
        self.label.setText(_translate("MainWindow", "Resultado"))
        self.menuAbrir.setTitle(_translate("MainWindow", "Abrir archivo"))
        self.menuUPS.setTitle(_translate("MainWindow", "UPS"))
        self.menuTMCS.setTitle(_translate("MainWindow", "TMCS"))
        self.menuAviat.setText(_translate("MainWindow", "Aviat"))
        self.menuBayly.setText(_translate("MainWindow", "Bayly"))
        self.actionLNB.setText(_translate("MainWindow", "LNB"))
        self.actionCCR.setText(_translate("MainWindow", "CCR"))
        self.actionMensajes_en_cola.setText(_translate("MainWindow", "Mensajes en cola"))
        self.actionGlobal.setText(_translate("MainWindow", "Global"))

    def limpiar_cajas(self):
        self.txtContenido.setText('')
        self.txtResultado.setText('')

    def abrir_bayly(self):
        self.limpiar_cajas()
        bayly = Bayly()
        self.txtContenido.setText(bayly.abrir_archivo('*.txt;;*.py'))
        try:
            conteo_evento, conteo_por_dia = bayly.procesar_archivo()
            self.txtResultado.append(bayly.archivo)
            self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
            self.txtResultado.append(str(conteo_evento))
            self.txtResultado.append(' \n\n**********Conteo por dia******** \n\n')
            self.txtResultado.append(str(conteo_por_dia))
            error_message = QtWidgets.QMessageBox(self.centralwidget)
            error_message.setWindowTitle("Aviso")
            error_message.setText("Resultado generado con exito")
            error_message.show()
        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))

    def abrir_aviat(self):
        self.limpiar_cajas()
        aviat = Aviat()
        self.txtContenido.setText(aviat.abrir_archivo('*.csv;;*.py'))
        try:
            conteo_evento, conteo_por_dia = aviat.get_events_count()
            self.txtResultado.append(aviat.archivo)
            self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
            self.txtResultado.append(str(conteo_evento))
            self.txtResultado.append(' \n\n**********Conteo por dia******** \n\n')
            self.txtResultado.append(str(conteo_por_dia))

        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))

    def abrir_tmcs_global(self):
        self.limpiar_cajas()
        tmcs = TMCS()
        contenido = tmcs.abrir_archivo('*.txt;;*.csv;;*.py')
        self.txtContenido.setText(contenido)
        try:
            if(contenido is not None):
                conteo_evento = tmcs.process_global_stats()
                self.txtResultado.append(tmcs.archivo)
                self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
                self.txtResultado.append(str(conteo_evento))                


        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))

    def abrir_ups_crucero(self):
        self.limpiar_cajas()
        ups = Ups()
        self.txtContenido.setText(ups.abrir_archivo('*.txt;;*.py'))
        try:
            conteo_evento, conteo_por_dia = ups.procesar_ups_lnb()
            self.txtResultado.append(ups.archivo)
            self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
            self.txtResultado.append(str(conteo_evento))
            self.txtResultado.append(' \n\n**********Conteo por dia******** \n\n')
            self.txtResultado.append(str(conteo_por_dia))
        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))

    def abrir_ups_ccr(self):
        self.limpiar_cajas()
        ups = Ups()
        self.txtContenido.setText(ups.abrir_archivo('*.txt;;*.py'))
        try:
            conteo_evento, conteo_por_dia = ups.procesar_ups_ccr()
            self.txtResultado.append(ups.archivo)
            self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
            self.txtResultado.append(str(conteo_evento))
            self.txtResultado.append(' \n\n**********Conteo por dia******** \n\n')
            self.txtResultado.append(str(conteo_por_dia))
        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))


    def abrir_msg_en_cola(self):
        self.limpiar_cajas()
        tmcs = TMCS()
        self.txtContenido.setText(tmcs.abrir_archivo('*.txt;;*.py'))
        try:
            conteo_evento, conteo_por_dia = tmcs.procesar_msg_en_cola()
            self.txtResultado.append(tmcs.archivo)
            self.txtResultado.append('**********Conteo Global de eventos******** \n\n')
            self.txtResultado.append(str(conteo_evento))
            self.txtResultado.append(' \n\n**********Conteo por dia******** \n\n')
            self.txtResultado.append(str(conteo_por_dia))

        except Exception as e:  # <- naked except is a bad idea
            error_message = QtWidgets.QErrorMessage(self.centralwidget)
            error_message.setWindowTitle("Error de archivo")
            error_message.showMessage("Imposible procesar el archivo: \n\n" + str(e))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


