from abc import ABC, abstractmethod


# Das Retrieval-System soll als Ergebnis ein eine sortierte Liste der relevanten DocIds zurückliefern 
# und eine Liste der dazugehörigen Ranking-Scores.
class InitRetrievalSystem(ABC):
    @abstractmethod
    def __init__(self, docIds):
        self.docIds = docIds
        pass
    
    @abstractmethod
    def retrieve(self, query):
        pass
    
    @abstractmethod
    def retrieve_k(self, query, k):
        pass
