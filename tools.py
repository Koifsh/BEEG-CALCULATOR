from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from threading import Thread


class Button(QPushButton):
    def __init__(self,window,text,pos=None,size = (200,70),func="notentered"):
        super().__init__(text, window)
        self.win = window
        self.cooldownstate = False
        self.func = func
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
            match self.func:
                case "datascreen":
                    self.win.datascreen()
                case "startscreen":
                    self.win.startscreen()
                case "tablescreen":
                    self.win.datatable()          
                case "loginscreen":
                    self.win.loginscreen()
                case "notentered":
                    print("Button function must be entered")
                case "createuserscreen":
                    self.win.createuserscreen()
                case _:
                    self.win.extrafuncs(self,self.func)

    def notice(self, sleeptime, message, orgmessage):
        def noticefunc():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        self.noticethread = Thread(target=noticefunc, daemon = True)
        self.noticethread.start()

class DataFrameEditor(QWidget):
    def __init__(self,window):
        self.win = window
        self.data = window.data
        super().__init__()
        self.resize(1200,800)
        mainLayout = QVBoxLayout()
        self.setWindowTitle("Data")
        self.setStyleSheet("background: #161219;")
        self.table = Table(self.data)
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.table)

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
    def __init__(self,window,text,pos,size):
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
        
class Table(QTableWidget):
    def __init__(self,window,data):
        self.win = window
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
            self.item(row,column).setText(str(self.win.data.iloc[row,column]))


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
      