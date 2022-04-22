import copy
from typing import Dict, List
from block import Block
from transaction import Transaction
from transactionpool import TransactionPool
from txhandler import TxHandler
from utxo import UTXO, UTXOPool


# Block Chain should maintain only limited block nodes to satisfy the functions
# You should not have all the blocks added to the block chain in memory
# as it would cause a memory overflow.
class State:
    def __init__(self, block: Block, utxoPool: UTXOPool) -> None:
        self._block = block
        self._utxoPool = copy.copy(utxoPool)

    def getUTXOPool(self):
        return copy.copy(self._utxoPool)

    def getBlock(self):
        return self._block

    def __str__(self) -> str:
        return self._block.getTransactions()


class BlockChain:
    CUT_OFF_AGE = 10

    """
    create an empty block chain with just a genesis block. Assume {​@code​ genesisBlock} is
    a valid block
    """

    def __init__(self, genesisBlock: Block):
        self.transPool: TransactionPool = TransactionPool()

        utxoPool: UTXOPool = UTXOPool()
        for i in range(genesisBlock.getCoinbase.numOutputs()):
            utxoPool.addUTXO(UTXO(genesisBlock.getCoinbase.hash, i),
                             genesisBlock.getCoinbase.getOutput(i))
        for trans in genesisBlock.getTransactions:
            if trans:
                for i in range(trans.numOutputs):
                    ouput = Transaction.getOutput(trans, i)
                    utxo = UTXO(trans.hash, i)
                    utxoPool.addUTXO(utxo, ouput)

        self.states: List[List[State]] = list()

        self.states.append([State(genesisBlock, utxoPool)])
        # IMPLEMENT THIS
        return

    def getMaxHeightBlock(self):
        return self.states[len(self.states) - 1][0].getBlock()
        # IMPLEMENT THIS

    def getMaxHeightUTXOPool(self):
        # IMPLEMENT THIS
        return self.states[len(self.states) - 1][0].getUTXOPool()

    def getTransactionPool(self):
        # IMPLEMENT THIS
        return self.transPool

    def addBlock(self, blk: Block):
        if not blk.getPrevBlockHash:
            return False
        isAdded = False
        for height in range(len(self.states)):
            for iState in range(len(self.states[height])):
                if blk.getPrevBlockHash == self.states[height][iState].getBlock().getHash:
                    if height + 1 == len(self.states):
                        utxoPool = self.states[height][iState].getUTXOPool()
                        txtHandler = TxHandler(utxoPool)

                        txtHandler.handleTxs(blk.getTransactions)
                        utxoPool = txtHandler.getUTXOPool()
                        for i in range(blk.getCoinbase.numOutputs()):
                            utxoPool.addUTXO(UTXO(blk.getCoinbase.hash, i),
                                             blk.getCoinbase.getOutput(i))
                        self.states.append([State(blk, utxoPool)])
                        if len(self.states) == self.CUT_OFF_AGE:
                            self.states.pop(0)
                    else:
                        self.states[height].append(State(blk, utxoPool))
                    isAdded = True
        # IMPLEMENT THIS
        if isAdded:
            for tx in blk.getTransactions:
                self.transPool.removeTransaction(tx.hash)

        return isAdded

    def addTransaction(self, tx: Transaction):
        # IMPLEMENT THIS
        self.transPool.addTransaction(tx)
        return
