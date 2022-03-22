from typing import List
from utxo import UTXO, UTXOPool
from transaction import Transaction
from crypto import Crypto


class TxHandler:
    """
    Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is {@code pool}.
    """

    def __init__(self, pool: UTXOPool):
        # IMPLEMENT THIS
        self.pool = pool
        return

    """
    @return true if:
    (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
    (2) the signatures on each input of {@code tx} are valid, 
    (3) no UTXO is claimed multiple times by {@code tx},
    (4) all of {@code tx}s output values are non-negative, and
    (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
        values; and false otherwise.
    """

    def isValidTx(self, tx: Transaction) -> bool:
        used_outputs = set()
        inp_sum = 0
        out_sum = 0
        for i in range(tx.numInputs()):
            input: Transaction.Input = tx.getInput(i)
            utxo = UTXO(input._prevTxHash, i)
            if not self.pool.contains(utxo):
                return False
            pre_output: Transaction.Output = self.pool.getTxOutput(
                UTXO(input._prevTxHash, i))
            message = tx.getRawDataToSign(i)
            if not Crypto.verifySignature(pre_output.address, message, input.signature):
                return False
            if utxo in used_outputs:
                return False

            used_outputs.add(utxo)
            # tx.getRawDataToSign(i)
            # self.pool.getTxOutput()
            # input.
            if pre_output.value < 0:
                return False
            inp_sum += pre_output.value

        for i in range(tx.numOutputs()):
            out_sum += tx.getOutput(i).value
        if inp_sum < out_sum and not tx.isCoinbase():
            return False
        # IMPLEMENT THIS
        return True

    """
    Handles each epoch by receiving an unordered array of proposed transactions, checking each
    transaction for correctness, returning a mutually valid array of accepted transactions, and
    updating the current UTXO pool as appropriate.
    """

    def handleTxs(self, txs: List[Transaction]):
        validTxs = []
        for tx in txs:
            if self.isValidTx(tx):
                for i in range(tx.numOutputs()):
                    output = tx.getOutput(i)
                    utxo = UTXO(tx.hash, i)
                    self.pool.addUTXO(utxo, output)
                for i in range(tx.numInputs()):
                    input = tx.getInput(i)
                    self.pool.removeUTXO(
                        UTXO(input.prevTxHash, input.outputIndex))
                validTxs.append(tx)
        # IMPLEMENT THIS
        return validTxs

    def getUTXOPool(self):
        return self.pool
