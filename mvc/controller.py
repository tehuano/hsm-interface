from model import MyModel
from view import MyView
import ctypes 
import os 
import time

# gpio_dma.so loaded to the python file 
# C functions can be accessed 

low_level_driver = ctypes.CDLL(os.path.abspath('../lib/gpio_driver.so'))
low_level_driver.get_byte.restype = ctypes.c_ubyte
#fun.get_byte.argtypes = [None]
low_level_driver.send_key_byte.argtypes = [ctypes.c_ubyte]
low_level_driver.send_data_byte.argtypes = [ctypes.c_ubyte]
returnVale = low_level_driver.init()
low_level_driver.set_debug_flag(0x00)
  
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
        print("Key = ", key, ord(key))
        start = time.time()
        vs = []
        for x in msg:
            vs.append(ord(x))
        print(vs)
        vv = []
        low_level_driver.send_key_byte(ord(key))
        for x in msg:
            time.sleep(0.01)
            low_level_driver.send_data_byte(ord(x))
            time.sleep(0.01)
            v = low_level_driver.get_byte()
            val = unichr(v)
            values.append(val)
            vv.append(v)
        print("Transaction finished. Time = ", time.time()-start)
        print(values)
        print(vv)
        return ''.join(values)
