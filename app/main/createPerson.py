# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 30/08/2017
#
# Function to handle GUI functionality of creating a new person object

import tkinter
from tkinter import *
from PersonClass import Person

def createPerson(person_list):
    root = Tk()

    # Creating frame to hold label and entry
    topFrame = Frame(root)
    topFrame.pack()
    
    # Creating label to explain function of entry
    label = Label(topFrame, text = "Enter name")
    label.pack( side = LEFT )

    # Creating entry
    entry = Entry(topFrame)
    entry.pack( side = LEFT)

    # Creating frame to hold button
    bottomFrame = Frame(root)
    bottomFrame.pack()

    # Function to define button functionality, create Person
    # with name in entry
    def nextPressed():
        person = Person(entry.get())
        person_list.append(person)
        # Closing this window
        root.destroy()
    
    # Creating button to finalize entry
    nextButton = tkinter.Button( bottomFrame, text = "Next Person",
                                 command = nextPressed)
    nextButton.pack(side = LEFT)

    root.mainloop()

