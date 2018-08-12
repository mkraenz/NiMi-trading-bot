class IHistoricalMarketData(object):
        
    def priceWithoutTimeChange(self, symbol):
        raise NotImplementedError("Class %s doesn't implement priceWithoutTimeChange()" % (self.__class__.__name__))