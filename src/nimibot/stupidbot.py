from InvestopediaApi.ita import Account, Action, get_quote
import time
import os


class StupidBot(object):
    
    USERNAME = '3rgwrqr2t2wrq5rgwy4u4ywsgr@trash-mail.com'
    PASSWORD = 'password'
    SYMBOL = 'GOOGL'
    UPDATE_INTERVAL = 10
    ROI = 1.002

    def __init__(self):
        self.purchase_price = 0

    def wait_till_bought(self, client):
        while True:
            portfolio = client.get_current_securities()
            for stock in portfolio.bought:
                if stock.symbol == self.SYMBOL:
                    self.purchase_price = portfolio.bought[0].purchase_price
                    return
            time.sleep(self.UPDATE_INTERVAL)

    def wait_till_ask(self):
        while get_quote(self.SYMBOL) / self.purchase_price < self.ROI:
            time.sleep(self.UPDATE_INTERVAL)

    def wait_till_sold(self, client):
        while not client.get_current_securities().bought:
            time.sleep(self.UPDATE_INTERVAL)            

    def log_profit(self, current_cash, cash_before_purchase):
        filename = os.path.join(os.getcwd(), 'ProfitOfNiMiBot.txt')
        with open(filename, 'w', newline='') as f:
            f.write('Profit = ' + str(current_cash - cash_before_purchase))
            f.write('Cash after purchase = ' + str(current_cash))
            f.write('Cash before purchase = ' + str(cash_before_purchase))
    
    def run(self):
        client = Account(self.USERNAME, self.PASSWORD)
        cash_before_purchase = client.get_portfolio_status().cash
        client.trade(self.SYMBOL, Action.buy, 50)
        
        self.wait_till_bought(client)
        self.wait_till_ask()
        client.trade(self.SYMBOL, Action.sell, 50)
        self.wait_till_sold(client)
        self.log_profit(client.get_portfolio_status().cash, cash_before_purchase)
        

if __name__ == '__main__':
    StupidBot().run()
