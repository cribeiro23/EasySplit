# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 01/09/2017
#
# Function to handle perform all final calculations of program and
# display the results

from PersonClass import Person
from ProductClass import Product
from convertPrice import convertPrice
import tkinter
from tkinter import messagebox

def finalize(person_list, product_list):
    # Looping through all the products in the list and
    # calculating price-per-person of each
    for product in product_list:
        convertPrice(product)
        product.costPerPerson()

    # Looping through all the people in the list and
    # calculating each person's final amount
    for person in person_list:
        person.calculatePriceToPay()

    # Displaying final results
    for person in person_list:
        messagebox.showinfo(person.name + "'s total", person.displayCost())
        
