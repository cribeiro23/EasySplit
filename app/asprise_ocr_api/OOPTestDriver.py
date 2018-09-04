# Driver to test OOP functionality of application before
# GUI part is complete

from ProductClass import Product
from PersonClass import Person

Person1 = Person("Cadu")
Person2 = Person("Mari")

Product1 = Product("Coca-Cola", 6)
Product2 = Product("Ice-Tea", 7)
Product3 = Product("Rodizio", 178)

Person1.addProduct(Product1)
Person2.addProduct(Product2)
Person1.addProduct(Product3)
Person2.addProduct(Product3)

Product.tip = 20

Product1.costPerPerson()
Product2.costPerPerson()
Product3.costPerPerson()

Person1.calculatePriceToPay()
Person2.calculatePriceToPay()

Person1.displayCost()
Person2.displayCost()
