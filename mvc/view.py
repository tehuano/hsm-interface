from Tkinter import *

#View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
 
class MyView(Frame):
    def loadView(self):
        label_llave = Label(self.frame,textvariable = self.label_text_llave).grid(row = 1,
            column = 0, columnspan = 3, sticky = EW)
        label_mensaje = Label(self.frame,textvariable = self.label_text_mensaje).grid(row = 2,
            column = 0, columnspan = 3, sticky = EW)
        entry_llave = Entry(self.frame,textvariable = self.entry_text_llave).grid(row = 1,
            column = 1, columnspan = 3, sticky = EW)
        entry_mensaje = Entry(self.frame,textvariable = self.entry_text_mensaje).grid(row = 2,
            column = 1, columnspan = 3, sticky = EW)
        label_resultado = Label(self.frame,textvariable = self.label_text_resultado).grid(row = 4,
            column = 0, columnspan = 4, sticky = EW)
        quitButton = Button(self.frame,text = 'Salir', 
            command= self.vc.salirButtonPressed).grid(row = 3,column = 0)
        addButton = Button(self.frame,text = "Calcular",
            command = self.vc.calcularButtonPressed).grid(row = 3, column = 2)
    def __init__(self,vc):
        vc.parent.geometry("500x200+200+200")
        self.frame=Frame()
        self.frame.grid(row = 0,column=1)
        welcome = Label(self.frame, text="HSM Interface")
        welcome.config(font=('Arial', 14))
        welcome.grid(row=0, column=1)
        self.vc = vc
        self.entry_text_llave = StringVar()
        self.entry_text_llave.set('')
        self.entry_text_mensaje = StringVar()
        self.entry_text_mensaje.set('')
        self.label_text_llave = StringVar()
        self.label_text_llave.set('LLave(hex)')
        self.label_text_mensaje = StringVar()
        self.label_text_mensaje.set('Mensaje(hex)')
        self.label_text_resultado = StringVar()
        self.label_text_resultado.set('')
        self.loadView()
    def getEntry_text(self):
    #returns a string of the entry text
        return self.entry_text_mensaje.get()
    def setEntry_text(self,text):
    #sets the entry text given a string
        self.entry_text_mensaje.set(text)
    def getLabel_text(self):
    #returns a string of the Label text
        return self.label_text_resultado.get()
    def setLabel_text(self,text):
    #sets the label text given a string
        self.label_text_resultado.set(text)
 

 
