from historical.historical_broker import HistoricalBroker
from historical.historical_market_data import HistoricalMarketData
from nimibot.stupidbot import StupidBot

if __name__ == '__main__':
    market_data = HistoricalMarketData()
    broker = HistoricalBroker(market_data)
    market_data.importPrices('data/GOOG.csv')
    bot = StupidBot(broker, market_data)
    bot.configure_running_behavior(update_interval=0, roi=1.0369) # expect sell on period 5, 2016-07-12 in GOOG.csv
    bot.configure_logging(5)
    bot.run()
