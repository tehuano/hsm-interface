from Tkinter import *

#View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
 
class MyView(Frame):
    def loadView(self):
        welcome = Label(self.frame, text="XOR Cipher Interface")
        welcome.config(font=('Arial', 12))
        welcome.grid(row=0, padx = 30, pady = 5, columnspan = 3)
        label_llave = Label(self.frame,textvariable = self.label_text_llave).grid(row = 1, padx = 10, sticky = W)
        label_mensaje = Label(self.frame,textvariable = self.label_text_mensaje).grid(row = 2, padx = 10, sticky = W)
        entry_llave = Entry(self.frame,textvariable = self.entry_text_llave).grid(row = 1,column = 1, columnspan = 4, sticky = W)
        entry_mensaje = Entry(self.frame,textvariable = self.entry_text_mensaje).grid(row = 2, column = 1, columnspan = 4, sticky = W)
        quitButton = Button(self.frame,text = 'Salir', command= self.vc.salirButtonPressed, highlightbackground='#3E4149').grid(row = 3, column = 2, pady = 5)
        addButton = Button(self.frame,text = "Calcular", command = self.vc.calcularButtonPressed, highlightbackground='#3E4149').grid(row = 3, column = 1, pady = 5)
        label_resultado = Label(self.frame,textvariable = self.label_text_resultado).grid(row = 4, padx = 10, pady = 10, columnspan = 4, sticky = W)

    def __init__(self,vc):
        vc.parent.geometry("300x150+150+200")
        self.frame=Frame()
        self.frame.grid(row = 0,column=1)
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
 

 
