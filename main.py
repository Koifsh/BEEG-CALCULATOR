# import libraries
from PyQt5.QtWidgets import (QMainWindow, QApplication)
import sys,pandas, sqlalchemy
from random import choice
import json, datetime
from functools import partial
from tools import *


class Screen(QMainWindow): # create a class that is a subclass of the pyqt5 widget class
    def __init__(self):
        super().__init__() # initialize the widget
        self.widgets = {}
        self.setFixedSize(600,600) # set the position and the size
        self.setWindowTitle("Fitness Calculator") # set the title
        self.engine = sqlalchemy.create_engine(url="mysql+pymysql://y12_23_kaiEPQ:%Sj58q5b7@77.68.35.85:3306/y12_23_kaiEPQ")
        self.connection = self.engine.connect()
        
        try:
            with open("./data/data.json", "r") as data:
                self.devicedata = json.load(data)
        except FileNotFoundError:
            deviceid = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
            devicelist = list(self.connection.execute(sqlalchemy.text("SELECT deviceID FROM deviceToUser")))[0]
            while deviceid in devicelist:
                deviceid = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
            self.devicedata = {"deviceid": deviceid,"measurement": "metric"}
            with open("./data/data.json","x") as data:
                json.dump(self.devicedata, data)
        
        self.excercises = pandas.read_csv("./data/excercises.csv")
        # reads data about users and if no users are found create a new data file
        self.strengthexcercises = self.excercises.loc[self.excercises["category"] == "Strength", "excercise"]
        self.cardioexcercises = self.excercises.loc[self.excercises["category"] == "Cardio", "excercise"]
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
            "title":        Text(self,"Fitness Calculator",(200,0),20),
            "login":        Button(self,"Login",(200,60),func=self.loginscreen),
            "createuser" :  Button(self,"Create new user",(200,140),func=self.createuserscreen)
        }
    
    @screen
    def mainscreen(self):
        # Creates a blank screen and then loads 3 widgets onto the screeb - this is the main screen 
        self.widgets = {
            "title":        Text(self,"Main Menu",(200,0),20),
            "logout":       Button(self,"Logout",(10,10),(100,70),self.logout),
            "addworkout":   Button(self,"Add new workout",(200,140),func=self.addworkoutscreen),
            "1repmax" :     Button(self, "1 Rep Max Calculator", (200,220), func=self.onerepmaxscreen),
            "displaydata":  Button(self,"Display Workouts",(200,300),func=self.displaydata),
            "options" :     Button(self, "Options", (200,430),func=self.optionsscreen),
        }
    
    @screen
    def createuserscreen(self):
        # This is the create user screen with 5 widgets about creating users
        self.widgets = {
            "back" :        Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title":        Text(self,"Create New User",(225,0),20),
            "username":     LineEdit(self,"Username",(200,60)),
            "password":     LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,120),(60,50),func=self.showpassword),
            "submit":       Button(self,"Submit",(200,180),func=self.submitcreateuser),
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password) 
    
    @screen
    def loginscreen(self): #This is the login screen with 5 widgets about logging into the saved users
        self.widgets = {
            "back" :        Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title":        Text(self,"Login",(225,0),20),
            "username":     LineEdit(self,"Username",(200,60)),
            "password":     LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,125),(50,40),func=self.showpassword,text_size=12),
            "RememberMe":   CheckBox(self,"Remember me",(195,180)),
            "submit":       Button(self,"Submit",(200,240),func=self.submitlogin)
            
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password)
    
    @screen
    def addworkoutscreen(self):
        self.rowID = 0
        self.widgets= {
            "back" :        Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title":        Text(self,"Add workout",(225,0),20),
            "workoutbox":   Scrollbox(self,(10,100),(580,490)),
            "saveworkout":  Button(self,"Save workout",(440,10),(150,50),self.saveworkout)
        }
        self.addrow()

    @screen
    def onerepmaxscreen(self):
        desctext = """
Enter a weight and the max reps you can acheive on it
*1 rep max is calculated by averaging Matt Bryzcki's formula,
Epley's formula and Lander's formula
        """
        self.widgets = {
            "back" :        Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title":        Text(self,"1 Rep Max Calculator",(225,0),20),
            "weight" :      LineEdit(self,"Weight",(10,150)),
            "x":            Text(self,"x",(215,150),20),
            "reps":         LineEdit(self,"Reps",(240,150)),
            "go":           Button(self,"Go",(450,150),(90,50),func=self.submitonerep),
            "estimatetext": Text(self,"Estimated one rep",(10,210),40),
            "estimate":     Button(self,"",(250,210),(100,50),func=None),
            "desc":         Text(self,desctext,(10,300),12),
        }
        self.widgets["estimate"].setEnabled(False)
        self.widgets["weight"].setValidator(QIntValidator())
        self.widgets["reps"].setValidator(QIntValidator())
    
    @screen
    def optionsscreen(self):
        self.widgets = {
            "back" :            Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title" :           Text(self,"Options",(225,0),15),
            "changeaesthetic":  Button(self,"Change Aesthetic",(200,140),func=self.stylechangescreen),
            "Metric System":    Button(self,f"Measurement: {self.devicedata['measurement']}",(200,220),func=self.changesystem),
            }

    
    @screen
    def stylechangescreen(self):
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.optionsscreen),
            "title" : Text(self,"Change ",(225,0),15),
            "resetcolors": Button(self, "Reset Colours",(390,10),func=self.resetcolors),
            "background" : Button(self,"Background",(200,180),func=lambda: self.colourpicker("bgcol")),
            "accent" :  Button(self,"Accent",(200,260),func=lambda: self.colourpicker("accent")),
            "primary":   Button(self,"Primary",(200,340),func=lambda: self.colourpicker("primcol")),
            "secondary":  Button(self,"Secondary",(200,420),func=lambda: self.colourpicker("seccol")),
            "textcolour": Button(self,"Text Colour",(200,500), func=lambda: self.colourpicker("textcol")),
        }

    @screen
    def displaydata(self):
        self.workoutdata = self.getWorkoutData()
        
        workoutdata = self.workoutdata.loc[self.workoutdata["excercise"].isin(self.strengthexcercises), ["datetime", "weight","reps","sets"]]
        volume = list(map((lambda weight,reps,sets : int(weight) * int(reps) * int(sets)), workoutdata["weight"],workoutdata["reps"],workoutdata["sets"]))
        print(volume)
        print(workoutdata["datetime"])
        self.widgets = {
            "back" :        Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title" :       Text(self,"Display Data",(225,0),15),
            "graph" :       ExerciseGraph(self,workoutdata["datetime"],volume),
            "type" :        dropdownbox(self,["Volume", "Weight", "Speed","Distance", "Time"],(20,80)),
            "excercise":    LineEdit(self,"Excercise",(130,80)),
            "generate" :    Button(self,"Generate",(340,80),(100,50),func=self.generateGraph)
        }
        self.dropdowntypechange()
        self.widgets["graph"].move(10,100)
        self.widgets["type"].currentTextChanged.connect(self.dropdowntypechange)
        
    def dropdowntypechange(self):
        match self.widgets["type"].currentText():
            case "Volume" | "Weight":
                self.validExcercises = QCompleter(self.excercises.loc[self.excercises["category"] == "Strength", "excercise"])
            
            case "Speed" | "Distance" | "Time":
                self.validExcercises = QCompleter(self.excercises.loc[self.excercises["category"] == "Cardio", "excercise"])
        self.validExcercises.setCaseSensitivity(Qt.CaseInsensitive)
        self.validExcercises.setFilterMode(Qt.MatchContains)
        self.widgets["excercise"].setCompleter(self.validExcercises)
    
    def generateGraph(self):
        excercisetype = self.widgets["type"].currentText()
        excercisename = self.widgets["excercise"].text()
        graph = lambda : self.widgets["graph"]
        strengthexcercises = self.workoutdata.loc[self.workoutdata["excercise"].isin(self.strengthexcercises), ["excercise","datetime", "weight","reps","sets"]].copy()
        strengthexcercises["weight"] = pandas.to_numeric(strengthexcercises["weight"], errors="coerce") * (2.2046226218 if self.devicedata["measurement"] == "imperial" else 1)
        strengthexcercises["reps"] = pandas.to_numeric(strengthexcercises["reps"], errors="coerce")* (2.2046226218 if self.devicedata["measurement"] == "imperial" else 1)
        strengthexcercises["sets"] = pandas.to_numeric(strengthexcercises["sets"], errors="coerce")* (2.2046226218 if self.devicedata["measurement"] == "imperial" else 1)
        cardioexcercises = self.workoutdata.loc[self.workoutdata["excercise"].isin(self.cardioexcercises), ["excercise","datetime", "weight","reps","sets"]].copy()
        cardioexcercises["sets"] = pandas.to_numeric(cardioexcercises["sets"], errors="coerce")* (0.62137119 if self.devicedata["measurement"] == "imperial" else 1)
        # Calculate the "volume" column
        strengthexcercises["volume"] = strengthexcercises["weight"] * strengthexcercises["reps"] * strengthexcercises["sets"]

        #volume = list(map((lambda weight,reps,sets : int(weight) * int(reps) * int(sets)), strengthexcercises["weight"],strengthexcercises["reps"],strengthexcercises["sets"]))
        
        # Convert "reps" to timedelta objects representing time duration
        cardioexcercises["time"] = cardioexcercises.apply(
            lambda row: int(row["reps"].split(":")[0])*60 + int(row["reps"].split(":")[1]),
            axis=1
        )
        
        cardioexcercises["split"] = cardioexcercises.apply(
            lambda row: row["time"] / row["sets"],
            axis=1
    )
        strengthexcercises["volume"] = pandas.to_numeric(strengthexcercises["weight"], errors="coerce") * \
                                       pandas.to_numeric(strengthexcercises["reps"], errors="coerce") * \
                                        pandas.to_numeric(strengthexcercises["sets"], errors="coerce")
        hasText = excercisename != ""
        print("hastext", hasText, excercisename)
        getExcerciseColumn = lambda category, column: category.loc[category["excercise"]==excercisename, column]
        match excercisetype:
            case "Weight":
                yaxislabel = f'{excercisetype} Lifted ({"lbs" if self.devicedata["measurement"] == "imperial" else "kgs"})'
                data = (getExcerciseColumn(strengthexcercises,"datetime"),getExcerciseColumn(strengthexcercises,"weight")) if hasText else (strengthexcercises["datetime"],strengthexcercises["weight"])
            case "Volume":
                yaxislabel = f'{excercisetype} Lifted ({"lbs" if self.devicedata["measurement"] == "imperial" else "kgs"})'
                #volume = list(map((lambda weight,reps,sets : int(weight) * int(reps) * int(sets)), strengthexcercises["weight"],strengthexcercises["reps"],strengthexcercises["sets"]))
                data = (getExcerciseColumn(strengthexcercises, "datetime"),getExcerciseColumn(strengthexcercises, "volume")) if hasText else (strengthexcercises["datetime"],strengthexcercises["volume"])
            case "Speed":
                yaxislabel = f'Time (min) per ({"mile" if self.devicedata["measurement"] == "imperial" else "km"})'
                data = (getExcerciseColumn(cardioexcercises, "datetime"),getExcerciseColumn(cardioexcercises, "split")) if hasText else (cardioexcercises["datetime"],cardioexcercises["split"])

            case "Distance":
                yaxislabel = f'Distance ({"miles" if self.devicedata["measurement"] == "imperial" else "kilometers"})'
                data = (getExcerciseColumn(cardioexcercises, "datetime"),getExcerciseColumn(cardioexcercises, "sets")) if hasText else (cardioexcercises["datetime"],cardioexcercises["sets"])

            case "Time":
                yaxislabel = "Time spent (mins)"
                data = (getExcerciseColumn(cardioexcercises, "datetime"),getExcerciseColumn(cardioexcercises, "time")) if hasText else (cardioexcercises["datetime"],cardioexcercises["time"])

        print(data, len(data[0]))
        if len(data[0]) == 0 or len(data[1]) == 0:
            graph().generate_no_data()
        else:
            graph().generate(yaxislabel,data)
        
    def getWorkoutData(self):
        query = sqlalchemy.text("""SELECT  workouts.excercise, workouts.sets, workouts.reps, workouts.weight, workoutslink.datetime
                   FROM workouts
                   INNER JOIN workoutslink ON workoutslink.workoutID = workouts.workoutID
                   WHERE workoutslink.userID = %s;""" % self.userID)
        return pandas.read_sql(query, self.connection)
    
    def colourpicker(self, element):
        color = QColorDialog.getColor().name()
        style[element] = color
        stylesheet = sheettemplate
        for key,value in style.items():
            stylesheet = stylesheet.replace(key,value)
        app.setStyleSheet(stylesheet)
        jsonstyle = json.dumps(style)
        with open("styles/defaultstyle.json", "w") as jsonfile:
            jsonfile.write(jsonstyle)
    
    def resetcolors(self):
        style = defaultstyle
        stylesheet = sheettemplate
        for key,value in style.items():
            stylesheet = stylesheet.replace(key,value)
            
        app.setStyleSheet(stylesheet)
        jsonstyle = json.dumps(style)
        with open("styles/defaultstyle.json", "w") as jsonfile:
            jsonfile.write(jsonstyle)
    
    def submitonerep(self):
        weight,reps = int(self.widgets["weight"].text()), int(self.widgets["reps"].text())
        onerep = (weight/(1.0278-0.0278*reps) + weight*(1 + 0.0333 * reps) + (100*weight)/(101.3 - 2.67123 * reps))/3
        self.widgets["estimate"].setText(f"{onerep:.2f}")
        
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
    def changesystem(self):
        if self.devicedata["measurement"] == "metric":
            self.devicedata["measurement"] = "imperial"
        else:
            self.devicedata["measurement"]="metric"
        self.widgets["Metric System"].setText(f"Measurement: {self.devicedata['measurement']}")
        self.widgets["Metric System"].show()
        with open("./data/data.json","w") as f:
            json.dump(self.devicedata, f)
    
    def saveworkout(self):
        workoutID = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
        workoutlist = list(self.connection.execute(sqlalchemy.text("SELECT workoutID FROM workoutslink")))#
        print(workoutlist)
        while workoutID in workoutlist:
                workoutID = "".join(list(choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(9)))
        data = list(map(lambda i: [workoutID,i[0].text(),i[1].text(),i[2].text(),i[3].text()],self.widgets["workoutbox"].scrollwidglist[:-1]))
        print(data)
        filtereddata = list(filter(lambda x : all(i != "" and i != "Not selected" for i in x),data))
        print(self.excercises["excercise"])
        print("Wide-Grip Push-Up" in filtereddata)
        if filtereddata != data:
            self.widgets["saveworkout"].notice(0.5, "Remove Empty Rows", "Save Workout") 
        else:
            if self.devicedata["measurement"] != "metric":
                print("eyup")
                data = map(lambda x:[x[0],x[1],x[2],x[3],round((float(x[4])*0.453592),2)], data)
            
            self.connection.execute(sqlalchemy.text("INSERT INTO workoutslink (workoutID,userID) VALUE ('%s','%s')" % (workoutID,self.userID)))
            
            print(workoutID)
            workoutdata = pandas.DataFrame(data,columns=["workoutID","excercise","sets","reps","weight"])
            workoutdata.to_sql(name="workouts",con=self.connection,if_exists="append",index=False)
            self.connection.commit()
            
            self.widgets["saveworkout"].notice(0.5, "Workout Saved", "Save Workout")
            self.widgets["saveworkout"].worker.finished.connect(self.addworkoutscreen)
            
    def units_check(self, row):
        workoutrow = lambda: self.widgets["workoutbox"].scrollwidglist[row]
        if workoutrow()[0].text() in ["Run","Rowing Erg"]:
            workoutrow()[1].setPlaceholderText("Distance")
            workoutrow()[2].setPlaceholderText("HH:MM")
            workoutrow()[2].focusInSignal.connect(lambda: workoutrow()[2].setInputMask("00:00"))
            workoutrow()[2].focusOutSignal.connect(lambda: workoutrow()[2].setInputMask("") if workoutrow()[2].text() in ["",":"] else None)
            workoutrow()[3].setText("N/A")
            workoutrow()[3].hide()
        else:
            workoutrow()[1].setPlaceholderText("Sets")
            workoutrow()[2].setPlaceholderText("Reps")
            workoutrow()[3].setText("")
            workoutrow()[3].show()
            
    def addrow(self):
        self.rowID += 1
        index = len(self.widgets["workoutbox"].scrollwidglist)-1
        scrollbox = lambda: self.widgets["workoutbox"]
        scrollbox().scrollwidglist.insert(index,[   LineEdit(self,"Excercise",None),
                                                    LineEdit(self,"Sets",None,(65,50)),
                                                    LineEdit(self,"Reps",None,(65,50)),
                                                    LineEdit(self,"+kgs" if self.devicedata["measurement"] == "metric" else "+lbs",None,(80,50)),
                                                    Button(self,"Delete",None,(100,50),partial(self.deleterow,self.rowID)),
                                                    self.rowID
                                                    ])
        scrollbox().scrollwidglist[index][0].textChanged.connect(lambda :self.units_check(index))
        completer = QCompleter(self.excercises["excercise"])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        scrollbox().scrollwidglist[index][0].setCompleter(completer)
        for i in range(1,4):
            scrollbox().scrollwidglist[index][i].setValidator(QIntValidator())

        
        scrollbox().scrollwidglist[index][3].setStyleSheet("QPushButton:hover{border: 4px solid red}")
        scrollbox().layout.removeWidget(scrollbox().scrollwidglist[-1][0])
        scrollbox().layout.addWidget(scrollbox().scrollwidglist[index][0],index,0,1,2)
        scrollbox().layout.addWidget(scrollbox().scrollwidglist[index][1],index,2)
        for i in range(3,6):
            scrollbox().layout.addWidget(scrollbox().scrollwidglist[index][i-1],index,i)
        scrollbox().layout.addWidget(scrollbox().scrollwidglist[-1][0],index+1,1)
        
    def deleterow(self,row):
        widglist = lambda : self.widgets["workoutbox"].scrollwidglist
        for i in widglist()[:-1]:
            if i[5] == row:
                for j in i[:-1]:
                    self.widgets["workoutbox"].layout.removeWidget(j)
                widglist().remove(i)
        
        map(lambda i,v: widglist()[i][4].clicked.connect(partial(self.deleterow,i)) if len(v) == 5 else None, enumerate(widglist()))

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
                self.connection.execute(sqlalchemy.text("INSERT INTO users (username,password) VALUES ('%s','%s')" % (username,password) ))
                self.username = username
                self.widgets["submit"].notice(0.5,"User created","Submit")
                self.connection.commit()
                self.usernames.append(username)
                self.loginscreen()
                self.widgets["username"].setText(self.username)

    def showpassword(self):
        self.showpass = not self.showpass
        if self.showpass:
            self.widgets["password"].setEchoMode(QLineEdit.Normal)
            self.widgets["showpassword"].setText("Hide")
        else:
            self.widgets["password"].setEchoMode(QLineEdit.Password)
            self.widgets["showpassword"].setText("Show")
    
    def logout(self):
        self.connection.execute(sqlalchemy.text("DELETE FROM deviceToUser WHERE deviceID = '%s'" % self.devicedata['deviceid']))
        self.startscreen()
        
    def closeEvent(self, event):
        self.connection.commit()
        super(QMainWindow, self).closeEvent(event)
    
        
    #endregion BUTTONFUNCTIONS ------------------------------

defaultstyle = {
    "primcol" : "#3D3D3D",
    "seccol" : "#F76D57",
    "accent" : "#2A363B",
    "bgcol" : "#1E1E1E",
    "textcol" : "white",
}

if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
     # initializes the window by instantiating the screen class
    with open("./styles/style.css", "r") as file:
        stylesheet = str(file.read())
    with open("./styles/defaultstyle.json","r") as file:
        style = json.load(file)

    sheettemplate = stylesheet
    
    for key, value in style.items():
        stylesheet = stylesheet.replace(key, value)
    app.setStyleSheet(stylesheet)
    window = Screen()
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the progr