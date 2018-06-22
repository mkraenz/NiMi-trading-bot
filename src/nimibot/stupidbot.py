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
    LOG_FILENAME = 'log_stupid_bot.txt'

    def __init__(self, broker, market_data):
        self.client = broker
        self.market_data = market_data
        self.purchase_price = 0
        filename = os.path.join(os.getcwd(), self.LOG_FILENAME)
        self.f = open(filename, 'a', 1)

    def wait_till_bought(self, client):
        start_time = time.time()
        self.log('wait_till_bought()')

        while True:
            portfolio = client.stocks()
            for stock in portfolio:
                if stock.symbol == self.SYMBOL:
                    self.purchase_price = stock.purchase_price
                    return
            if self.LOG_LEVEL: self.log_waited_minutes(start_time)
            time.sleep(self.UPDATE_INTERVAL)

    def current_revenue(self):
        return self.market_data.price(self.SYMBOL) * self.AMOUNT - self.client.fee()

    def total_costs(self):
        return self.purchase_price * self.AMOUNT + self.client.fee()

    def wait_till_ask(self):
        start_time = time.time()
        self.log('wait_till_ask()')
        while self.current_revenue() / self.total_costs() < self.ROI:
            if self.LOG_LEVEL: 
                self.log_waited_minutes(start_time)
                self.log('current price', self.market_data.price(self.SYMBOL))
                self.log('current ROI', self.current_revenue() / self.total_costs())
            time.sleep(self.UPDATE_INTERVAL)
            if (time.time() - start_time) / 60 > 60:  # TODO: remove timeout after 60 min
                return

    def is_stock_not_yet_sold(self, client):
        return self.SYMBOL in [s.symbol for s in client.stocks()]

    def wait_till_sold(self, client):
        start_time = time.time()
        self.log('wait_till_sold()')
        while self.is_stock_not_yet_sold(client):
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
        if self.LOG_LEVEL: self.log('\n' * 10 + '>>>>>>>>>>>>> %s .run() at time' % (self.__class__.__name__), str(datetime.now()))
        cash_before_purchase = self.client.cash()

        self.client.bid(self.SYMBOL, self.AMOUNT)
        if self.LOG_LEVEL: self.log('buy order sent')

        self.wait_till_bought(self.client)
        if self.LOG_LEVEL: self.log_after_wait_till_bought()
        
        self.wait_till_ask()
        self.client.ask(self.SYMBOL, self.AMOUNT)
        if self.LOG_LEVEL: self.log('sell order sent')
        
        self.wait_till_sold(self.client)
        if self.LOG_LEVEL: self.log_profit(self.client.cash(), cash_before_purchase)
        self.f.close()


if __name__ == '__main__':
    from broker.adapter_investopediaapi_to_ibroker import AdapterInvestopediaApiToIBroker
    from broker.adapter_investopediaapi_to_imarketdata import AdapterInvestopediaApiToIMarketData
    broker = AdapterInvestopediaApiToIBroker()
    broker.login(USERNAME, PASSWORD)
    market_data = AdapterInvestopediaApiToIMarketData()
    StupidBot(broker, market_data).run()
