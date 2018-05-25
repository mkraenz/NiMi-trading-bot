'''
Created on 11.05.2018

@author: Mirco
'''
import unittest
from test_investopedia_trading_api.config import TEST_PASSWORD, TEST_USERNAME
from InvestopediaApi.ita import Action, get_quote, Account


class TestInvestopediaApi(unittest.TestCase):
    
    SYMBOL = "NVCN"
    PASSWORD = TEST_PASSWORD
    USERNAME = TEST_USERNAME
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.client = Account(self.USERNAME, self.PASSWORD)

    def test_login(self):
        client = Account(self.USERNAME, self.PASSWORD)
        self.assertTrue(client.logged_in)

    def test_buy(self):
        self.assertTrue(self.client.trade(self.SYMBOL, Action.buy, 1))

    def test_sell(self):
        portfolio = self.client.get_current_securities()
        for bought in portfolio.bought:
            if bought.symbol == self.SYMBOL:
                self.assertTrue(self.client.trade(self.SYMBOL, Action.sell, 1))
                return
        self.assertTrue(False,
                            'Possesses no stock to test TestInvestopediaApi.test_sell(). Buy some manually.')

    def test_get_current_securities(self):
        self.assertTrue(self.client.get_current_securities())
        
    def test_get_quote(self):
        self.assertTrue(get_quote(self.SYMBOL))


if __name__ == "__main__":
    unittest.main()
