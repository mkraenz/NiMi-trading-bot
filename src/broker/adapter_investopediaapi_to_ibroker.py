from broker.i_broker import IBroker
from InvestopediaApi.ita import Account, Action
from broker.stock import Stock
from broker.config import COMMISION_FEE


class AdapterInvestopediaApiToIBroker(IBroker):
    
    def bid(self, symbol, amount):
        return self.client.trade(symbol, Action.sell, amount)
    
    def ask(self, symbol, amount):
        return self.client.trade(symbol, Action.buy, amount)
    
    def fee(self, symbol):
        return COMMISION_FEE

    def current_stocks(self):
        bought = self.client.get_current_securities().bought
        return [self.__createStock(stock) for stock in bought]
        
    def cash(self):
        return self.client.get_portfolio_status().cash
    
    def login(self, username, password):
        self.client = Account(username, password)
        return self.client.logged_in
    
    def __createStock(self, security):
        return Stock(
            symbol=security.symbol,
            name=security.description,
            quantity=security.quantity,
            purchase_price=security.purchase_price,
            current_price=security.current_price
        )
        
