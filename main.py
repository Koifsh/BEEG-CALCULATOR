from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
import time
from threading import Thread

class button:
    def __init__(self, defualttitle, clicktitle, click):
        self.butt = QPushButton(self.win)
        self.butt.setText(defaulttitle)
        self.butt.clicked.connect(self.clicked)
        
    def clicked(self):
        self.butt.setText("Clicked")
        def reset():
            time.sleep(1.5)
            self.butt.setText("Click")
        click = Thread(target=reset, daemon=True)
        click.start()

class screen():
    def __init__(self):
        app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(300,300,300,300)
        self.win.setWindowTitle("BEEEEG MUSEL")
        self.label =QtWidgets.QLabel(self.win)
        self.label.setText("LABEL")



        self.win.show()
        sys.exit(app.exec_())

    



window = screen()
