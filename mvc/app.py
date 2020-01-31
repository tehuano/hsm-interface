#! /usr/bin/python

from Tkinter import *
from controller import MyController

def main():
    root = Tk()
    frame = Frame(root,bg='#0555ff' )
    root.title('HSM')
    app = MyController(root)
    root.mainloop() 
 
if __name__ == '__main__':
    main() 
