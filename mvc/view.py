from Tkinter import *

#View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
 
class MyView(Frame):
    def loadView(self):
        quitButton = Button(self.frame,text = 'Salir', 
            command= self.vc.salirButtonPressed).grid(row = 3,column = 3)
        addButton = Button(self.frame,text = "Calcular",
            command = self.vc.calcularButtonPressed).grid(row = 3, column = 1)
        entry = Entry(self.frame,textvariable = self.entry_text).grid(row = 2,
            column = 1, columnspan = 3, sticky = EW)
        label = Label(self.frame,textvariable = self.label_text_msg).grid(row = 2,
            column = 0, columnspan = 3, sticky = EW)
        label = Label(self.frame,textvariable = self.label_text).grid(row = 5,
            column = 0, columnspan = 3, sticky = EW)
    def __init__(self,vc):
        vc.parent.geometry("500x200")
        self.frame=Frame()
        self.frame.grid(row = 0,column=0)
        self.vc = vc
        self.entry_text = StringVar()
        self.entry_text.set('nil')
        self.label_text = StringVar()
        self.label_text.set('nil')
        self.label_text_msg = StringVar()
        self.label_text_msg.set('nil')
        self.loadView()
    def getEntry_text(self):
    #returns a string of the entry text
        return self.entry_text.get()
    def setEntry_text(self,text):
    #sets the entry text given a string
        self.entry_text.set(text)
    def getLabel_text(self):
    #returns a string of the Label text
        return self.label_text.get()
    def setLabel_text(self,text):
    #sets the label text given a string
        self.label_text.set(text)
 

 
