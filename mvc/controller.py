from model import MyModel
from view import MyView
import ctypes 
import os 

# gpio_dma.so loaded to the python file 
# C functions can be accessed 
low_level_driver = ctypes.CDLL(os.path.abspath('../lib/gpio_driver.so'))
  
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
        #a non cheat way to do MVC wiht tkinter control variables
        #self.view.setEntry_text('Data') 
        self.view.setLabel_text('Resultado')
     #event handlers
    def salirButtonPressed(self):
        self.parent.destroy()
    def calcularButtonPressed(self):
        self.view.setLabel_text(self.view.entry_text.get())
        low_level_driver.usage('test')
        self.model.clearList()
        self.model.addToList('msg')
        self.model.addToList('key')
    def listChangedDelegate(self):
        #model internally chages and needs to signal a change
        print(self.model.getList())
