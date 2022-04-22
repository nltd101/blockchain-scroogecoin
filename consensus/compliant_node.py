from transaction import Transaction
from node import Node
from candidate import Candidate


class CompliantNode(Node):
    def __init__(self, p_graph, p_mallicious, p_txDistribution, numRound):
        # IMPLEMENT THIS
        self.p_graph = p_graph
        self.p_mallicious = p_mallicious
        self.p_txDistribution = p_txDistribution
        self.numRound = numRound
        return

    def setFollowees(self, followees):
        self.followees = followees
        # IMPLEMENT THIS
        return

    def setPendingTransaction(self, pendingTransactions):
        self.pendingTransaction = pendingTransactions
        # IMPLEMENT THIS
        return

    def sendToFollowers(self) -> set[Transaction]:
        # IMPLEMENT THIS
        return self.pendingTransaction

    def receiveFromFollowees(self, candidates: set[Candidate]):
        newtxset = set()
        for candidate in candidates:
            newtxset.add(candidate.tx)
        self.pendingTransaction = newtxset
        # IMPLEMENT THIS
        return
