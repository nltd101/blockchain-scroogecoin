from blockchain import BlockChain
from block import Block
from txhandler import TxHandler
from transaction import Transaction

class BlockHandler:
    def __init__(
        self,
        blkChain: BlockChain,
        privateKey,
    ):
        self._blockchain = blkChain
    
    def processBlock(self, Block: Block):
        if Block is None:
            return False
        return True
    
    def createBlock(self, myAddress):
        parent = self._blockchain.getMaxHeightBlock()
        prevHash = parent._hash
        utxoPool = self._blockchain.getMaxHeightUTXOPool()
        txsPool = self._blockchain.getTransactionPool()
        txs = txsPool.getTransactions()
        handler = TxHandler(utxoPool)
        validTxs = handler.handleTxs(txs)
        
        current = Block(
            prevHash,
            myAddress,
            validTxs,
            parent._height + 1,
            None
        )
        current.finalize()
        if self._blockchain.addBlock(current):
            return current
        return None
    
    def processTx(self, tx: Transaction):
        self._blockchain.addTransaction(tx)
