from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from threading import Thread
import pandas
import matplotlib.pyplot as plt

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("BEEEEGGG calculator")
        self.setStyleSheet("background: #161219;")
        try :
            self.data = pandas.read_csv("data.csv")
        except FileNotFoundError:
            frame = dict(weight=[0], height=[0], hours=[0])
            #creates a dataframe with the datatypes of the columns defined
            self.data = pandas.DataFrame(frame)
        self.mainscreen()
        self.show()
        
    def mainscreen(self):
        self.widgets = {
            "title": Text(self,"Beeg Calculator",(225,10),15),
            "data": Button(self,"Show data",(200,60))
        }
        self.update()
    
    def datascreen(self):
        previousweight = self.data["weight"].iloc[-1]
        previousheight = self.data["height"].iloc[-1]
        previoushours = self.data["hours"].iloc[-1]
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50)),
            "title": Text(self,"Data",(225,10),15),
            "weightbox" : LineEdit(self,"Weight",(200,70)),
            "heightbox" : LineEdit(self,"Height",(200,130)),
            "hoursbox" : LineEdit(self,"Hours",(200,190)),
            "submit" : Button(self,"Submit",(200,250),(200,50)),
            "weights" : Text(self,f"Previous weight = {previousweight} ",(10,300),15),
            "heights" : Text(self,f"Previous height = {previousheight}",(10,320),15),
            "hours" : Text(self,f"Previous hours = {previoushours} ",(10,340),15),
            "fulldata" : Button(self,"Show Full Data",(470,10),(120,50))
        }
        self.update()
        
        
    def update(self):
        for widget in self.widgets.values():
            widget.show()
        

    def clearscreen(self):
        tempwidgets = dict(self.widgets)
        for key,value in self.widgets.items():
            value.hide()
            del tempwidgets[key]
    
    def closeEvent(self, event) :
        self.data.to_csv("data.csv",mode="w",index=False)
        event.accept()


class LineEdit(QLineEdit):
    def __init__(self,window,text,pos,size=(200,50)):
        super().__init__(window)
        self.move(*pos)
        self.setPlaceholderText(text)
        self.setFixedSize(*size)
        self.setStyleSheet(
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
    def __init__(self,window, text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignVCenter)
        self.setStyleSheet(
            "*{"+
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;

            margin-top: 20px'''
            +"}")
        self.setFixedSize(size*len(text),size*3)    

class Button(QPushButton):
    def __init__(self,window, text,pos,size = (200,70)):
        super().__init__(text,window)
        self.win = window
        self.cooldownstate = False
        self.message = text
        
        self.move(*pos)
        self.setFixedSize(*size)
        self.setStyleSheet(
        #setting variable margins
        '''
        QPushButton {
        border: 4px solid #737373;
        color: white;
        font-family: shanti;
        font-size: 15px;
        border-radius: 4px;
        padding: 15px 0;
        margin-top: 0px}
        
        QPushButton::hover{
            background: #737373;
        }
        ''')
        self.clicked.connect(self.buttfunctions)
    
    
    def buttfunctions(self):
        if not self.cooldownstate:
            match self.message:
                case "Show data":
                    window.clearscreen()
                    window.datascreen()
                case "Back":
                    window.clearscreen()
                    window.mainscreen()
                case "Submit":
                    editboxes = [window.widgets[i].text() for i in ["weightbox","heightbox","hoursbox"]]
                    if all((i.isnumeric() or isfloat(i)) for i in editboxes):
                        newrow = pandas.DataFrame.from_records([{"weight" : float(editboxes[0]),
                                                                 "height" : float(editboxes[1]),
                                                                 "hours" : float(editboxes[2])}])
                        window.data = pandas.concat([window.data,newrow])
                        window.data.reset_index(drop=True,inplace=True)
                        window.datascreen()
                        self.notice(0.5,"Submitted successfully","Submit")
                    else:
                        self.notice(0.5,"Values entered incorrectly","Submit")
                        
    def notice(self, sleeptime, message, orgmessage):
        def noticethread():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        Thread(target=noticethread, daemon = True).start()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Screen()
    window.show()
    sys.exit(app.exec_())