from typing import Dict, List
from block import Block
from transaction import Transaction
from transactionpool import TransactionPool
from txhandler import TxHandler
from utxo import UTXO, UTXOPool


# Block Chain should maintain only limited block nodes to satisfy the functions
# You should not have all the blocks added to the block chain in memory
# as it would cause a memory overflow.


class BlockChain:
    CUT_OFF_AGE = 10

    """
    create an empty block chain with just a genesis block. Assume {​@code​ genesisBlock} is
    a valid block
    """

    def __init__(self, genesisBlock: Block):
        self.transPool: TransactionPool = TransactionPool()

        self.maxUtxoPool: UTXOPool = UTXOPool()
        for i in range(genesisBlock.getCoinbase.numOutputs()):
            self.maxUtxoPool.addUTXO(UTXO(genesisBlock.getCoinbase.hash, i),
                                     genesisBlock.getCoinbase.getOutput(i))
        for trans in genesisBlock.getTransactions:
            if trans:
                for i in range(trans.numOutputs):
                    ouput = Transaction.getOutput(trans, i)
                    utxo = UTXO(trans.hash, i)
                    self.maxUtxoPool.addUTXO(utxo, ouput)

        self.blocks: List[List[Block]] = list()

        self.blocks.append([genesisBlock])
        # IMPLEMENT THIS
        return

    def getMaxHeightBlock(self):
        return self.blocks[len(self.blocks) - 1][0]
        # IMPLEMENT THIS

    def getMaxHeightUTXOPool(self):
        # IMPLEMENT THIS
        return self.maxUtxoPool

    def getTransactionPool(self):
        # IMPLEMENT THIS
        return self.transPool

    def addBlock(self, blk: Block):
        if not blk.getPrevBlockHash:
            return False
        isAdded = False
        for height in range(len(self.blocks)):
            for iBlock in range(len(self.blocks[height])):
                if blk.getPrevBlockHash == self.blocks[height][iBlock].getHash:
                    if height + 1 == len(self.blocks):
                        self.blocks.append([blk])
                        txtHandler = TxHandler(self.maxUtxoPool)
                        txtHandler.handleTxs(blk.getTransactions)
                        self.maxUtxoPool = txtHandler.getUTXOPool()
                        for i in range(blk.getCoinbase.numOutputs()):
                            self.maxUtxoPool.addUTXO(UTXO(blk.getCoinbase.hash, i),
                                                     blk.getCoinbase.getOutput(i))

                        if len(self.blocks) == self.CUT_OFF_AGE:
                            self.blocks.pop(0)
                    else:
                        self.blocks[height].append(blk)
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
