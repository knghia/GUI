#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import serial
import time

import numpy as np
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from Bee.source.path import path
from Bee.source.device import SimpleDevice

class ShowForm(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(ShowForm, self).__init__()
        self.setStyleSheet("background-color: #444953;"
                           "border: solid;"
                           "border-radius: 5px;")

        self.textbrower = QtWidgets.QTextBrowser()
        self.textbrower.setStyleSheet("color: #4FAFE4;font-size:10pt;")

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.textbrower)

        self.device = SimpleDevice.getInstance()
        self.device.com_provider.monitor_data.connect(self.show_data)

    def show_data(self,value):
        # print(value)
        print([hex(elem) for elem in value])
        # self.textbrower.append(value)
