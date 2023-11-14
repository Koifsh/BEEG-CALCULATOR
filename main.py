# import libraries
from PyQt5.QtWidgets import (QMainWindow, QApplication)
import sys,pandas, sqlalchemy
from tools import *
from random import choice
import json


class Screen(QMainWindow): # create a class that is a subclass of the pyqt5 widget class
    def __init__(self):
        super().__init__() # initialize the widget
        self.widgets = {}
        self.setFixedSize(600,600) # set the position and the size
        self.setWindowTitle("Fitness Calculator") # set the title
        self.engine = sqlalchemy.create_engine(url="mysql+pymysql://y12_23_kaiEPQ:%Sj58q5b7@77.68.35.85:3306/y12_23_kaiEPQ")
        self.connection = self.engine.connect()
        
        try:
            with open("data.json", "r") as data:
                self.devicedata = json.load(data)
        except FileNotFoundError:
            deviceid = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
            devicelist = list(self.connection.execute(sqlalchemy.text("SELECT deviceID FROM deviceToUser")))[0]
            while deviceid in devicelist:
                deviceid = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
            self.devicedata = {"deviceid": deviceid}
            with open("data.json","x") as data:
                json.dump(self.devicedata, data)
        
        

        self.excercises = pandas.read_csv("excercises.csv")
        self.workouts = pandas.read_csv("workouts.csv")
        
        # reads data about users and if no users are found create a new data file

        self.userID = list(self.connection.execute(sqlalchemy.text("SELECT userID FROM deviceToUser WHERE deviceID = '%s'" % self.devicedata["deviceid"])))
        self.usernames = list(map(lambda x: x[0],list(self.connection.execute(sqlalchemy.text("SELECT username FROM users")))))
        if self.userID != []:
            self.userID = self.userID[0][0]
            _,self.username,_ = list(self.connection.execute(sqlalchemy.text("SELECT * FROM users WHERE userID = '%s'" % self.userID)))[0]
            print(self.username, self.userID)
            self.mainscreen()
        else:
            self.startscreen()

    #region - SCREENS -----------------------------------------
    def screen(func):#This updates the different frames so that each widget can be seen
        def wrapper(self):
            self.clearscreen()
            func(self)
            self.update()
        return wrapper

    @ screen
    def startscreen(self):
        # Creates a blank screen and then loads 3 widgets onto the screen - this is the first screen the user will see
        self.widgets = {
            "title": Text(self,"Fitness Calculator",(200,0),20),
            "login": Button(self,"Login",(200,60),func=self.loginscreen),
            "createuser" : Button(self,"Create new user",(200,140),func=self.createuserscreen)
        }
    
    @screen
    def mainscreen(self):
        # Creates a blank screen and then loads 3 widgets onto the screeb - this is the main screen 
        self.widgets = {
            "title": Text(self,"Main Menu",(200,0),20),
            "logout": Button(self,"Logout",(10,10),(100,70),self.logout),
            "addworkout": Button(self,"Add new workout",(200,140),func=self.addworkoutscreen),
        }
    
    @screen
    def createuserscreen(self):
        # This is the create user screen with 5 widgets about creating users
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title": Text(self,"Create New User",(225,0),20),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,120),(60,50),func=self.showpassword),
            "submit": Button(self,"Submit",(200,180),func=self.submitcreateuser)
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password) 
    
    @screen
    def loginscreen(self): #This is the login screen with 5 widgets about logging into the saved users
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title": Text(self,"Login",(225,0),20),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,125),(50,40),func=self.showpassword,text_size=12),
            "RememberMe": CheckBox(self,"Remember me",(195,180)),
            "submit": Button(self,"Submit",(200,240),func=self.submitlogin)
            
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password)
    
    @screen
    def addworkoutscreen(self):
        self.widgets= {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title": Text(self,"Add excercise",(225,0),20),
            "workoutbox": Scrollbox(self,(10,100),(580,490)),
            "saveworkout": Button(self,"Save workout",(440,10),(150,50),self.saveworkout)
        }
        self.addrow()

    def update(self):
        for key, widget in self.widgets.items():
            print(key) # To check what widgets have been loaded
            widget.show()
        print()
    
    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None) # deletes the widget from the screen
        self.widgets = {} # deletes the entire widget dictionary
    
        #This is extra functions of buttons that aren't changing frames so that I won't need to switch to the other 
        # script every time I need to create a new button
    
    #endregion SCREENS -------------------------------------------
    #region-BUTTONFUNCTIONS ---------------------------------
    def saveworkout(self):
        excercisesdone = [i[0].currentText() for i in self.widgets["workoutbox"].scrollwidglist]
        if not all(i != "None" for i in excercisesdone):
            self.widgets["saveworkout"].notice(0.5,"Delete Empty Rows","Save Workout")
        elif self.widgets["workoutbox"].scrollwidglist == []:
            self.widgets["saveworkout"].notice(0.5,"Add a Row","Save Workout")
        else:
            newrow = pandas.DataFrame.from_records([{"UID":self.uid,"excercises":excercisesdone}])
            self.workouts = pandas.concat([self.workouts, newrow])
            self.workouts.reset_index(inplace=True,drop=True) # Resets indexes
            self.widgets["saveworkout"].notice(0.5,"Workout Saved","Save Workout")
            self.workouts.to_csv("workouts.csv",index=False) # Saves to the the file#
            
            # w1 = list(map(lambda x: eval(x),self.workouts.loc[self.workouts["UID"]==self.uid,"excercises"]))
    
    def addrow(self):
        index = len(self.widgets["workoutbox"].scrollwidglist)
        
        self.widgets["workoutbox"].scrollwidglist.append([dropdownbox(self,self.excercises["excercise"]),Button(self,"Delete",None,(100,50),self.deleterow)])
        self.widgets["workoutbox"].scrollwidglist[index][1].clicked.connect(lambda : self.deleterow(row=index))
        self.widgets["workoutbox"].scrollwidglist[index][1].setStyleSheet("QPushButton:hover{border: 4px solid red}")
        self.widgets["workoutbox"].layout.removeRow(index)
        self.widgets["workoutbox"].layout.addRow(*self.widgets["workoutbox"].scrollwidglist[index])
        self.widgets["workoutbox"].layout.addRow(Button(self,"add row",None,(100,50),self.addrow))
        
    def deleterow(self,row):
        self.widgets["workoutbox"].layout.removeRow(row)
        self.widgets["workoutbox"].scrollwidglist.pop(row)
    
    def submitlogin(self): # controls what the submit button does in the login screen
        username,password = (self.widgets[i].text() for i in ["username","password"]) # creates a list with the text of each box
        if all(i == "" for i in (username,password)): # If every box is empty
            self.widgets["submit"].notice(0.5,"Boxes aren't filled","Submit")
            return
        
        if username not in self.usernames: # Checks if the username does not exists
            self.widgets["submit"].notice(0.5,"Username does not exist","Submit")
            return

        if list(self.connection.execute(sqlalchemy.text("SELECT password FROM users WHERE username = '%s'" % username)))[0][0] != password: #Checks if the password doesnt match
            self.widgets["submit"].notice(0.5,"Password incorrect","Submit")
            return
        
        self.userID = list(self.connection.execute(sqlalchemy.text("SELECT userID FROM users WHERE username = '%s'" % username)))[0][0]
        if self.widgets["RememberMe"].isChecked():
            self.connection.execute(sqlalchemy.text("INSERT INTO deviceToUser (deviceID, userID) VALUES ('%s','%s')" % (self.devicedata['deviceid'],self.userID)))
        self.username = username
        self.mainscreen()
        
    def submitcreateuser(self): # controls what the submit button does in the create user screen
        username,password = (self.widgets[i].text() for i in ["username","password"]) # creates a list with the text of each box
        if all(i == "" for i in (username,password)):# If every box is empty
            self.widgets["submit"].notice(0.5,"Boxes aren't filled","Submit")
        else:
            if username in self.usernames: # If the user already exists
                self.widgets["submit"].notice(0.5,"Username already exists","Submit")
            else:
                # Appends the new user and password into the dataframe
                self.connection.execute("INSERT INTO users (username,password) VALUES ('%s','%s')" % (username,password) )
                self.username = username
                self.widgets["submit"].notice(0.5,"User created","Submit")
                self.loginscreen()

    def showpassword(self):
        self.showpass = not self.showpass
        if self.showpass:
            self.widgets["password"].setEchoMode(QLineEdit.Normal)
            self.widgets["showpassword"].setText("Hide")
        else:
            self.widgets["password"].setEchoMode(QLineEdit.Password)
            self.widgets["showpassword"].setText("Show")
    
    def createnewexcercise(self): # 1:Legs 2: Chest 3: Bicep 4: Tricep 5:Back 6:Shoulders 7:Lats 8: Core 9: Forearm 0: Full Body
        workout,muscle = (self.widgets[i].text() for i in ["workoutname","bodypart"])
        if all(i == "" for i in (workout,muscle)):# If every box is empty
            self.widgets["addworkout"].notice(0.5,"Boxes aren't filled","Submit")
        else:
            if workout in set(self.excercises): # If the user already exists
                self.widgets["addworkout"].notice(0.5,"Workout already exists","Submit")
            else:
                newrow = pandas.DataFrame.from_records([{"excercise":workout,"musclehit":muscle}])
                self.excercises = pandas.concat([self.excercises,newrow])
                self.excercises.reset_index(drop=True,inplace=True)
                self.widgets["addworkout"].notice(0.5,"Workout added","Add")
                self.excercises.to_csv("excercises.csv",mode="w",index=False)
                for i in ["workoutname","bodypart"]:
                    self.widgets[i].setParent(None)
                    del self.widgets[i]
                self.widgets["workoutname"] = LineEdit(self,"Workout Name",(150,100),(300,50))
                self.widgets["bodypart"] = LineEdit(self,"Muscle Group Hit",(150,160),(300,50))
                self.update()
        
    def logout(self):
        self.connection.execute(sqlalchemy.text("DELETE FROM deviceToUser WHERE deviceID = '%s'" % self.devicedata['deviceid']))
        self.startscreen()
        
    def closeEvent(self, event):
        self.connection.commit()
        super(QMainWindow, self).closeEvent(event)
    
        
    #endregion BUTTONFUNCTIONS ------------------------------

style = {
    "primcol" : "#3D3D3D",
    "seccol" : "#F76D57",
    "accent" : "#2A363B",
    "bgcol" : "#1E1E1E",
    "textcol" : "white",
}

if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
     # initializes the window by instantiating the screen class
    with open("style.css", "r") as file:
        stylesheet = str(file.read())
    
    for key, value in style.items():
        stylesheet = stylesheet.replace(key, value)
    app.setStyleSheet(stylesheet)
    window = Screen()
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been bd.