#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import threading
import serial
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class SimpleDevice:
    __instance = None

    @staticmethod
    def getInstance():
        if SimpleDevice.__instance == None:
            SimpleDevice()
        return SimpleDevice.__instance

    def __init__(self):
        if SimpleDevice.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.serial_port = serial.Serial()
            self.is_connected = False
            self.parameter_connect = {}
            self.element_list = []
            self.com_provider = SerialThreading()
            SimpleDevice.__instance = self
 
    def configure_connection(self, config_dict):
        self.parameter_connect = {
            "port" : config_dict["port"],
            "baudrate" : int(config_dict["baudrate"]),
            "bytesize" : 8,
            "parity" : 'N',
            "stopbits" : 1,
            "timeout" : 0.1
        }
        print(self.parameter_connect)

    def start_theading(self):
        self.com_provider.master = self.serial_port
        self.com_provider.is_run.connect(self.dis_connect)
        self.com_provider.start()

    def connect(self):
        if self.is_connected == True:
            return
        try:
            self.serial_port.port = self.parameter_connect['port']
            self.serial_port.baudrate = self.parameter_connect['baudrate']
            self.serial_port.parity = self.parameter_connect['parity']
            self.serial_port.stopbits = self.parameter_connect['stopbits']
            self.serial_port.bytesize = self.parameter_connect['bytesize']
            self.serial_port.timeout = self.parameter_connect['timeout']

            self.serial_port.open()
            if self.serial_port.isOpen() == True:
                self.is_connected = True
                self.start_theading()
                return
            else:
                raise "Don\'t response"
        except serial.SerialException as serEx:
            logging.warning("Don\'t response")
            self.show_problem("Don\'t response",0)
            return False

    def dis_connect(self):
        if self.is_connected == True:
            self.is_connected = False
            self.com_provider.master.close()
            for listener in self.element_list:
                listener.setEnabled(False)

    def add_element(self, listener):
        self.element_list.append(listener)

    def show_problem(self,text,status = 1):
        msgBox = QtWidgets.QMessageBox()
        if status == 1:
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
        else:
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle('ConfigTool')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

class SerialThreading(QtCore.QThread):
    monitor_data = QtCore.pyqtSignal(bytes)
    is_run = QtCore.pyqtSignal(bool)

    def __init__(self, master=None, *args,**kwargs):
        super(SerialThreading, self).__init__()
        self._stop_event = threading.Event()
        self.master = master
        self.timeout = 10

    def run(self):
        try:
            while not self.stopped():
                if (self.master.isOpen() == True):
                    bytes_data = self.master.readline()
                    if len(bytes_data) != 0 and bytes_data != None:
                        self.monitor_data.emit(bytes_data)
                        self.timeout = 10
                else:
                    self.timeout -=1
                    if self.timeout == 0:
                        self.is_run.emit(False)
                time.sleep(0.1)
                    
        except serial.SerialException as serial_error:
            logging.error(serial_error, exc_info=True)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()