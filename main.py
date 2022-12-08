from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,pandas,time
import matplotlib.pyplot as plt
from threading import Thread

class Screen(QMainWindow):
    def init(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("BEEEEGGG calculator")
        self.setStyleSheet("background: #161219;")
        try :
            self.data = pandas.read_csv("data.csv")
            self.startscreen()
        except FileNotFoundError:
            frame = dict(username=[],password=[])
            self.data = pandas.DataFrame(frame)
            self.data.to_csv("data.csv",mode="w",index=False)
            self.startscreen()
            
        
    def startscreen(self):
        self.widgets = {
            "title": Text("Beeg Calculator",(225,10),15),
            "login": Button("Login",(200,60),func="loginscreen"),
            "createuser" : Button("Create new user",(200,140),func="createuserscreen")
        }
        self.update()
    
    def mainscreen(self):
        self.widgets = {
            "title": Text("Beeg Calculator",(225,10),15),
            "data": Button("Show Data",(200,60),func="datascreen")
        }
        self.update()
    
    def createuserscreen(self):
        self.widgets = {
            "back" : Button("Back",(10,10),(100,50),func="startscreen"),
            "title": Text("Create New User",(225,10),15),
            "username": LineEdit("Username",(200,60)),
            "password": LineEdit("Password",(200,120)),
            "submit": Button("Submit",(200,180),func="submitcreateuser")
        }
        self.widgets["password"].setEchoMode(QLineEdit.Password)
        self.update()
        
        
    def datatable(self):
        self.datatable = DataFrameEditor(self)
        self.datatable.show()
    
    def loginscreen(self):
        self.widgets = {
            "back" : Button("Back",(10,10),(100,50),func="startscreen"),
            "title": Text("Login",(225,10),15),
            "username": LineEdit("Username",(200,60)),
            "password": LineEdit("Password",(200,120)),
            "submit": Button("Submit",(200,180),func="submitlogin")
        }
        self.widgets["password"].setEchoMode(QLineEdit.Password)
        self.update()
    
    def datascreen(self):
        previousweight = self.data["weight"].iloc[-1]
        previousheight = self.data["height"].iloc[-1]
        previoushours = self.data["hours"].iloc[-1]
        self.widgets = {
            "back" : Button("Back",(10,10),(100,50),func="startscreen"),
            "title": Text("Data",(225,10),15),
            "weightbox" : LineEdit("Weight",(200,70)),
            "heightbox" : LineEdit("Height",(200,130)),
            "hoursbox" : LineEdit("Hours",(200,190)),
            "submit" : Button("Submit",(200,250),(200,50),func="saveresults"),
            "weights" : Text(f"Previous weight = {previousweight} ",(10,300),15),
            "heights" : Text(f"Previous height = {previousheight}",(10,320),15),
            "hours" : Text(f"Previous hours = {previoushours} ",(10,340),15),
            "fulldata" : Button("Show Full Data",(470,10),(120,50),func="tablescreen")
        }
        self.update()
        
    def update(self):
        for key, widget in self.widgets.items():
            print(key)
            widget.show()
        print()
    def clearscreen(self):
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None)


app = QApplication(sys.argv)
window = Screen()

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
            
class Table(QTableWidget):
    def __init__(self,data):
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
    def __init__(self,text,pos,size=(200,50)):
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
    def __init__(self,text,pos,size):
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
    def __init__(self,text,pos=None,size = (200,70),func="notentered"):
        super().__init__(text, window)
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
                    window.clearscreen()
                    window.datascreen()
                case "startscreen":
                    window.clearscreen()
                    window.startscreen()
                case "saveresults":
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
                case "tablescreen":
                    window.datatable()           
                case "submitlogin":
                    editboxes = [window.widgets[i].text() for i in ["username","password"]]
                    if all(i == "" for i in editboxes):
                        self.notice(0.5,"Boxes aren't filled","Submit")
                    else:
                        if editboxes[0] not in set(window.data["username"]):
                            self.notice(0.5,"Username does not exist","Submit")
                            print(window.data["username"])
                        else:
                            print(window.data.loc[window.data["username"] == editboxes[0],"password"].values[0])
                            if window.data.loc[window.data["username"] == editboxes[0],"password"].values[0] != editboxes[1]:
                                self.notice(0.5,"Password incorrect","Submit")
                            else:
                                #placeholder
                                window.clearscreen()
                                window.mainscreen()
                                
                case "loginscreen":
                    window.clearscreen()
                    window.loginscreen()
                case "notentered":
                    print("Button function must be entered")
                case "submitcreateuser":
                    editboxes = [window.widgets[i].text() for i in ["username","password"]]
                    if all(i == "" for i in editboxes):
                        self.notice(0.5,"Boxes aren't filled","Submit")
                    else:
                        if editboxes[0] in set(window.data):
                            self.notice(0.5,"Username already exists","Submit")
                        else:
                            newrow = pandas.DataFrame.from_records([{"username":editboxes[0],"password":editboxes[1]}])
                            window.data = pandas.concat([window.data, newrow])
                            window.data.reset_index(drop=True)
                            self.notice(0.5,"User created","Submit")
                            window.data.to_csv("data.csv",mode="w",index=False)
                case "createuserscreen":
                    window.clearscreen()
                    window.createuserscreen()

    def notice(self, sleeptime, message, orgmessage):
        def noticefunc():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        self.noticethread = Thread(target=noticefunc, daemon = True)
        self.noticethread.start()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    window.init()
    window.show()
    sys.exit(app.exec_())