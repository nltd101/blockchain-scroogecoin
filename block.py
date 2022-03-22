import hashlib
from typing import List
from transaction import Transaction


class Block:
    COINBASE = 25

    def __init__(
        self,
        prevBlockHash: bytes,
        address,
        txs,
        height: int,  # Additional field
        hash: bytes,
    ):
        if address is None:
            raise ValueError("Invalid params, miner's address can't be null")
        else:
            coinbase = Transaction.NewCoinbase(Block.COINBASE, address)
            self._coinbase = coinbase
        if prevBlockHash is None:
            raise ValueError("Invalid params, prevBlockHash can't be null")
        else:
            self._prevBlockHash = prevBlockHash
        if height is None:
            raise ValueError("Invalid params, height can't be null")
        else:
            self._height = height
        if txs is None:
            self._txs = []
        else:
            self._txs = txs

        if hash != None:
            raise ValueError(
                "Invalid params, hash must be null, and be assigned later.")
        else:
            self._hash = []

    @property
    def getCoinbase(self):
        return self._coinbase

    @property
    def getHash(self):
        return self._hash

    @property
    def getPrevBlockHash(self):
        return self._prevBlockHash

    @property
    def getTransactions(self):
        return self._txs

    @property
    def getTransaction(self, index):
        return self._txs[index]

    def addTransaction(self, tx):
        self._txs.append(tx)

    def getRawBlock(self):
        rawBlock = b""
        rawBlock += self._prevBlockHash
        rawBlock += self._coinbase.getRawTx()
        for tx in self._txs:
            rawBlock += tx.getRawTx()
        return rawBlock

    def finalize(self):
        md = hashlib.sha256()
        md.update(self.getRawBlock())
        self._hash = md.digest()
