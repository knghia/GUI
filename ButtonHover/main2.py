
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class PushButton(QtWidgets.QGroupBox):
    def __init__(self,*args,**kwargs):
        super(PushButton,self).__init__()
        self.setStyleSheet("""QWidget{background-color: #444953;border: None;border-radius: 10px;}""")

        self.label = QtWidgets.QLabel()
        self.label.setFixedSize(25,60)
        self.label.setStyleSheet("""QLabel{background-color: #444953;}""")

        self.config_bt = QtWidgets.QPushButton(text=kwargs['text'])
        pixmap = QtGui.QPixmap("./img/setting.png")
        self.icon = QtGui.QIcon(pixmap)
        self.config_bt.setIcon(self.icon)
        self.config_bt.setIconSize(QtCore.QSize(50,60))
        self.config_bt.setStyleSheet("""QPushButton{
            font-size: 22pt;
            border: None;
            background-color: #444953;}""")
        self.config_bt.setFixedSize(200,60)
        self.config_bt.installEventFilter(self)
        
        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.label)
        box.addWidget(self.config_bt)
        box.setContentsMargins(0,0,0,0)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            self.label.setStyleSheet("""QLabel{
                background-color: #FCC522;
                border-top-left-radius : 10px;
                border-top-right-radius : 0px;
                border-bottom-left-radius : 10px;
                border-bottom-right-radius : 0px;
                }""")
        elif event.type() == QtCore.QEvent.Leave:
            self.label.setStyleSheet("QLabel{background-color: #444953;}")
        return False

class MainWindow(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__()

        # self.setStyleSheet("background-color: red;")
        self.bt = PushButton(text="CONFIG")

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.bt)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())