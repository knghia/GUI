
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class PushButton(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(PushButton,self).__init__()

        self.text=kwargs['text']
        self.config_bt = QtWidgets.QPushButton()
        pixmap = QtGui.QPixmap("./img/setting.png")
        self.icon = QtGui.QIcon(pixmap)
        self.config_bt.setIcon(self.icon)
        self.config_bt.setIconSize(QtCore.QSize(100,50))
        self.config_bt.setStyleSheet(
            """QPushButton{
                font-size: 22pt;
                background-color: #444953;
                border-radius: 10px;
            }""")
        self.config_bt.setFixedSize(100,50)
        self.config_bt.installEventFilter(self)
        
        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.config_bt)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            self.config_bt.setText(self.text)
            self.config_bt.setIcon(self.icon)
            self.config_bt.setFixedSize(200,50)
        elif event.type() == QtCore.QEvent.Leave:
            self.config_bt.setText("")
            self.config_bt.setIcon(self.icon)
            self.config_bt.setFixedSize(100,50)
        return False

class MainWindow(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__()

        self.bt = PushButton(text="CONFIG")

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.bt)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())