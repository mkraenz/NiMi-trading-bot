from broker.i_marketdata import IMarketData
from historical.i_historical_market_data import IHistoricalMarketData


class HistoricalMarketData(IMarketData, IHistoricalMarketData):
    
    prices = []
    time = -1
        
    def price(self, symbol):
        self.time += 1
        return self.prices[self.time]
    
    def priceWithoutTimeChange(self, symbol):
        return self.prices[self.time] if self.time > 0 else self.prices[0]
    
    def importPrices(self, path):
        with open(path, 'r') as file:
            prices_as_str = [line.split(',')[5] for line in file]
        prices_as_str.pop(0)
        self.prices = [float(string) for string in prices_as_str]


if __name__ == '__main__':
    md = HistoricalMarketData()
    md.importPrices('data/GOOG.csv')
    print(md.prices)
