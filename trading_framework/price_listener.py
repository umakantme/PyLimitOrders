from typing import Protocol


class PriceListener(Protocol):

    def __init__(self):
        pass

    def on_price_tick(self):
        """
        invoked on market data change
        :param product_id: id of the product that has a price change
        :param price: the current market price of hte product
        :return: None
        """
        self.product_id = input("Enter the product id : ")
        self.price = int(input("Enter the price : "))
        print("Current market price of the Product {0} : Price {1}".format(self.product_id, self.price))

        return self.product_id, self.price

