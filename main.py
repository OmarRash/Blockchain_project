import hashlib
import time

class Node:
    def __init__(self, data):
        self.left=None
        self.right=None
        self.data=data

class Markle_tree:
    def __init__(self,transactions_list):
        self.node_list = []
        for i in range (0, 8, 2):
            node_data=hashlib.sha256((transactions_list[i]+transactions_list[i+1]).encode()).hexdigest()
            node = Node(node_data)
            node.left=transactions_list[i]
            node.right=transactions_list[i+1]
            self.node_list.append(node)

        for i in range (0, 6, 2):
            node_data = hashlib.sha256((self.node_list[i].data + self.node_list[i + 1].data).encode()).hexdigest()
            node = Node(node_data)
            node.left = self.node_list[i]
            node.right = self.node_list[i + 1]
            self.node_list.append(node)

    def root_node(self):
        return self.node_list[len(self.node_list)-1]

class Transaction:
    def __init__(self, sender, reciever, amount):
        self.sender= sender
        self.reciever= reciever
        self.amount= amount
        self.transaction_time=time.time()
        self.transaction_data=f"{sender} - {reciever}-{self.transaction_time}-{amount}"
        self.hash=hashlib.sha256(self.transaction_data.encode()).hexdigest()

    def hash_value(self):
        return self.hash

class Block:
    def __init__(self, previous_block_hash, root,timestamp):
        self.previous_block_hash = previous_block_hash
        self.root = root
        self.timestamp=timestamp
        self.nonce = 0
        self.block_data = f"{root.data} - {previous_block_hash}-{timestamp}-{self.nonce}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

    def mineBlock(self, difficulty):
        x="0"*difficulty
        while (self.block_hash[:difficulty] != x):
            self.nonce = self.nonce + 1
            self.block_data = f"{self.root} - {self.previous_block_hash}-{self.timestamp}-{self.nonce}"
            self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        print(self.nonce)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()
        self.difficulty=4
        self.transactions_list=[]

    def generate_genesis_block(self):
        genesis_node=Node("Genesis Block")
        self.chain.append(Block("0", genesis_node, 0))

    def create_block_from_transaction(self, transaction):
        if type(transaction)==str:
            self.transactions_list.append(transaction)
        elif len(transaction)>1:
            for i in range(len(transaction)):
                self.transactions_list.append(transaction[i])
        print(len(self.transactions_list))
        if len(self.transactions_list)==8:
            root=Markle_tree(self.transactions_list).root_node()
            previous_block_hash = self.last_block.block_hash
            t=time.time()
            B=Block(previous_block_hash, root, t)
            B.mineBlock(self.difficulty)
            self.chain.append(B)
            self.transactions_list=[]

    def display_chain(self):
        for i in range(len(self.chain)-1):
            print(f"Data {i + 1}: {self.chain[i+1].block_data}")
            print(f"Hash {i + 1}: {self.chain[i+1].block_hash}\n")

    @property
    def last_block(self):
        return self.chain[-1]

if __name__ == "__main__":

    t1 = Transaction("George", "Joe", "3.1")
    t2 = Transaction("Joe", "Adam", "2.5")
    t3 = Transaction("Joe", "Bob", "2.5")
    t4 = Transaction("Jo", "Adam", "2.5")
    t5 = Transaction("Joee", "Adam", "2.5")
    t6 = Transaction("Ji", "Adam", "2.5")
    t7 = Transaction("Jet", "Adam", "2.5")
    t8 = Transaction("Jel", "Adam", "2.5")

    block_chain = Blockchain()
    start=time.time()
    block_chain.create_block_from_transaction([t1.hash_value(), t2.hash_value(), t3.hash_value(), t4.hash_value()])
    block_chain.create_block_from_transaction([t5.hash_value(), t6.hash_value(), t7.hash_value()])
    block_chain.create_block_from_transaction(t8.hash_value())

    end1=time.time()
    print(end1-start)

    block_chain.display_chain()
    block_chain.create_block_from_transaction([t5.hash_value(), t6.hash_value(), t7.hash_value(), t8.hash_value()])
    block_chain.create_block_from_transaction([t1.hash_value(), t2.hash_value(), t3.hash_value(), t4.hash_value()])

    end2=time.time()
    print(end2-end1)
    block_chain.display_chain()