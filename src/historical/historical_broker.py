from broker.i_broker import IBroker
from historical.config import INITIAL_CASH, COMMISION_FEE
from broker.stock import Stock


class HistoricalBroker(IBroker):
    
    __stocks = []
    __cash = INITIAL_CASH

    def __init__(self, iHistoricalMarketData):
        self.__md = iHistoricalMarketData

    def bid(self, symbol, amount):
        price = self.__md.priceWithoutTimeChange(symbol)
        if amount * price + 2 * self.fee() <= self.cash():
            stock = Stock(
                symbol=symbol,
                name='stockname',
                quantity=amount,
                purchase_price=price,
            )
            self.__cash -= amount * price + self.fee()
            self.__stocks.append(stock)  # TODO: implement case for existing stock
            return True
        else:
            return False

    def ask(self, symbol, amount):
        # TODO: search stocksymbol in self.stocks()
        if amount <= self.stocks()[0].quantity:
            price = self.__md.priceWithoutTimeChange(symbol)
            stock = self.stocks()[0]  # TODO: check for existence
            self.__cash += amount * price - self.fee()
            stock.quantity -= amount
            if not stock.quantity:
                self.__stocks.remove(stock)
            return True
        else:
            return False
    
    def fee(self):
        return COMMISION_FEE

    def stocks(self):
        return self.__stocks

    def cash(self):
        return self.__cash
    
    def login(self):
        return True

    def getQuantity(self, symbol):
        filtered_stock = [stock for stock in self.stocks() if stock.symbol == symbol]
        return 0 if not filtered_stock else filtered_stock[0].quantity
        