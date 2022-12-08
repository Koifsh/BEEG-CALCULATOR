from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,pandas
from tools import *

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.widgets = {}
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
        self.clearscreen()
        self.widgets = {
            "title": Text(self,"Beeg Calculator",(225,10),15),
            "login": Button(self,"Login",(200,60),func="loginscreen"),
            "createuser" : Button(self,"Create new user",(200,140),func="createuserscreen")
        }
        self.update()
    
    def mainscreen(self):
        self.widgets = {
            "title": Text(self,"Beeg Calculator",(225,10),15),
            "data": Button(self,"Show Data",(200,60),func="datascreen")
        }
        self.update()
    
    def createuserscreen(self):
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func="startscreen"),
            "title": Text(self,"Create New User",(225,10),15),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "submit": Button(self,"Submit",(200,180),func="submitcreateuser")
        }
        self.widgets["password"].setEchoMode(QLineEdit.Password)
        self.update()
        
    def datatable(self):
        self.datatable = DataFrameEditor(self)
        self.datatable.show()
    
    def loginscreen(self):
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func="startscreen"),
            "title": Text(self,"Login",(225,10),15),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "submit": Button(self,"Submit",(200,180),func="submitlogin")
        }
        self.widgets["password"].setEchoMode(QLineEdit.Password)
        self.update()
    
    def datascreen(self):
        self.clearscreen()
        previousweight = self.data["weight"].iloc[-1]
        previousheight = self.data["height"].iloc[-1]
        previoushours = self.data["hours"].iloc[-1]
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func="startscreen"),
            "title": Text(self,"Data",(225,10),15),
            "weightbox" : LineEdit(self,"Weight",(200,70)),
            "heightbox" : LineEdit(self,"Height",(200,130)),
            "hoursbox" : LineEdit(self,"Hours",(200,190)),
            "submit" : Button(self,"Submit",(200,250),(200,50),func="saveresults"),
            "weights" : Text(self,f"Previous weight = {previousweight} ",(10,300),15),
            "heights" : Text(self,f"Previous height = {previousheight}",(10,320),15),
            "hours" : Text(self,f"Previous hours = {previoushours} ",(10,340),15),
            "fulldata" : Button(self,"Show Full Data",(470,10),(120,50),func="tablescreen")
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
    
    def extrafuncs(self,butt,name):
        match name:
            case "saveresults":
                editboxes = [self.widgets[i].text() for i in ["weightbox","heightbox","hoursbox"]]
                if all((i.isnumeric() or isfloat(i)) for i in editboxes):
                    newrow = pandas.DataFrame.from_records([{"weight" : float(editboxes[0]),
                                                                "height" : float(editboxes[1]),
                                                                "hours" : float(editboxes[2])}])
                    self.data = pandas.concat([self.data,newrow])
                    self.data.reset_index(drop=True,inplace=True)
                    self.datascreen()
                    butt.notice(0.5,"Submitted successfully","Submit")
                else:
                    butt.notice(0.5,"Values entered incorrectly","Submit")
                    
            case "submitlogin":
                    editboxes = [self.widgets[i].text() for i in ["username","password"]]
                    if all(i == "" for i in editboxes):
                        butt.notice(0.5,"Boxes aren't filled","Submit")
                    else:
                        if editboxes[0] not in set(self.data["username"]):
                            butt.notice(0.5,"Username does not exist","Submit")
                            print(self.data["username"])
                        else:
                            print(self.data.loc[self.data["username"] == editboxes[0],"password"].values[0])
                            if self.data.loc[self.data["username"] == editboxes[0],"password"].values[0] != editboxes[1]:
                                butt.notice(0.5,"Password incorrect","Submit")
                            else:
                                #placeholder
                                self.clearscreen()
                                self.mainscreen()
                                
            case "submitcreateuser":
                editboxes = [self.widgets[i].text() for i in ["username","password"]]
                if all(i == "" for i in editboxes):
                    butt.notice(0.5,"Boxes aren't filled","Submit")
                else:
                    if editboxes[0] in set(self.data):
                        butt.notice(0.5,"Username already exists","Submit")
                    else:
                        newrow = pandas.DataFrame.from_records([{"username":editboxes[0],"password":editboxes[1]}])
                        self.data = pandas.concat([self.data, newrow])
                        self.data.reset_index(drop=True)
                        butt.notice(0.5,"User created","Submit")
                        self.data.to_csv("data.csv",mode="w",index=False)
            
            case _:
                print("function does not exist")




            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Screen()
    window.show()
    sys.exit(app.exec_())