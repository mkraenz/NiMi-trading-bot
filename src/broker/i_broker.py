class IBroker(object):
    
    def bid(self, symbol, amount):
        raise NotImplementedError("Class %s doesn't implement bid()" % (self.__class__.__name__))

    def ask(self, symbol, amount):
        raise NotImplementedError("Class %s doesn't implement ask()" % (self.__class__.__name__))
    
    def fee(self):
        raise NotImplementedError("Class %s doesn't implement fees()" % (self.__class__.__name__))

    def stocks(self):
        raise NotImplementedError("Class %s doesn't implement stocks()" % (self.__class__.__name__))

    def cash(self):
        raise NotImplementedError("Class %s doesn't implement cash()" % (self.__class__.__name__))
    
    def login(self):
        raise NotImplementedError("Class %s doesn't implement login()" % (self.__class__.__name__))