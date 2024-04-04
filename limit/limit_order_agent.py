from trading_framework.execution_client import ExecutionClient,ExecutionException
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        # self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy_flag, product_id, amount, limit):
        order = {
            'buy_flag': buy_flag,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self):
        self.product_id = input("Enter the product id : ")
        self.price = int(input("Enter the price : "))
        print("Current market price of the Product {0} : Price {1}".format(self.product_id, self.price))
        return self.product_id,self.price

    def buy(self,product_id,amount):
        print("Executing buy order of Product {0} for the amount : {1}".format(product_id,amount))

    def sell(self,product_id,amount):
        print("Executing sell order of Product {0} for the amount : {1}".format(product_id, amount))

    def execute_order(self):
        self.product_id, self.price = self.on_price_tick()
        for order in self.orders:

            if (order['buy_flag'] and order['product_id'] == self.product_id and self.price < order['limit']):
                self.buy(order['product_id'],order['amount'])
                order['execution_flag'] = True
            elif not order['buy_flag'] and order['product_id'] == self.product_id and self.price > order['limit']:
                self.sell(order['product_id'],order['amount'])
                order['execution_flag'] = True

        # remove the added orders after they have been executed for either buy or sell
        self.orders = [item for item in self.orders if not item.get('execution_flag')]

        self.unexecuted_orders()

    #retrying unexecuted orders needs to be added so that whenever the market price condition is satisfied it should be executed immediately afterwards
    def unexecuted_orders(self):
        """
        retrying unexecuted orders needs to be added so that whenever the market price condition is satisfied it should be executed immediately afterwards
        """
        while self.orders:
            self.execute_order()
