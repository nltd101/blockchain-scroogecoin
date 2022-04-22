from transaction import Transaction
from node import Node

class MaliciousNode(Node):
    def __init__(self, p_graph, p_mallicious, p_txDistribution, numRound):
        pass
        

    def setFollowees(self, follow):
        pass

    def setPendingTransaction(self, pendingTransactions):
        pass

    def sendToFollowers(self) -> set:
        return set()

    def receiveFromFollowees(self, candidates: set):
        pass
