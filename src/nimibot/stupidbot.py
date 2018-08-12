import os
from _datetime import datetime


class StupidBot(object):
    
    def configure_logging(self, log_level=5, log_filename='log_bot.txt'):
        self.LOG_LEVEL = log_level  # 0 log nothing, 5 even logs the location of your mom
        self.LOG_FILENAME = log_filename
        self.f = None
    
    def configure_running_behavior(self, symbol='GOOG', update_interval=5, roi=1.00005, amount=50, periods=255, mov_avg_length=5):
        '''
        :param symbol: the stock we trade
        :param update_interval: get updates from broker in this interval, given in seconds
        :param roi: required return on investment on which sell will be performed
        :param amount: the quantity we trade in each order
        '''
        self.SYMBOL = symbol
        self.UPDATE_INTERVAL = update_interval
        self.ROI = roi
        # TODO change to quantity everywhere
        self.AMOUNT = amount
        self.PERIODS = periods
        self.MOV_AVG_LENGTH = mov_avg_length

    def __init__(self, broker, market_data):
        self.broker = broker
        self.market_data = market_data
        self.purchase_price = 0
        self.configure_running_behavior()
        
        self.configure_logging()

    def run(self):
        self.log('\n' * 5 + '>>>>>>>>>>>>> %s .run()' % (self.__class__.__name__)) 
        self.log('at time' + str(datetime.now()))
        
        prices = self.preparePrices()
        isBuy = True # True = next action is buy, else sell
        
        for period in range(self.PERIODS - self.MOV_AVG_LENGTH):
            if isBuy and self.getMovAvg(prices) < prices[-1]:
                self.buy(period + self.MOV_AVG_LENGTH)
                isBuy = False
                
            elif (not isBuy) and self.getMovAvg(prices) > prices[-1]:
                self.sell(period  + self.MOV_AVG_LENGTH)
                isBuy = True
                
            self.updatePrices(prices)

        self.closeLog()
        
    def preparePrices(self):
        return [self.market_data.price(self.SYMBOL) for _ in range(self.MOV_AVG_LENGTH)]
    
    def getMovAvg(self, prices):
        return sum(prices) / len(prices)
        
    def updatePrices(self, prices):        
        prices.pop(0)
        prices.append(self.market_data.price(self.SYMBOL))

    def buy(self, period):
        cash_before_purchase = self.broker.cash()
        self.log('Cash before purchase ' + str(cash_before_purchase))
        
        self.broker.bid(self.SYMBOL, self.AMOUNT)
        
        self.log('StupidBot bought in period ' + str(period))
        self.log('Total costs of purchase ' + str(cash_before_purchase - self.broker.cash()))
        self.log('Cash after purchase ' + str(self.broker.cash()))
        
    def sell(self, period):
        self.broker.ask(self.SYMBOL, self.AMOUNT)

        self.log('StupidBot sold  in period ' + str(period))
        self.log('Cash after purchase ' + str(self.broker.cash()))
        self.log('')
        
        
    def log(self, string):
        if not self.f:
            filename = os.path.join(os.getcwd(), self.LOG_FILENAME)
            self.f = open(filename, 'a', 1)
        self.f.writelines([string, '\n'])
        print(string)
        
    def closeLog(self):
        self.f.close()
        self.f = None
        
    
