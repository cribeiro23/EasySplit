# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 05/09/2017

# Function to handle bulk of GUI functionality of check_application

from tkinter import *
from PersonClass import Person
from ProductClass import Product
import tkinter

def handleGUI(product_list, person):
    root = Tk()

    # Adding appropriate heading to window
    root.wm_title(person.name)

    # Creating frame to enter tip
    frame = Frame(root)
    frame.pack()
    
    # Entering field to select tip percentage
    # TODO: Remove this and put elsewhere
    tipLabel = Label(frame, text = "Enter tip")
    tipLabel.pack( side = LEFT)
    tipEntry = Entry(frame)
    tipEntry.pack( side = RIGHT)
    
    # Looping through items and creating GUI components for each item
    for product in product_list:
        # Creating a frame for each product/price pair
        frame = Frame(root)
        frame.pack()
        
        # Creating label for the product
        product_var = StringVar()
        product_label = Label( frame, textvariable=product_var, relief=RAISED )
        product_var.set(product.name)
        # Positioning label
        product_label.pack( side = LEFT )

        # Creating label for the price
        price_var = StringVar()
        price_label = Label( frame, textvariable=price_var, relief=RAISED)
        price_var.set(product.price)
        # Positioning label
        price_label.pack(side = LEFT)

        # Creating check button variable
        buttonVar = IntVar()

        # Adding functionality to checkButton
        def buttonChecked(product, var):
            # Determining which action to perform depending on state
            # of checked box
            if var.get():
                person.addProduct(product)
            else:
                person.removeProduct(product)
                
        # Initializing empty button list
        consumedButtonList = []
        i = 0

        # Creating and positioning check button
        consumedButtonList.append(None)   
        consumedButtonList[i] = Checkbutton(frame, variable = buttonVar,
                                            command = lambda product=product,
                                            buttonVar=buttonVar :
                                            buttonChecked(product, buttonVar))
        consumedButtonList[i].pack( side = LEFT)

        i += 1

    # Adding next button functionality
    def nextPressed():
        # Closing window to move to next person
        root.destroy()
  
    # Creating new frame to keep button
    frame = Frame(root)
    frame.pack()
    
    # Creating next button 
    nextButton = tkinter.Button( frame, text = "Next person",
                                 command = nextPressed)
    nextButton.pack()
    root.mainloop()
