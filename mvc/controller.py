from model import MyModel
from view import MyView
import ctypes 
import os 

# gpio_dma.so loaded to the python file 
# C functions can be accessed 

#low_level_driver = ctypes.CDLL(os.path.abspath('../lib/gpio_driver.so'))
  
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
        #self.view.setLabel_text('>')
    #event handlers
    def salirButtonPressed(self):
        self.parent.destroy()
    def calcularButtonPressed(self):
        key = self.view.getEntry_text_key()
        msg =  self.view.getEntry_text_msg()
        self.model.clearList()
        if len(key):
            self.model.addToList(key[0])
        if len(msg):
            self.model.addToList(msg)
        if (len(key) and len(msg)):
            self.view.setLabel_text(self.getCipherText(self.model.getList()))
    def listChangedDelegate(self):
        #model internally chages and needs to signal a change
        print(self.model.getList())
    def getCipherText(self, in_list):
        key = in_list[0]
        msg = in_list[1]
        values = []
        print("Key = ", key)
        for x in msg:
            print("In: ", x)
            values.append(chr(ord(key) ^ ord(x)))
        print(values)
        return ''.join(values)
