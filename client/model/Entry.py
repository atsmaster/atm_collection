class Entry():

    def __init__(self, exchange, symbol):
        self.__exchange = exchange
        self.__symbol = symbol
        pass

    @property
    def exchange(self):
        return self.__exchange

    @exchange.setter
    def exchange(self, value):
        self.__exchange = value

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, value):
        self.__symbol = value
