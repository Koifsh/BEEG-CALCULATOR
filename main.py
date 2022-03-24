from PyQt5.QtWidgets import *
import sys
import time
from threading import Thread

class Screen:
    def __init__(self):
        app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(300,300,300,300)
        self.win.setWindowTitle("BEEEEG MUSCLE")

        buttons = []
        for i in range(10):
            b = Button(self,(0,i*30))
            buttons.append(b)


        self.win.show()
        sys.exit(app.exec_())



class Button:
    def __init__(self, window, xypos = (0,0), defaulttitle = "Click", clicktitle = "Clicked"):
        self.clicktitle = clicktitle
        self.defaulttitle = defaulttitle
        self.butt = QPushButton(window.win)
        self.butt.setText(defaulttitle)
        self.butt.clicked.connect(self.clicked)
        self.butt.move(*xypos)
        self.butt.setStyleSheet("QPushButton::pressed""{""background-color : #808080""}")
        
    def clicked(self):
        self.butt.setText(self.clicktitle)
        def reset():
            time.sleep(1.5)
            self.butt.setText(self.defaulttitle)
        Thread(target=reset, daemon=True).start()

window = Screen()

