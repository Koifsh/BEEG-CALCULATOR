from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from threading import Thread

class Button(QPushButton):
    #Here I have taken window as an argument to stop cyclical imports
    def __init__(self,window,text,pos=None,size = (200,70),func=None,text_size=15):
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
        if self.func == None:
            print("Function not Entered")
        else:
            self.clicked.connect(self.func)

    def notice(self, sleeptime, message, orgmessage): # Gives the user a brief idea of what the button has just done
        def noticefunc():
            self.setEnabled(False)#This variable makes sure that the button wont do anything while the message is displayed
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.setEnabled(True)
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
        