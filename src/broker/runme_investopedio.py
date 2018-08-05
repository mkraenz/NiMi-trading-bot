from broker.adapter_investopediaapi_to_ibroker import AdapterInvestopediaApiToIBroker
from broker.config import USERNAME, PASSWORD
from broker.adapter_investopediaapi_to_imarketdata import AdapterInvestopediaApiToIMarketData
from nimibot.stupidbot import StupidBot

if __name__ == '__main__':
    broker = AdapterInvestopediaApiToIBroker()
    broker.login(USERNAME, PASSWORD)
    market_data = AdapterInvestopediaApiToIMarketData()
    bot = StupidBot(broker, market_data)
    # Investopedia updates prices etc every 60 to 80 seconds
    bot.configure_running_behavior(update_interval=60)
    bot.configure_logging(5) # log everything
    bot.run()