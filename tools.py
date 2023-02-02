from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from threading import Thread

class Button(QPushButton):
    #Here I have taken window as an argument to stop cyclical imports
    def __init__(self,window,text,pos=None,size = (200,70),func="notentered",text_size=15):
        super().__init__(text, window)
        self.win = window  # setting the window as a class variable
        self.cooldownstate = False
        self.func = func
        if pos is not None: #Move the button if the position argument is specified
            self.move(*pos)
        self.setFixedSize(*size)
        self.setStyleSheet(
        #Setting the style of the button
        '''
        QPushButton {
        border: 4px solid #737373;
        color: white;
        font-family: shanti;'''+
        f"font-size: {text_size}px;" +'''
        border-radius: 4px;
        margin-top: 0px}
        
        QPushButton::hover{
            background: #737373;
        }
        ''')
        self.clicked.connect(self.buttfunctions)
        if self.func == "deleteexcercise":
                    self.setStyleSheet(
        #setting variable margins
                    '''
                    QPushButton {
                    border: 4px solid #BA0001;
                    color: white;
                    font-family: shanti;
                    font-size: 15px;
                    border-radius: 4px;
                    padding: 15px 0;
                    margin-top: 0px}
                    
                    QPushButton::hover{
                        background: #BA0001;
                    }
                    ''')
    def buttfunctions(self):
        #Matching buttons to the screens it should take the user to.
        if not self.cooldownstate:
            match self.func:
                case "datascreen":
                    self.win.datascreen()
                case "startscreen":
                    self.win.startscreen()
                case "tablescreen":
                    self.win.datatable()          
                case "loginscreen":
                    self.win.loginscreen()
                case "addworkoutscreen":
                    self.win.addworkoutscreen()
                case "mainscreen":
                    self.win.clearscreen()
                    self.win.mainscreen()
                case "addentryscreen":
                    self.win.addentryscreen()
                case "notentered":
                    print("Button function must be entered")
                case "createuserscreen":
                    self.win.createuserscreen()
                case _:
                    # Functions that are not transition buttons are managed in the main script 
                    # to avoid back and forth between different files
                    self.win.extrafuncs(self,self.func)

    def notice(self, sleeptime, message, orgmessage): # Gives the user a brief idea of what the button has just done
        def noticefunc():
            self.cooldownstate = True#This variable makes sure that the button wont do anything while the message is displayed
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
         #daemon thread allows the rest of the screen to function while the message is being displayed
        self.noticethread = Thread(target=noticefunc, daemon = True)
        self.noticethread.start()

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
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;

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
        