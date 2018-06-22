from broker.i_marketdata import IMarketData
from InvestopediaApi.ita import get_quote

class AdapterInvestopediaApiToIMarketData(IMarketData):

    def price(self, symbol):
        return get_quote(symbol)
