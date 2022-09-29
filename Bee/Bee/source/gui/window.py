#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from Bee.source.gui.connect import connect
from Bee.source.gui.show import show

class WidgetWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(WidgetWindow,self).__init__()

        self.resize(970, 600)
        self.setWindowTitle('Bee')
        self.setStyleSheet("background-color: #2E3138;font-weight: bold;font-family: Roboto;")
        self.connect_form = connect.ConnectForm()
        self.show_form = show.ShowForm()

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.connect_form)
        box.addWidget(self.show_form)