from PyQt5.QtWidgets import *
import sys
import time
from threading import Thread
import csv

try:
    with open("data.txt") as f:
        data = list(csv.DictReader(f))
except FileNotFoundError:
    with open("data.txt",mode="w") as f:
        print("File created successfully")
        header = ["weight", "height", "hours a week"]
        writer = csv.writer(f)
        writer.writerow(header)
except EOFError:
    print("Nothing to read")

class Button:
    def __init__(self, window, func, defaulttitle = "Click", xypos = (0,0), clicktitle = "Clicked"):
        self.clicktitle = clicktitle
        self.defaulttitle = defaulttitle
        self.butt = QPushButton(window)
        self.butt.setText(defaulttitle)
        self.butt.clicked.connect(func)
        self.butt.move(*xypos)
        self.butt.setStyleSheet("QPushButton::pressed{background-color : #808080}")
        
        
    def clicked(self):
        self.butt.setText(self.clicktitle)
        def reset():
            time.sleep(1.5)
            self.butt.setText(self.defaulttitle)
        Thread(target=reset, daemon=True).start()
    
class datawindow(QWidget):
    def __init__(self):
        super().__init__()
        win = QVBoxLayout()
        win.addWidget(QLabel("Weight: "))
        self.setLayout(win)


class Screen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("BEEEEG MUSCLE")
        data = Button(self, self.showdata,"Show Data")


    def showdata(self):
        self.datawin = datawindow()
        self.datawin.show()
    





app = QApplication(sys.argv)
window = Screen()
window.show()
sys.exit(app.exec_())
