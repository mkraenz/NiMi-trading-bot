from broker.i_broker import IBroker
from InvestopediaApi.ita import Account, Action
from broker.stock import Stock
from broker.config import COMMISION_FEE


class AdapterInvestopediaApiToIBroker(IBroker):
    
    def bid(self, symbol, amount):
        return self.client.trade(symbol, Action.buy, amount)
    
    def ask(self, symbol, amount):
        return self.client.trade(symbol, Action.sell, amount)
    
    def fee(self):
        return COMMISION_FEE

    def current_stocks(self):
        bought = self.client.get_current_securities().bought
        return [self.__createStock(stock) for stock in bought]
        
    def cash(self):
        return self.client.get_portfolio_status().cash
    
    def login(self, username, password):
        self.client = Account(username, password)
        if not self.client.logged_in: raise Exception('Login failed.')
    
    def __createStock(self, security):
        return Stock(
            symbol=security.symbol,
            name=security.description,
            quantity=security.quantity,
            purchase_price=security.purchase_price,
        )
        
