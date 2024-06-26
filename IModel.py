from abc import ABC, abstractmethod

class ModelInterface(ABC):
    #can be implemented using spot or forward measure
    @abstractmethod
    def drift(self):
        pass    

    #can be determinstic
    @abstractmethod
    def volatility(self):
        pass

    #can be determinstic
    @abstractmethod
    def distribution(self):
        pass

    #can be determinstic
    @abstractmethod
    def SDE(self):
        pass

    #if applicable
    @abstractmethod
    def choleskyFactor(self):
         pass  

    #Discrtization of time component
    @property 
    def timeGrid(self): 
        return self._tg

    @timeGrid.setter
    def timeGrid(self, value):
        self._tg = value 
