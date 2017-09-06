# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last Edited: 04/09/2017
#
# Product class to define product objects, that have an associated cost,
# name and number of customers

PERCENTAGE_CALCULATOR = 100

class Product:
    # Static (in java sense) variable tip
    tip = 10

    # Constructor to initialize product's name and cost
    # and start customer count at 0
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.customer_count = 0
        self.cost_per_person = 0

    # Method to increment customer count
    def incCustomer(self):
        self.customer_count += 1

    # Method to decrement customer count
    def decCustomer(self):
        self.customer_count -= 1

    # Method to compare Product objects
    def equals(self, product):
        if self.name == product.name and self.price == product.price:
            return true
        else:
            return false
        


    # Method to calculate cost per person that consumed the product
    def costPerPerson(self):
        totalCost = self.price * (1 + (Product.tip/PERCENTAGE_CALCULATOR))
        self.cost_per_person = totalCost / self.customer_count

        
    
