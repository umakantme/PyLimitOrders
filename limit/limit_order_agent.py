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

    def execute_order(self):

        self.product_id, self.price = PriceListener.on_price_tick(self)
        for order in self.orders:
            if (order['buy_flag'] and self.price < order['limit']):
                ExecutionClient.buy(self,order['product_id'],order['amount'])
                order['execution_flag'] = True
            elif not order['buy_flag'] and self.price > order['limit']:
                ExecutionClient.sell(self,order['product_id'],order['amount'])
                order['execution_flag'] = True

        # remove the added orders after they have been executed for either buy or sell
        self.orders = [item for item in self.orders if not item.get('execution_flag')]

    #retrying unexecuted orders needs to be added so that whenever the market price condition is satisfied it should be executed immediately afterwards
    def unexecuted_orders(self):
        if self.orders:
            self.execute_order()
        else:
            print("All orders executed successfully...")



if __name__ == "__main__":

    try:

        # execution_client = MockExecutionClient()
        agent = LimitOrderAgent(PriceListener)

        # Add buy order for 1000 shares of IBM at $100 limit
        agent.add_order(True, 'IBM', 1000, 100)

        # Add sell order for 1000 shares of IBM at $150 limit
        agent.add_order(False, 'IBM', 1000, 150)

        agent.execute_order()
        agent.unexecuted_orders()

    except ExecutionException as e:
        print("An error occurred:", e)
