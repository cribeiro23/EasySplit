# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 01/09/2017

# Function to convert price string (often containing multiple numbers and
# characters) of product objects into single int

from ProductClass import Product

def convertPrice(product):

    # Converting commas to decimal points if necessary
    product.price = product.price.replace(',','.')

    # Using index variable that starts from end of string
    i = -1
    
    # Starting infinite loop
    while True:
        # Checking to see if current pattern is a float
        try:
            float(product.price[i:])
            # If successful, decrement i and keep going
            i -= 1

        # If unsucessful, break from loop
        except:
            # Setting i back to last working state
            i += 1
            break

    # Converting price to final version
    product.price = float(product.price[i:])


