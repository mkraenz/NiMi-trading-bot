import time


class StupidBot(object):
    
    def configure_logging(self, log_level=0, log_filename='log_bot.txt'):
        self.LOG_LEVEL = log_level  # 0 log nothing, 5 even logs the location of your mom
        self.LOG_FILENAME = log_filename
    
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
            print('Period is ', period)
            period += 1
            time.sleep(self.UPDATE_INTERVAL)

    def wait_till_sold(self, expected_amount_after_sell=0):
        while self.broker.getQuantity(self.SYMBOL) > expected_amount_after_sell:
            time.sleep(self.UPDATE_INTERVAL)

    def run(self):
        print('StupidBot.run()')
        cash_before_purchase = self.broker.cash()

        self.broker.bid(self.SYMBOL, self.AMOUNT)
        print('StupidBot bids')
        
        self.wait_till_bought()
        print('StupidBot bought')
        print('Total costs for purchase', cash_before_purchase - self.broker.cash())
        
        self.wait_till_ask()
        print('StupidBot waits for ask')
        self.broker.ask(self.SYMBOL, self.AMOUNT)
        print('StupidBot asks')
        print('Profit', self.broker.cash() - cash_before_purchase)
        print('Cash after purchase', self.broker.cash())
        print('Cash before purchase', cash_before_purchase)
        
        self.wait_till_sold()
        print('StupidBot sold')
