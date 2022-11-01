from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from threading import Thread
import pandas
import matplotlib.pyplot as plt



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
            value.deleteLater()
            del tempwidgets[key]
        self.widgets = tempwidgets
        print(self.widgets)
    
    def closeEvent(self, event) :
        self.data.to_csv("data.csv",mode="w",index=False)
        event.accept()

class DataFrameEditor(QWidget):
    def __init__(self):
        self.data = window.data
        super().__init__()
        self.resize(1200,800)
        mainLayout = QVBoxLayout()
        self.setWindowTitle("Data")
        self.setStyleSheet("background: #161219;")
        self.table = Table(self.data)
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.table)
        buttonexport = Button(self,"Save edited changes")
        mainLayout.addWidget(buttonexport)
        buttonrevert = Button(self,"Revert changes")
        mainLayout.addWidget(buttonrevert)
        

class Table(QTableWidget):
    def __init__(self, data):
        self.tabledata = data
        super().__init__()
        rowcount, columncount = self.tabledata.shape
        self.setColumnCount(columncount)
        self.setRowCount(rowcount)
        self.setHorizontalHeaderLabels(("Weight","Height","Hours"))
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet('''
                           QTableView {
                           color: white;
                           gridline-color: #737373;
                           font-size:35px;
                           border-style:none;
                            border-bottom: 1px solid #fffff8;
                            border-right: 1px solid #fffff8;
                           background-color: #161219
                           
                           }
                           QHeaderView::section {
                            color: white;
                            background-color: #161219;
                            padding: 4px;
                            border: 1px solid #fffff8;
                            font-size: 14pt;
                            }
                            QTableView::item:focus{
                            color: #d97218;
                            border: 2px solid #d97218;
                            background-color: #161219;
                            }
                            QTableWidget QTableCornerButton::section {
                            background-color: #161219;
                            border: 1px solid #fffff8;
                            }
                            ''')
        
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i,j, QTableWidgetItem(str(self.tabledata.iloc[i,j])))
        
        self.cellChanged[int,int].connect(self.updateDF)
    
    def updateDF(self,row,column):
        text = self.item(row,column).text()
        if isfloat(text) or text.isnumeric():
            self.tabledata.iloc[row,column] = float(text)
        else:
            self.item(row,column).setText(str(window.data.iloc[row,column]))
                
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
    def __init__(self,window, text,pos=None,size = (200,70)):
        super().__init__(text,window)
        self.win = window
        self.cooldownstate = False
        self.message = text
        if pos is not None:
            self.move(*pos)
        if size is not None:
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
                
                case "Show Full Data":
                    window.datatable = DataFrameEditor()
                    window.datatable.show()
                
                case "Save edited changes":
                    window.data = window.datatable.data
                    window.datascreen()
                
                case "Revert changes":
                    window.datatable.__init__()
                    
    def notice(self, sleeptime, message, orgmessage):
        def noticethread():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        Thread(target=noticethread, daemon = True).start()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Screen()
    window.show()
    sys.exit(app.exec_())