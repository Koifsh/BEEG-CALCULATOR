# import libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,pandas
from tools import *


class Screen(QMainWindow): # create a class that is a subclass of the pyqt5 widget class
    def __init__(self):
        super(Screen,self).__init__() # initialize the widget
        self.widgets = {}
        self.setGeometry(300,300,600,600) # set the position and the size
        self.setWindowTitle("BEEEEGGG calculator")
        self.setStyleSheet("background: #161219;")  # set the colour
        try : # reads data about users and if no users are found create a new data file
            self.data = pandas.read_csv("users.csv")
            self.startscreen()
        except FileNotFoundError: # creates a new file if it doesn't exist
            frame = dict(username=[],password=[])
            self.data = pandas.DataFrame(frame)
            self.data.to_csv("users.csv",mode="w",index=False)
            self.startscreen()
            
        
    def startscreen(self):
        self.clearscreen()
        # Creates a blank screen and then loads 3 widgets onto the screen - this is the first screen the user will see
        self.widgets = {
            "title": Text(self,"Beeg Calculator",(225,10),15),
            "login": Button(self,"Login",(200,60),func="loginscreen"),
            "createuser" : Button(self,"Create new user",(200,140),func="createuserscreen")
        }
        self.update()
    
    def mainscreen(self):
        # Creates a blank screen and then loads 3 widgets onto the screeb - this is the main screen 
        self.widgets = {
            "title": Text(self,"Beeg Calculator",(225,10),15),
            "logout": Button(self,"Logout",(10,10),(100,70),"startscreen"),
            "data": Button(self,"Show Data",(200,60),func="datascreen")
        }
        self.update()
    
    def createuserscreen(self):
        # This is the create user screen with 5 widgets about creating users
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func="startscreen"),
            "title": Text(self,"Create New User",(225,10),15),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "submit": Button(self,"Submit",(200,180),func="submitcreateuser")
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.widgets["password"].setEchoMode(QLineEdit.Password) 
        self.update()
        
    
    def loginscreen(self): #This is the login screen with 5 widgets about logging into the saved users
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func="startscreen"),
            "title": Text(self,"Login",(225,10),15),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "submit": Button(self,"Submit",(200,180),func="submitlogin")
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.widgets["password"].setEchoMode(QLineEdit.Password)
        self.update()
    
        
    def update(self):#This updates the different frames so that each widget can be seen
        for key, widget in self.widgets.items():
            print(key) # To check what widgets have been loaded
            widget.show()
        print()
        
    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for key, value in self.widgets.items():
            value.setParent(None) # deletes the widget from the screen
            del self.widgets[key] # deletes it from the widget dictionary
    
    def extrafuncs(self,butt,name):
        #This is extra functions of buttons that aren't changing frames so that I won't need to switch to the other 
        # script every time I need to create a new button
        match name:
            case "submitlogin": # controls what the submit button does in the login screen
                
                    editboxes = [self.widgets[i].text() for i in ["username","password"]] # creates a list with the text of each box
                    if all(i == "" for i in editboxes): # If every box is empty
                        butt.notice(0.5,"Boxes aren't filled","Submit")
                    else:
                        if editboxes[0] not in set(self.data["username"]): # Checks if the username does not exists
                            butt.notice(0.5,"Username does not exist","Submit")
                            print(self.data["username"])
                        else:
                            if self.data.loc[self.data["username"] == editboxes[0],"password"].values[0] != editboxes[1]: #Checks if the password doesnt match
                                butt.notice(0.5,"Password incorrect","Submit")
                            else:
                                self.clearscreen()
                                self.mainscreen()
                                
            case "submitcreateuser": # controls what the submit button does in the create user screen
                editboxes = [self.widgets[i].text() for i in ["username","password"]] # creates a list with the text of each box
                if all(i == "" for i in editboxes):# If every box is empty
                    butt.notice(0.5,"Boxes aren't filled","Submit")
                else:
                    if editboxes[0] in set(self.data): # If the user already exists
                        butt.notice(0.5,"Username already exists","Submit")
                    else:
                        # Appends the new user and password into the dataframe
                        newrow = pandas.DataFrame.from_records([{"username":editboxes[0],"password":editboxes[1]}])
                        self.data = pandas.concat([self.data, newrow])
                        self.data.reset_index(drop=True) # Resets indexes
                        butt.notice(0.5,"User created","Submit")
                        self.data.to_csv("users.csv",mode="w",index=False) # Saves to the the file
            
            case _: # Helps to catch logic errors regarding function names
                print("function does not exist")


if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
    window = Screen() # initializes the window by instantiating the screen class
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been closed.