from InvestopediaApi.ita import Account, Action, get_quote
import time
import os


class StupidBot(object):
    
    LOG_LEVEL = 5
    USERNAME = '3rgwrqr2t2wrq5rgwy4u4ywsgr@trash-mail.com'
    PASSWORD = 'password'
    SYMBOL = 'GOOGL'
    UPDATE_INTERVAL = 60  # Investopedia updates prices etc every 60 to 80 seconds
    ROI = 1.00005
    AMOUNT = 50
    COMMISION_FEE = 0.0  # determined by broker

    def __init__(self):
        self.purchase_price = 0
        filename = os.path.join(os.getcwd(), 'ProfitOfNiMiBot.txt')
        self.f = open(filename, 'w')

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
        self.log('waited minutes', ((time.time() - start_time) / 60))
    
    def run(self):
        client = Account(self.USERNAME, self.PASSWORD)
        cash_before_purchase = client.get_portfolio_status().cash

        client.trade(self.SYMBOL, Action.buy, self.AMOUNT)
        if self.LOG_LEVEL: self.log('buy order sent')

        self.wait_till_bought(client)
        if self.LOG_LEVEL: self.log_after_wait_till_bought()
        
        self.wait_till_ask()
        client.trade(self.SYMBOL, Action.sell, self.AMOUNT)
        if self.LOG_LEVEL: self.log('sell order sent')
        
        self.wait_till_sold(client)
        if self.LOG_LEVEL: self.log_profit(client.get_portfolio_status().cash, cash_before_purchase)
        self.f.close()


if __name__ == '__main__':
    StupidBot().run()
