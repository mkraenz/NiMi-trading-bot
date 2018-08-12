import time
import os
from _datetime import datetime


class StupidBot(object):
    
    def configure_logging(self, log_level=5, log_filename='log_bot.txt'):
        self.LOG_LEVEL = log_level  # 0 log nothing, 5 even logs the location of your mom
        self.LOG_FILENAME = log_filename
        self.f = None
    
    def configure_running_behavior(self, symbol='GOOG', update_interval=5, roi=1.00005, amount=50):
        '''
        :param symbol: the stock we trade
        :param update_interval: get updates from broker in this interval, given in seconds
        :param roi: required return on investment on which sell will be performed
        :param amount: the quantity we trade in each order
        '''
        self.SYMBOL = symbol
        self.UPDATE_INTERVAL = update_interval
        self.ROI = roi
        # TODO #14 change to quantity everywhere
        self.AMOUNT = amount

    def __init__(self, broker, market_data):
        self.broker = broker
        self.market_data = market_data
        self.purchase_price = 0
        self.configure_running_behavior()
        
        self.configure_logging()

    def wait_till_bought(self):
        while True:
            for stock in self.broker.stocks():
                if stock.symbol == self.SYMBOL:
                    self.purchase_price = stock.purchase_price
                    return
            time.sleep(self.UPDATE_INTERVAL)

    def current_revenue(self):
        return self.market_data.price(self.SYMBOL) * self.AMOUNT - self.broker.fee()

    def total_costs(self):
        return self.purchase_price * self.AMOUNT + self.broker.fee()

    def wait_till_ask(self):
        period = 1
        while self.current_revenue() < self.ROI * self.total_costs():
            period += 1
            time.sleep(self.UPDATE_INTERVAL)
        self.log('Period is ' + str(period))

    def wait_till_sold(self, expected_amount_after_sell=0):
        while self.broker.getQuantity(self.SYMBOL) > expected_amount_after_sell:
            time.sleep(self.UPDATE_INTERVAL)

    def run(self):
        self.log('\n' * 5 + '>>>>>>>>>>>>> %s .run()' % (self.__class__.__name__)) 
        self.log('at time' + str(datetime.now()))
        cash_before_purchase = self.broker.cash()

        self.broker.bid(self.SYMBOL, self.AMOUNT)
        self.log('StupidBot bids')
        
        self.wait_till_bought()
        self.log('StupidBot bought')
        self.log('Total costs for purchase' + str(cash_before_purchase - self.broker.cash()))
        
        self.wait_till_ask()
        self.log('StupidBot waits for ask')
        self.broker.ask(self.SYMBOL, self.AMOUNT)
        self.log('StupidBot asks')
        self.log('Profit ' + str(self.broker.cash() - cash_before_purchase))
        self.log('Cash after purchase ' + str(self.broker.cash()))
        self.log('Cash before purchase ' + str(cash_before_purchase))
        
        self.wait_till_sold()
        self.log('StupidBot sold')
        self.closeLog()
        
    def log(self, string):
        if not self.f:
            filename = os.path.join(os.getcwd(), self.LOG_FILENAME)
            self.f = open(filename, 'a', 1)
        self.f.writelines([string, '\n'])
        print(string)
        
    def closeLog(self):
        self.f.close()
        self.f = None
