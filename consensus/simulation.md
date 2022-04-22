# Simulation

Edit the parameters used to test your code in the `__main__` block:

```python
if __name__ == "__main__":
    s = Simulation(numNodes = 100, p_graph = 0.1, p_mal = 0.3, p_txD = 0.01, numR = 20)
    s.main()
```

Run the simulation with `python simulation.py`.

## Simulation class:

A basic graph generator using to run own simulation. There will be a set number of rounds where during each round, nodes
will broadcast their proposal to their followers and at the end of the round, should have reached a consensus on what
transactions should be agreed upon.

- ### Properties

| **Attribute**      | **Type**  | **Description**                                                                  |
| -------------      | --------- | ----------------------------------------------------                             |
| *numNodes*         | *integer* | The number of nodes in graph (default: 100)                                      |
| *p_graph*          | *float*   | The pairwise connectivity probability of the random graph                        |
| *p_malicious*      | *float*   | The probability that a node will be set to be malicious                          |
| *p_txDistribution* | *float*   | The probability that each of the initial valid transactions will be communicated |
| *numRounds*        | *integer* | The number of rounds in the simulation                                           |

- ### Main function

#### Step 1

- Generate `numNodes` - number of Nodes in the network, nodes are either compliant or malicious.
- Pick which nodes are malicious and which are compliant by `p_malicious` - malicious probability of node.

```python
nodes = []
compliants = []

for i in range(self.numNodes):
    if random.rand() < self.p_malicious:
        nodes.append(MaliciousNode(self.p_graph, self.p_malicious, self.p_txDistribution, self.numRounds))
    else:
        node = CompliantNode(self.p_graph, self.p_malicious, self.p_txDistribution, self.numRounds)
        nodes.append(node)
        compliants.append(node)
```

#### Step 2

- Each node will be given its list of followees via a boolean 2-dimensional array.
- `followees[i][j]` is `True` if node `i` follows node `j`, `False` otherwise.
- Initialize the pairwise by `p_graph` - connectivity probability of the random graph.

```python
followees = full((self.numNodes, self.numNodes), False)

for i in range(self.numNodes):
    for j in range(self.numNodes):
        if i == j:
            continue
        if random.rand() < self.p_graph:
            followees[i][j] = True
```

- After the pairwise establishment, notify all nodes of their followees:

```python
for i in range(self.numNodes):
    nodes[i].setFollowees(followees[i])
}
```

#### Step 3

- Generating the initial transactions. Assume that all transactions are valid and that invalid transactions cannot be
  created.
- Default number of Transactions is 500 for testing. Each Transaction is unique.

```python
numTx = 500
validTxIds = {i for i in range(numTx)}
```

- Distribute the 500 Transactions throughout the nodes, to initialize the starting state of Transactions each node has
  heard.
- These transactions will be stored in Pending Transaction pool of each Node.
- The distribution is random with probability `p_txDistribution` for each Transaction-Node pair.
- Also compute the largest possible consensus that could be achieved on this network.

```python
possibleConsensus = set()
for i in range(self.numNodes):
    pendingTransactions = set()
    for txID in validTxIds:
        if random.rand() < self.p_txDistribution:
            pendingTransactions.add(Transaction(txID))
    nodes[i].setPendingTransaction(pendingTransactions)
    if isinstance(nodes[i], CompliantNode):
        possibleConsensus |= pendingTransactions
```

#### Step 4

- Simulate for `numRounds` times. In each round, nodes will broadcast their proposal (list of transactions) to their
  followers.
- Gather all the proposals into a map - `allProposals`. The key is the index of the node receiving proposals. The value
  is candidate arrays. Candidate contains the id of the transaction being proposed and the index of the node proposing
  the transaction.

```python
for _round in range(self.numRounds):
    allProposals = dict()

    for i in range(self.numNodes):
        proposals = nodes[i].sendToFollowers()

        for tx in proposals:
            # Ensure that each tx is actually valid
            if tx.id not in validTxIds:
                continue

            for j in range(self.numNodes):
              # tx only matters if j follows i
              if not followees[j][i]:
                continue

                if j not in allProposals:
                    allProposals[j] = set()

                candidate = Candidate(tx, i)
                allProposals[j].add(candidate)
```

- Each round, distribute the Proposals in `allProposals` map to their intended recipients as Candidates

```python
for i in range(self.numNodes):
    if i in allProposals:
        nodes[i].receiveFromFollowees(allProposals[i])
```

#### Step 5

- Get the result after simulation.
- Group nodes together according to the consensus that they have achieved. 
- Print each consensus group and their sizes.

```python
groups = dict()
for i in range(self.numNodes):
    if isinstance(nodes[i], CompliantNode):
        ids = [tx.id for tx in nodes[i].sendToFollowers()]
        ids.sort()
        ids = tuple(ids)
        if ids not in groups:
            groups[ids] = []
        groups[ids].append(i)

for txs, nodes in groups.items():
    print("Node group: %d/%d" % (len(nodes), len(compliants)))
    print(nodes)
    print("Consensus: %d/%d" % (len(txs), len(possibleConsensus)))
    print(txs)
    print()
```
