from model import MyModel
from view import MyView

#Controller: Ties View and Model together.
#       --Performs actions based on View events.
#       --Sends messages to Model and View and gets responses
#       --Has Delegates
 
class MyController():
    def __init__(self,parent):
        self.parent = parent
        self.model = MyModel(self)    # initializes the model
        self.view = MyView(self)  #initializes the view
        #initialize objects in view
        self.view.setEntry_text('Data') #a non cheat way to do MVC wiht tkinter control variables
        self.view.setLabel_text('Ready')
 #event handlers
    def quitButtonPressed(self):
        self.parent.destroy()
    def addButtonPressed(self):
        self.view.setLabel_text(self.view.entry_text.get())
        self.model.addToList(self.view.entry_text.get())
    def listChangedDelegate(self):
        #model internally chages and needs to signal a change
        print(self.model.getList())
 
