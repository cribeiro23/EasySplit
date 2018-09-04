# Author: Carlos Eduardo Matos Ribeiro
# Version: 1.0
# Last edited: 28/08/2017
#
# Function to parse text version of check and separate values and prices

def parseCheck(checkText):

    # Splitting input into multiple lines
    checkText = checkText.splitlines()
    
    # Initializing variables to ensure parsing was successful
    productCount = 0
    priceCount = 0

    # Initializing empty lists
    productList = []
    priceList = []

    for line in checkText:
        # Checking whether the line has a $ marker to
        # determine whether it is a product or a value
        if '$' in line:
            # Adding item to correct list and updating counter
            priceCount += 1
            priceList.append(line)
        else:
            #Adding item to correct list and updating counter
            productCount += 1
            productList.append(line)

    # Checking counters to ensure successful parsing

    
    if productCount != priceCount:
        # Printing error message in case of insucessful parsing
        print("An error has occured parsing the values")
        # Quitting program in case of error
        quit()
    
    else:
        # If successful, merge each list into a dictionary
        price_value_dict = dict(zip(productList,priceList))
        return price_value_dict
