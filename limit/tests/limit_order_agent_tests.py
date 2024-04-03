import unittest
from unittest.mock import patch, MagicMock
from limit.limit_order_agent import LimitOrderAgent
class LimitOrderAgentTest(unittest.TestCase):

    # def test_something(self):
    #     self.fail("not implemented")

    @patch('builtins.input', side_effect=["IBM", "100"])
    def test_on_price_tick(self, mock_input):
        agent = LimitOrderAgent(None)
        product_id, price = agent.on_price_tick()
        self.assertEqual(product_id, "IBM")
        self.assertEqual(price, 100)

    def test_add_order(self):
        agent = LimitOrderAgent(None)
        agent.add_order(True, "ABC", 100, 50)
        self.assertEqual(len(agent.orders), 1)
        self.assertEqual(agent.orders[0]['buy_flag'], True)
        self.assertEqual(agent.orders[0]['product_id'], "ABC")
        self.assertEqual(agent.orders[0]['amount'], 100)
        self.assertEqual(agent.orders[0]['limit'], 50)

    def test_buy(self):
        agent = LimitOrderAgent(None)
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            agent.buy("XYZ", 200)
            self.assertEqual(mock_stdout.getvalue().strip(), "Executing buy order of Product XYZ for the amount : 200")

    def test_sell(self):
        agent = LimitOrderAgent(None)
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            agent.sell("XYZ", 200)
            self.assertEqual(mock_stdout.getvalue().strip(), "Executing sell order of Product XYZ for the amount : 200")

    def test_execute_order_buy(self):
        agent = LimitOrderAgent(None)
        agent.add_order(True, "XYZ", 100, 150)
        with patch.object(agent, 'on_price_tick', return_value=("XYZ", 100)):
            with patch.object(agent, 'buy') as mock_buy:
                agent.execute_order()
                mock_buy.assert_called_once_with("XYZ", 100)
        self.assertEqual(len(agent.orders), 0)

    def test_execute_order_sell(self):
        agent = LimitOrderAgent(None)
        agent.add_order(False, "XYZ", 100, 50)
        with patch.object(agent, 'on_price_tick', return_value=("XYZ", 100)):
            with patch.object(agent, 'sell') as mock_sell:
                agent.execute_order()
                mock_sell.assert_called_once_with("XYZ", 100)
        self.assertEqual(len(agent.orders), 0)

    def test_unexecuted_orders(self):
        agent = LimitOrderAgent(None)
        agent.add_order(True, "XYZ", 100, 150)
        agent.add_order(False, "ABC", 200, 50)
        with patch.object(agent, 'on_price_tick', return_value=("XYZ", 100)):
            with patch.object(agent, 'buy'):
                agent.execute_order()
        with patch.object(agent, 'on_price_tick', return_value=("ABC", 100)):
            with patch.object(agent, 'sell'):
                agent.execute_order()
        self.assertEqual(len(agent.orders), 0)


if __name__ == '__main__':
    unittest.main()