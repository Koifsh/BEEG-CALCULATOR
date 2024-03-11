from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import sleep
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
    focusInSignal = pyqtSignal()
    focusOutSignal = pyqtSignal()
    def __init__(self,window,text,pos,size=(200,50)):
        super().__init__(window)
        if pos is not None:
            self.move(*pos)
        
        self.setPlaceholderText(text) # Gives the edit box a prompt
        self.setFixedSize(*size)
    
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusInSignal.emit()
    
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focusOutSignal.emit()
    
class Text(QLabel):
    def __init__(self,window,text,pos,size):
        super().__init__(text,window)
        if pos:
            self.move(*pos)
        self.setAlignment(Qt.AlignVCenter) # changes the alignment to the center of the widget
        self.setFont(QFont("consolas",size))
        self.adjustSize()# adjusts the size of the widget based on text size.

class CheckBox(QCheckBox):
    def __init__(self,window,text,pos):
        super().__init__(text,window)
        self.move(*pos)
        self.setFixedSize(200,42)

class dropdownbox(QComboBox):
    def __init__(self,window,options=list, position = None):
        super().__init__(window)
        self.setFixedSize(100,50)
        self.addItems(options)
        self.move(*position)
        
        

class Scrollbox:
    def __init__(self,window,pos,size):
        self.workoutbox = QGroupBox(window)
        self.scroll = QScrollArea(window)
        self.layout = QGridLayout()
        self.scroll.move(*pos)
        self.scroll.setFixedSize(*size)
        self.layout.setAlignment(Qt.AlignTop)
        self.scrollwidglist = [[Button(window,"add row",None,(100,50),window.addrow)]]
        self.layout.addWidget(*self.scrollwidglist[0],0,1)
        self.workoutbox.setLayout(self.layout)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.workoutbox)
        
    def addText(self,list):
        for i in list:
            self.layout.addWidget(Text(self.window,i,None,15))
        
        
    def show(self):
        self.workoutbox.show()
        self.scroll.show()
        
    def setParent(self,_):
        self.workoutbox.setParent(None)
        self.scroll.setParent(None)


class ExerciseGraph(QWidget):
    def __init__(self, win,x_vals, y_vals):
        super().__init__(win)
        # Create a Matplotlib figure and axis
        self.win = win
        self.figure, self.ax = plt.subplots(figsize=(6,3))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setFixedSize(600,450)
        self.figure.patch.set_facecolor('#1E1E1E')
        self.ax.xaxis.label.set_color('#FFFFFF')  # Dark Gray
        self.ax.yaxis.label.set_color('#FFFFFF')  # Dark Gray
        
        self.ax.grid(True, color='#2A363B')  # Slate Gray
        self.ax.tick_params(axis='x', colors='#FFFFFF',rotation=15)  # Dark Gray
        self.ax.tick_params(axis='y', colors='#FFFFFF')  # Dark Gray

        # Convert x_vals to Python datetime objects
        # Generate some random data for demonstration
        if 0 not in [len(x_vals),len(y_vals)]:
            self.generate(f'Volume Lifted {"lbs" if self.win.devicedata["measurement"] == "imperial" else "kgs"}',x_vals,y_vals)
        else:
            self.generate_no_data()
        
    def generate(self, yaxislabel,x_vals, y_vals):
        self.x_vals, self.y_vals = self.takeMax(zip(x_vals,y_vals))
        # Set background color
        # Set labels color
        self.ax.set_facecolor('#1E1E1E')
        margin = timedelta(days=1)  # Change the timedelta as needed
        self.ax.set_ylabel(yaxislabel)
        start_date = min(self.x_vals) - margin
        end_date = max(self.x_vals) + margin
        self.ax.set_xlim(start_date, end_date)

        # Set y-axis limit
        self.ax.set_ylim(0, max(self.y_vals) + max(y_vals)//10)  # Adjust the limits according to your data
        
        self.graph, = self.ax.plot(self.x_vals, self.y_vals, marker='o', linestyle='-', color='#F76D57', linewidth=2)  # Coral
        self.canvas.draw()
    
    def takeMax(self,data):
        maxData = {}
        for i in data:
            if i[0] in maxData.keys():
                maxData[i[0]] = max(maxData[i[0]],i[1])
            else:
                maxData[i[0]] = i[1]
                
        return maxData.keys(), maxData.values()
    
    def generate_no_data(self):
        self.ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=16,font="Consolas", color='#F76D57')
        self.ax.set_facecolor('#3d3b3b')
        # Remove x and y ticks for cleaner appearance
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas.draw()  # Draw the canvas to display the text
    


    


class Progressbar(QProgressBar):
    def __init__(self,window, pos,text= "", backgroundcolor = "orange", barcolor = "red", min = 0, max = 100):
        super().__init__(window)
        self.win = window
        self.setMinimum(min)
        self.setMaximum(max)
        self.move(*pos)
        self.setFixedSize(180,30)
        self.setFormat(text)
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(quit)