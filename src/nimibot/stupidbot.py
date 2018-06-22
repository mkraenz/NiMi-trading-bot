from InvestopediaApi.ita import Account, Action, get_quote
import time
import os
import math
from nimibot.config import PASSWORD, USERNAME
from datetime import datetime


class StupidBot(object):
    
    LOG_LEVEL = 5
    SYMBOL = 'GOOGL'
    UPDATE_INTERVAL = 5  # Investopedia updates prices etc every 60 to 80 seconds
    ROI = 1.00005
    AMOUNT = 50
    COMMISION_FEE = 0.0  # determined by broker
    LOG_FILENAME = 'log_stupid_bot.txt'

    def __init__(self, client):
        self.client = client
        self.purchase_price = 0
        filename = os.path.join(os.getcwd(), self.LOG_FILENAME)
        self.f = open(filename, 'a', 1)

    def wait_till_bought(self, client):
        start_time = time.time()
        self.log('wait_till_bought()')

        while True:
            portfolio = client.get_current_securities()
            for stock in portfolio.bought:
                if stock.symbol == self.SYMBOL:
                    self.purchase_price = stock.purchase_price
                    return
            if self.LOG_LEVEL: self.log_waited_minutes(start_time)
            time.sleep(self.UPDATE_INTERVAL)

    def current_revenue(self):
        return get_quote(self.SYMBOL) * self.AMOUNT - self.COMMISION_FEE

    def total_costs(self):
        return self.purchase_price * self.AMOUNT + self.COMMISION_FEE

    def wait_till_ask(self):
        start_time = time.time()
        self.log('wait_till_ask()')
        while self.current_revenue() / self.total_costs() < self.ROI:
            if self.LOG_LEVEL: 
                self.log_waited_minutes(start_time)
                self.log('current price', get_quote(self.SYMBOL))
                self.log('current ROI', self.current_revenue() / self.total_costs())
            time.sleep(self.UPDATE_INTERVAL)
            if (time.time() - start_time) / 60 > 60:  # TODO: remove timeout after 60 min
                return

    def is_not_stock_yet_sold(self, client):
        return self.SYMBOL in [s.symbol for s in client.get_current_securities().bought]

    def wait_till_sold(self, client):
        start_time = time.time()
        self.log('wait_till_sold()')
        while self.is_not_stock_yet_sold(client):
            if self.LOG_LEVEL: 
                self.log_waited_minutes(start_time)
            time.sleep(self.UPDATE_INTERVAL)

    def log(self, name, value=''):
        self.f.writelines([name, ' = ', str(value), '\n'])
        print(name, ' = ', str(value))

    def log_profit(self, current_cash, cash_before_purchase):
        self.log('Profit', current_cash - cash_before_purchase)
        self.log('Cash after purchase', current_cash)
        self.log('Cash before purchase', cash_before_purchase)
    
    def log_after_wait_till_bought(self):
        self.log('purchase price', self.purchase_price)
        self.log('total costs', self.total_costs())

    def log_waited_minutes(self, start_time):
        self.log('waited minutes', (math.floor((time.time() - start_time) / 60 * 100) / 100))
    
    def run(self):
        if self.LOG_LEVEL: self.log('\n'*10 + '>>>>>>>>>>>>> %s .run() at time' % (self.__class__.__name__), str(datetime.now()))
        cash_before_purchase = self.client.get_portfolio_status().cash

        self.client.trade(self.SYMBOL, Action.buy, self.AMOUNT)
        if self.LOG_LEVEL: self.log('buy order sent')

        self.wait_till_bought(self.client)
        if self.LOG_LEVEL: self.log_after_wait_till_bought()
        
        self.wait_till_ask()
        self.client.trade(self.SYMBOL, Action.sell, self.AMOUNT)
        if self.LOG_LEVEL: self.log('sell order sent')
        
        self.wait_till_sold(self.client)
        if self.LOG_LEVEL: self.log_profit(self.client.get_portfolio_status().cash, cash_before_purchase)
        self.f.close()


if __name__ == '__main__':
    client = Account(USERNAME, PASSWORD)
    StupidBot(client).run()
