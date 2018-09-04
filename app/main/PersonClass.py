# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last Edited: 05/09/2017
#
# Person class to define person objects, that have a name,
# list of products consumed and final price to pay

import ProductClass

class Person:

    # Constructor to initialize person's name. Product list
    # starts empty and price to pay starts at 0
    def __init__(self, name):
        self.name = name
        self.price_to_pay = 0
        self.product_list = []

    # Method to add a product to person's list
    def addProduct(self, product):
        self.product_list.append(product)
        product.incCustomer()

    # Method to remove a product from a person's list
    def removeProduct(self, product):
        self.product_list.remove(product)
        product.decCustomer()

    # Method to calculate person's price_to_pay
    def calculatePriceToPay(self):
        # Adding value of each product
        for product in self.product_list:
            self.price_to_pay += product.cost_per_person
        # Rouding to two decimal places
        self.price_to_pay = float("{0:.2f}".format(self.price_to_pay))

    # Method to display final cost
    def displayCost(self):
        return (self.name + " has to pay $" + str(self.price_to_pay))

    
