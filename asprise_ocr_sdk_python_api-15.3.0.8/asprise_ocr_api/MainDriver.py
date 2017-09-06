# Author: Carlos Eduardo Matos Ribeiro
# Version 1.0
# Last edited: 01/09/2017
#
# Main driver function of check_application program
#

# Importing necessary functions
from Python_Asprise_Test import doOcr
from parseCheck import parseCheck
from handleGUI import handleGUI
from ProductClass import Product
from PersonClass import Person
from createPerson import createPerson
from finalize import finalize
from enterTip import enterTip
from tkinter import *
import tkinter

#Performing ocr on desired check image
checkText = doOcr()

#Printing for testing purposes TODO: remove
print(checkText)

# Parsing result
price_value_dict = parseCheck(checkText)

#Creating empty list of products
product_list = []

# Looping through dictionary of prices and product names to
# populate the list of product objects
for product, price in price_value_dict.items():
    # Printing for testing purposes
    print(product,price)

    # Creating product objects from product names and prices
    DefProduct = Product(product, price)
    product_list.append(DefProduct)
    

# Requesting user for number of people to split check between
number_of_people = input("Insert number of people to split check: ")

#Initializing empty person list
person_list = []

# Creating the necessary number of people objects
for x in range(0, int(number_of_people)):
    createPerson(person_list)

# Prompting for the tip
enterTip()

# Generating a check window for each person created
for person in person_list:
    handleGUI(product_list, person)

# Finalizing program and displaying results
finalize(person_list,product_list)

# Continue application...


