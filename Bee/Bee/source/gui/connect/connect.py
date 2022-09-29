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

class ConnectForm(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(ConnectForm, self).__init__()
        self.setStyleSheet("color: white;"
                           "background-color: #444953;"
                           "border: solid;"
                           "border-radius: 10px;")

        self.company_name = QtWidgets.QLabel(self,text="BEE  ")
        self.company_name.setStyleSheet("font-size: 20pt;")

        self.connect_bt = QtWidgets.QPushButton(self,text='CONNECT')
        self.connect_bt.setFixedSize(140,30)
        self.connect_bt.clicked.connect(self.connect_device_action)
        self.connect_bt.setStyleSheet("font-size: 12pt;background-color: #23252B;border-radius: 4px;")

        self.config_bt = QtWidgets.QPushButton(self,text='CONFIG')
        self.config_bt.setFixedSize(140,30)
        self.config_bt.clicked.connect(self.configure_device_action)
        self.config_bt.setStyleSheet("font-size: 12pt;background-color: #23252B;border-radius: 4px;")

        connection_control_layout = QtWidgets.QHBoxLayout(self)
        connection_control_layout.addWidget(self.connect_bt)
        connection_control_layout.addWidget(self.config_bt)
        connection_control_layout.addStretch(1)
        connection_control_layout.addWidget(self.company_name)

        self.device = SimpleDevice.getInstance()
        
    def configure_device_action(self):
        config_dialog = SerialConfigForm()
        result = config_dialog.exec_()
        if result == 0:
            device_config = config_dialog.get_config_value()
            self.device.configure_connection(device_config)

    def connect_device_action(self):
        if self.device.is_connected:
            self.device.dis_connect()
            if self.device.is_connected == False:
                self.connect_bt.setText("CONNECT")
                self.config_bt.setEnabled(True)
        else:
            self.device.connect()
            if self.device.is_connected:
                self.connect_bt.setText("DISCONNECT")
                self.config_bt.setEnabled(False)

class SerialConfigForm(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(SerialConfigForm, self).__init__()
        self.setWindowIcon(QtGui.QIcon(path.get_path_img("gear.png")))
        self.setWindowTitle("CONFIG")
        self.setStyleSheet("background-color: #2E3138;color: #4FAFE4;font-size: 20px;")

        self.port_la = QtWidgets.QLabel(text="Port")
        self.baudrate_la = QtWidgets.QLabel(text="Baud rate")
        self.parity_la = QtWidgets.QLabel(text="Parity")
        self.data_la = QtWidgets.QLabel(text="Data")
        self.stop_la = QtWidgets.QLabel(text="Stop")
        self.timeout_la = QtWidgets.QLabel(text="Time out")
        
        ports = self.get_ports()
        self.port_cb = QtWidgets.QComboBox()
        self.port_cb.addItems(ports)
        part_port = path.get_portname()
        self.port_cb.setCurrentText(part_port)
        
        baud = ['1200', '2400', '4800', '9600','19200', '38400', '57600', '115200', '230400', '250000', '500000','1000000']
        self.baudrate_cb = QtWidgets.QComboBox()
        self.baudrate_cb.addItems(baud)
        
        part_baud = path.get_baudrate()
        self.baudrate_cb.setCurrentText(part_baud)

        data_list = ['8', '7', '6', '5']
        self.data_size_cb = QtWidgets.QComboBox()
        self.data_size_cb.addItems(data_list)
        
        parity_list = ['None', 'Even', 'Odd']
        self.parity_cb = QtWidgets.QComboBox()
        self.parity_cb.addItems(parity_list)

        stop_list = ['1', '1.5', '2']
        self.stop_cb = QtWidgets.QComboBox()
        self.stop_cb.addItems(stop_list)

        self.timeout_edit = QtWidgets.QLineEdit(text="100")
        self.timeout_edit.setValidator(QtGui.QIntValidator())
        self.timeout_edit.setStyleSheet("background-color: #42454C;")

        box = QtWidgets.QHBoxLayout(self)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.port_la)
        box_la.addWidget(self.baudrate_la)
        box_la.addWidget(self.parity_la)
        box_la.addWidget(self.data_la)
        box_la.addWidget(self.stop_la)
        box_la.addWidget(self.timeout_la)
        box.addLayout(box_la)

        box_cb = QtWidgets.QVBoxLayout()
        box_cb.addWidget(self.port_cb)
        box_cb.addWidget(self.baudrate_cb)
        box_cb.addWidget(self.parity_cb)
        box_cb.addWidget(self.data_size_cb)
        box_cb.addWidget(self.stop_cb)
        box_cb.addWidget(self.timeout_edit)
        box.addLayout(box_cb)

        self.device = SimpleDevice.getInstance()

    def get_config_value(self):
        values = {
            'port': self.port_cb.currentText(),
            'baudrate': self.baudrate_cb.currentText(),
            'stop': self.stop_cb.currentText(),
            'size': self.data_size_cb.currentText(),
            'parity':  self.parity_cb.currentText(),
            'timeout':  self.timeout_edit.text()
        }
        path.set_portname(self.port_cb.currentText())
        path.set_baudrate(self.baudrate_cb.currentText())
        return values

    def get_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result[::-1]
