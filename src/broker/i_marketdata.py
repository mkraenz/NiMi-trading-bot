class IMarketData(object):
    '''
    Separated from broker, because data can be retrieved from many webpages, e.g. Yahoo Finance, Google, etc.
    '''
    
    def price(self, symbol):
        raise NotImplementedError("Class %s doesn't implement price()" % (self.__class__.__name__))
