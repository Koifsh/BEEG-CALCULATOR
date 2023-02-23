from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from tools import *

class Screen(QMainWindow): # create a class that is a subclass of the pyqt5 widget class
    def __init__(self):
        super().__init__() # initialize the widget
        self.qvlayout = QVBoxLayout()
        
        self.widgets = {}
        self.setGeometry(300,300,600,600) # set the position and the size
        self.setWindowTitle("Fitness Calculator") # set the title
        self.setStyleSheet("background: #161219;")  # set the colour
        self.startscreen()
        
    def screen(func):#This updates the different frames so that each widget can be seen
        def wrapper(self):
            self.box  = QGroupBox(self)
            self.layout = QGridLayout(self)
            func(self)
            for value in self.widgets.values():
                self.layout.addWidget(value,*value.position)
            self.box.setLayout(self.layout)
            self.qvlayout.addWidget(self.box)
            self.setLayout(self.qvlayout)
            self.show()
        return wrapper
    
    @screen
    def startscreen(self):
        self.clearscreen()
        # Creates a blank screen and then loads 3 widgets onto the screen - this is the first screen the user will see
        self.widgets = {
            "back" : Button(self,"Back",(0,0)),
            "addexcercise" : Button(self,"Add excercise",(0,1)),
        }

    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None) # deletes the widget from the screen
        self.widgets = {} # deletes it from the widget dictionary
    
    
    
if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
    window = Screen() # initializes the window by instantiating the screen class
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been closed.