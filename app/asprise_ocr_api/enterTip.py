# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 05/09/2017
#
# Function to handle GUI functionality of entering the tip

import tkinter
from tkinter import *
from ProductClass import Product

def enterTip():
    root = Tk()

    # Creating frame to hold label and entry
    topFrame = Frame(root)
    topFrame.pack()
    
    # Creating label to explain function of entry
    label = Label(topFrame, text = "Enter tip")
    label.pack( side = LEFT )

    # Creating entry
    entry = Entry(topFrame)
    entry.pack( side = LEFT)

    # Creating frame to hold button
    bottomFrame = Frame(root)
    bottomFrame.pack()

    # Function to define button functionality, get tip
    # from entry
    def nextPressed():
        Product.tip = float(entry.get())
        # Closing this window
        root.destroy()
    
    # Creating button to finalize entry
    nextButton = tkinter.Button( bottomFrame, text = "Continue",
                                 command = nextPressed)
    nextButton.pack(side = LEFT)

    root.mainloop()


