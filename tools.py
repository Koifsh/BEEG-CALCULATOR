from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import sleep

from PyQt5.QtWidgets import QWidget
# from threading import Thread



class Button(QPushButton):
    #Here I have taken window as an argument to stop cyclical imports
    def __init__(self,window,text,pos=None,size = (200,70),func=None,text_size=15,color="#737373"):
        super().__init__(text, window)
        self.win = window  # setting the window as a class variable
        self.func = func
        if pos is not None: #Move the button if the position argument is specified
            self.move(*pos)
        self.setFixedSize(*size)
        self.setStyleSheet(
        #Setting the style of the button
        '''
        QPushButton {'''+
        f"border: 4px solid {color};" +'''
        color: white;
        font-family: shanti;'''+
        f"font-size: {text_size}px;" +'''
        border-radius: 4px;
        margin-top: 0px}
        
        QPushButton::hover{
            background: #737373;
        }
        ''')
        if self.func == None:
            print("Function not Entered")
            return
        
        self.clicked.connect(self.func)
    
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
        self.move(*pos)
        self.setPlaceholderText(text) # Gives the edit box a prompt
        self.setFixedSize(*size)
        self.setStyleSheet(
            #Sets the style of the edit boxes
            '''
            QLineEdit {
            border: 4px solid #d97218;
            color: white;
            font-family: shanti;
            font-size: 15px;
            border-radius: 4px;
            margin-top: 0px}
            '''
        )
        
class Text(QLabel):
    def __init__(self,window,text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignVCenter) # changes the alignment to the center of the widget
        self.setStyleSheet( # sets the style of the text
            "*{"+
            f'''
            font-family: 'consolas';
            font-size: {size}px;
            color: white;
            margin-top: 20px'''
            +"}")
        self.setFixedSize(size*len(text),size*3) # adjusts the size of the widget based on text size.

class CheckBox(QCheckBox):
    def __init__(self,window,text,pos):
        super().__init__(text,window)
        self.move(*pos)
        self.setFixedSize(200,42)
        self.setStyleSheet(
            """
        QCheckBox{
            font-family: 'shanti';
            color: white;
        }
            QCheckBox::indicator {
            width: 30px;
            height: 30px;
            border-radius: 12px;
            border-style: solid;
            border-width: 3px;
            border-color: #737373;
        }
        QCheckBox::indicator:checked {
            background-color: #737373;}
            
        QCheckBox::indicator:hover{
            border-color: #575757;
            }
        """)

class dropdownbox(QComboBox):
    def __init__(self,window,options=list):
        super().__init__(window)
        self.setFixedSize(300,50)
        self.addItems(options)
        self.setStyleSheet("""
            QComboBox {
            border: 4px solid #737373;
            color: white;
            font-family: shanti;
            font-size: 15px;
            border-radius: 4px;
            margin-top: 0px}
            
            QListView {
            border: 4px solid #737373;
            border-radius: 4px;
            color: white;
            font-family: shanti;
            }
            QScrollBar:vertical{
            background-color: #2A2929;
            width: 15px;
            border:none;
            margin: 15px 3px 15px 3px;
            border: 1px transparent #2A2929;
            border-radius: 4px;}
            QScrollBar::handle:vertical{
                background: #d96207;
                min-height: 5px;
                border-radius: 4px;}
            QScrollBar::sub-line:vertical{height:0px;}
            QScrollBar::add-line:vertical{height: 0px;}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;}
                
                           """)

class Scrollbox:
    def __init__(self,window,pos,size):
        self.workoutbox = QGroupBox(window)
        self.scroll = QScrollArea(window)
        self.layout = QFormLayout()
        self.workoutbox.setStyleSheet("QGroupBox{border: none;}")
        self.scroll.move(*pos)
        self.scroll.setFixedSize(*size)
        self.scroll.setStyleSheet("""
        QScrollArea{
            border: 4px solid #737373;
            color: black;
            border-radius: 4px;
            margin-top: 0px;
        }""")
        self.scroll.verticalScrollBar().setStyleSheet("""
    QScrollBar:vertical{
        background-color: #2A2929;
        width: 15px;
        border:none;
        margin: 15px 3px 15px 3px;
        border: 1px transparent #2A2929;
        border-radius: 4px;}
    QScrollBar::handle:vertical{
        background: #d96207;
        min-height: 5px;
        border-radius: 4px;}
    QScrollBar::sub-line:vertical{height:0px;}
    QScrollBar::add-line:vertical{height: 0px;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;}""")
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
    