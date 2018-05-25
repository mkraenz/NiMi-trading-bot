from InvestopediaApi.ita import Account, Action, get_quote
import time
import os


class StupidBot(object):
    
    LOG_LEVEL = 5
    USERNAME = '3rgwrqr2t2wrq5rgwy4u4ywsgr@trash-mail.com'
    PASSWORD = 'password'
    SYMBOL = 'GOOGL'
    UPDATE_INTERVAL = 10
    ROI = 1.002
    AMOUNT = 50

    def __init__(self):
        self.purchase_price = 0

    def wait_till_bought(self, client):
        while True:
            portfolio = client.get_current_securities()
            for stock in portfolio.bought:
                if stock.symbol == self.SYMBOL:
                    self.purchase_price = portfolio.bought[0].purchase_price
                    return
            if self.LOG_LEVEL: print('wait_till_bought(), I mean wait_till_bored(), still running')
            time.sleep(self.UPDATE_INTERVAL)

    def wait_till_ask(self):
        while get_quote(self.SYMBOL) / self.purchase_price >= self.ROI:
            if self.LOG_LEVEL: 
                print('wait_till_ask() still running')
                print('current price', get_quote(self.SYMBOL))
                print('current yield', get_quote(self.SYMBOL) / self.purchase_price)
            time.sleep(self.UPDATE_INTERVAL)

    def wait_till_sold(self, client):
        while not client.get_current_securities().bought:
            if self.LOG_LEVEL: print('wait_till_sold() still running')
            time.sleep(self.UPDATE_INTERVAL)            

    def log_profit(self, current_cash, cash_before_purchase):
        filename = os.path.join(os.getcwd(), 'ProfitOfNiMiBot.txt')
        with open(filename, 'w', newline='') as f:
            f.write('Profit = ' + str(current_cash - cash_before_purchase) + '\n')
            f.write('Cash after purchase = ' + str(current_cash) + '\n')
            f.write('Cash before purchase = ' + str(cash_before_purchase) + '\n')
    
    def run(self):
        client = Account(self.USERNAME, self.PASSWORD)
        cash_before_purchase = client.get_portfolio_status().cash
        if self.LOG_LEVEL: print('cash before purchase = ', str(cash_before_purchase))

        client.trade(self.SYMBOL, Action.buy, self.AMOUNT)
        if self.LOG_LEVEL: print('buy order sent.')

        self.wait_till_bought(client)
        self.wait_till_ask()
        client.trade(self.SYMBOL, Action.sell, self.AMOUNT)
        if self.LOG_LEVEL: print('sell order sent.')
        
        self.wait_till_sold(client)
        if self.LOG_LEVEL: 
            new_cash = client.get_portfolio_status().cash
            print('new cash', str(new_cash))
            print('profit', str(new_cash - self.cash_before_purchase))
        self.log_profit(client.get_portfolio_status().cash, cash_before_purchase)
        

if __name__ == '__main__':
    StupidBot().run()
