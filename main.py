import hashlib
import time
import copy

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


class Pool:
    def __init__(self):
        self.pool = []

    def add_transaction(self,transaction):
        if type(transaction)==str:
            self.pool.append(transaction)
        elif len(transaction)>1:
            for i in range(len(transaction)):
                self.pool.append(transaction[i]) 

    def generate_block(self):
        if len(self.pool)>=8:
            root=Markle_tree(self.pool).root_node()
            t=time.time()
            self.pool=self.pool[8:]
            return Block("", root, t)
        else:
            return False

class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()
        self.difficulty=4


    def set_difficulty(self,n):
        self.difficulty=n

    def get_difficulty(self):
        return self.difficulty

    def generate_genesis_block(self):
        genesis_node=Node("Genesis Block")
        self.chain.append(Block("0", genesis_node, 0))

    
    def mineBlock(self,B,speed):
        x="0"*self.difficulty
        i=0
        for i in range(speed):
            if B.block_hash[:self.difficulty] == x:
                print('nonce: ' + str(B.nonce))
                self.chain.append(B)
                return True
            B.nonce = B.nonce + 1
            B.block_data = f"{B.root.data} - {B.previous_block_hash}-{B.timestamp}-{B.nonce}"
            B.block_hash = hashlib.sha256(B.block_data.encode()).hexdigest()
        return False
        

    def display_chain(self):
        for i in range(len(self.chain)-1):
            print(f"Data {i + 1}: {self.chain[i+1].block_data}")
            print(f"Hash {i + 1}: {self.chain[i+1].block_hash}\n")

    @property
    def last_block(self):
        return self.chain[-1]


class User:
    def __init__(self,id):
        self.id = id
        self.local_block_chain = Blockchain()

    def set_BC_block_chain(self,bc):
        self.compare(bc)
    
    def compare(self,bc):
        if len(bc.chain)>len(self.local_block_chain.chain):
            self.local_block_chain = copy.deepcopy(bc) 
        elif len(bc.chain)==len(self.local_block_chain.chain):
            if((bc.chain[-1].timestamp-self.local_block_chain.chain[-1].timestamp)<0):
                self.local_block_chain = copy.deepcopy(bc)

    def create_block(self,b):
        b.previous_block_hash = self.local_block_chain.chain[-1].block_hash
        b1 = copy.deepcopy(b)
        return b1

if __name__ == "__main__":

    user = User(1)
    user1 = User(2)
    attacker = User(-1)
    user2 = User(3)

    transactions = Pool()

    t = []
    for i in range(40):
        transactions.add_transaction(Transaction("joe","bob",str(i+1)).hash_value())

    b = transactions.generate_block()
    b1 = user1.create_block(b)
    b2 = user2.create_block(b)

    start_time = time.time()

    while(1):   
        if user1.local_block_chain.mineBlock(b1,51):
            user.set_BC_block_chain(user1.local_block_chain)
            user2.set_BC_block_chain(user1.local_block_chain)
            attacker.set_BC_block_chain(user1.local_block_chain)
            print("block 1: User1 is TOP\n")
            break
        elif user2.local_block_chain.mineBlock(b2,49):
            user.set_BC_block_chain(user2.local_block_chain)
            user1.set_BC_block_chain(user2.local_block_chain)
            attacker.set_BC_block_chain(user2.local_block_chain)
            print("block 1: User2 is TOP\n")
            break

    print(f'time taken to mine block = {time.time()-start_time} sec')
    b = transactions.generate_block()

    b1 = user1.create_block(b)
    b2 = user2.create_block(b)

    while(1):   
        if user2.local_block_chain.mineBlock(b2,51):
            user.set_BC_block_chain(user2.local_block_chain)
            user1.set_BC_block_chain(user2.local_block_chain)
            attacker.set_BC_block_chain(user2.local_block_chain)
            print("block 2: User2 is TOP\n")
            break

        elif user1.local_block_chain.mineBlock(b1,49):
            user.set_BC_block_chain(user1.local_block_chain)
            user2.set_BC_block_chain(user1.local_block_chain)
            attacker.set_BC_block_chain(user1.local_block_chain)
            print("block 2: User1 is TOP\n")
            break

    print('after adding 2 blocks: ')
    user.local_block_chain.display_chain()

    b = transactions.generate_block()

    b1 = user1.create_block(b)
    b2 = user2.create_block(b)
    attacker.local_block_chain.chain.pop()
    print("attacker: ")
    attacker.local_block_chain.display_chain()

    while(1):   
        if attacker.local_block_chain.mineBlock(b1,40):
            user.set_BC_block_chain(attacker.local_block_chain)
            user1.set_BC_block_chain(attacker.local_block_chain)
            user2.set_BC_block_chain(attacker.local_block_chain)
            print("block 3: Attacker is TOP\n")
            break
        elif user2.local_block_chain.mineBlock(b2,49):
            user.set_BC_block_chain(user2.local_block_chain)
            user1.set_BC_block_chain(user2.local_block_chain)
            attacker.set_BC_block_chain(user2.local_block_chain)
            print("block 3: User2 is TOP\n")
            break

    print('block chain: ')
    user.local_block_chain.display_chain()

    print('forked block chain: ')
    attacker.local_block_chain.display_chain()

    b = transactions.generate_block()

    b1 = user1.create_block(b)
    b2 = user2.create_block(b)

    while(1):   
        if attacker.local_block_chain.mineBlock(b1,40):
            user.set_BC_block_chain(attacker.local_block_chain)
            user1.set_BC_block_chain(attacker.local_block_chain)
            user2.set_BC_block_chain(attacker.local_block_chain)
            print("block 4: Attacker is TOP\n")
            break
        elif user2.local_block_chain.mineBlock(b2,49):
            user.set_BC_block_chain(user2.local_block_chain)
            user1.set_BC_block_chain(user2.local_block_chain)
            attacker.set_BC_block_chain(user2.local_block_chain)
            print("block 4: User2 is TOP\n")
            break

    print("after attack: ")
    user.local_block_chain.display_chain()

    b = transactions.generate_block()

    b1 = user1.create_block(b)
    b2 = user2.create_block(b)

    while(1):   
        if user1.local_block_chain.mineBlock(b1,51):
            user.set_BC_block_chain(user1.local_block_chain)
            attacker.set_BC_block_chain(user1.local_block_chain)
            user2.set_BC_block_chain(user1.local_block_chain)
            print("block 5: User1 is TOP\n")
            break
        elif user2.local_block_chain.mineBlock(b2,49):
            user.set_BC_block_chain(user2.local_block_chain)
            user1.set_BC_block_chain(user2.local_block_chain)
            attacker.set_BC_block_chain(user2.local_block_chain)
            print("block 5: User2 is TOP\n")
            break
    
    print("trusted block chain: ")
    user.local_block_chain.display_chain()