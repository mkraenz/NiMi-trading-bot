from InvestopediaApi.ita import Account, Action
from broker.config import COMMISION_FEE
from broker.i_broker import IBroker
from broker.stock import Stock


class AdapterInvestopediaApiToIBroker(IBroker):

    def bid(self, symbol, amount):
        return self.broker.trade(symbol, Action.buy, amount)

    def ask(self, symbol, amount):
        return self.broker.trade(symbol, Action.sell, amount)

    def fee(self):
        return COMMISION_FEE

    def stocks(self):
        bought = self.broker.get_current_securities().bought
        return [self.__createStock(stock) for stock in bought]

    def cash(self):
        return self.broker.get_portfolio_status().cash

    def login(self, username, password):
        self.broker = Account(username, password)
        if not self.broker.logged_in: raise Exception('Login failed.')

    def __createStock(self, security):
        return Stock(security.symbol,
                     security.description,
                     security.quantity,
                     security.purchase_price,
                     )

    def getQuantity(self, symbol):
        filtered_stock = [stock for stock in self.stocks() if stock.symbol == symbol]
        return 0 if not filtered_stock else filtered_stock[0].quantity
