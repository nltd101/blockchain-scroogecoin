from block import Block
from blockchain import BlockChain
from blockhandler import BlockHandler
from transaction import Transaction
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15

alice_key: RSA.RsaKey = RSA.generate(1024)
pubkey = alice_key.public_key().export_key()
private_key = alice_key.export_key()

coin_base = Transaction.NewCoinbase(10, alice_key)
bob_key: RSA.RsaKey = RSA.generate(1024)

gblock = Block(bytes(0),  alice_key, [], 0, None)
gblock.finalize()
blockchain = BlockChain(gblock)

bHandler = BlockHandler(blockchain, None)

t = Transaction()
t.addInput(gblock.getCoinbase.hash, 0)

t.addOutput(4, bob_key)
t.addOutput(21, alice_key)
for i in range(t.numInputs()):
    h = SHA256.new(t.getRawDataToSign(i))
    verifier = pkcs1_15.new(alice_key)
    sig = verifier.sign(h)
    input = t.getInput(i)
    input.addSignature(sig)

bHandler.processTx(t)
bHandler.createBlock(bob_key)

