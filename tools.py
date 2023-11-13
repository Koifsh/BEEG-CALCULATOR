from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import sleep

from PyQt5.QtWidgets import QLineEdit, QWidget
# from threading import Thread



class Button(QPushButton):
    #Here I have taken window as an argument to stop cyclical imports
    def __init__(self,window,text,pos=None,size = (200,70),func=None,text_size=15):
        super().__init__(text, window)
        self.win = window  # setting the window as a class variable
        if pos is not None: #Move the button if the position argument is specified
            self.move(*pos)
        self.setFixedSize(*size)
        self.setFont(QFont("consolas", text_size))
        #self.setStyleSheet("QPushButton:hover{background: accent;}")
        if func == None:
            print("Function not Entered")
            return
        
        self.clicked.connect(func)
    
    def notice(self, sleeptime, message, orgmessage): # Gives the user a brief idea of what the button has just done
         #daemon thread allows the rest of the screen to function while the message is being displayed
        self.worker = Cooldown(sleeptime)
        self.worker.start()
        self.setEnabled(False)
        self.setText(message)
        self.worker.finished.connect(lambda: self.setEnabled(True))
        self.worker.finished.connect(lambda: self.setText(orgmessage))

class Cooldown(QThread):
    def __init__(self, sleeptime) -> None:
        super().__init__()
        self.sleeptime = sleeptime
    
    def run(self):
        sleep(self.sleeptime)
        


class LineEdit(QLineEdit):
    def __init__(self,window,text,pos,size=(200,50)):
        super().__init__(window)
        if pos is not None:
            self.move(*pos)
        self.setPlaceholderText(text) # Gives the edit box a prompt
        self.setFixedSize(*size)
    
class Text(QLabel):
    def __init__(self,window,text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignVCenter) # changes the alignment to the center of the widget
        self.setFont(QFont("consolas",size))
        self.setFixedSize(size*len(text),size*3) # adjusts the size of the widget based on text size.

class CheckBox(QCheckBox):
    def __init__(self,window,text,pos):
        super().__init__(text,window)
        self.move(*pos)
        self.setFixedSize(200,42)

class dropdownbox(QComboBox):
    def __init__(self,window,options=list):
        super().__init__(window)
        self.setFixedSize(300,50)
        self.addItems(options)
        
    
class Scrollbox:
    def __init__(self,window,pos,size):
        self.workoutbox = QGroupBox(window)
        self.scroll = QScrollArea(window)
        self.layout = QFormLayout()
        self.scroll.move(*pos)
        self.scroll.setFixedSize(*size)
        self.scrollwidglist = []
        self.layout.addRow(Button(window,"add row",None,(100,50),window.addrow))
        self.workoutbox.setLayout(self.layout)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.workoutbox)
        
    def show(self):
        self.workoutbox.show()
        self.scroll.show()
        
    def setParent(self,_):
        self.workoutbox.setParent(None)
        self.scroll.setParent(None)



class Progressbar(QProgressBar):
    def __init__(self,window, pos,text= "", backgroundcolor = "orange", barcolor = "red", min = 0, max = 100):
        super().__init__(window)
        self.win = window
        self.setMinimum(min)
        self.setMaximum(max)
        self.move(*pos)
        self.setFixedSize(200,30)
        self.setFormat(text)
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(quit)