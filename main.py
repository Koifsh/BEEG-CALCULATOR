from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import sys
import time
from threading import Thread
import csv

def read():
    with open("data.txt") as f:
        global data
        data = list(csv.DictReader(f))
        return data

try:
    print(read())
except FileNotFoundError:
    with open("data.txt",mode="w") as f:
        print("File created successfully")
        header = ["weight", "height", "hours a week"]
        zeros = ["0","0","0"]
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(2):writer.writerow(zeros)
    print(read())
except EOFError:
    print("Nothing to read")

print(data)
class Button:
    def __init__(self, screen, func, defaulttitle = "Click", xypos = (0,0), clicktitle = "Clicked"):
        self.clicktitle = clicktitle
        self.defaulttitle = defaulttitle
        def createdatawin():
            screen.datawindow = datawindow()
            screen.datawindow.show()

        def clicked():
            self.butt.setText(self.clicktitle)
            def reset():
                time.sleep(1.5)
                self.butt.setText(self.defaulttitle)
            Thread(target=reset, daemon=True).start()
    
        self.butt = QPushButton(defaulttitle,screen)
        self.butt.move(*xypos)
        self.butt.setStyleSheet("QPushButton::pressed{background-color : #808080}")
        if func == "clicked":self.butt.clicked.connect(clicked)
        if func == "createdatawin":self.butt.clicked.connect(createdatawin)


        
    
class datawindow(QWidget):
    def __init__(self):
        super().__init__()
        win = QVBoxLayout()
        weights = hours = height = ""
        for index,row in enumerate(data):
            weights = weights + ("," if index != 0 else "") + row["weight"] 
            hours = hours + ("," if index != 0 else "") + row["hours a week"]
            height = height + ("," if index != 0 else "") + row["height"]
        print(weights,hours,height)
        win.addWidget(QLabel("Weight: " + weights))
        win.addWidget(QLabel("Height: " + height))
        win.addWidget(QLabel("Hours a week: "+ hours))
        self.setLayout(win)
        self.setWindowTitle("Data")
        self.setGeometry(300,300,300,300)


class Screen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("BEEEEG MUSCLE")
        self.header = QLabel("MUSCLE HELPER",self)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        data = Button(self, "createdatawin","Show Data",(0,30))
        button = Button(self, "clicked","Click",(0,60))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Screen()
    screen.show()
    sys.exit(app.exec_())
