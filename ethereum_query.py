from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))

if w3.isConnected():
    x = 0
#     This line will mess with our autograders, but might be useful when debugging
else:
    print( "Failed to connect to Ethereum node!" )

def get_transaction(tx):
    tx = {}   #YOUR CODE HERE
    return tx

# Return the gas price used by a particular transaction,
#   tx is the transaction
def get_gas_price(tx):
    gas_price = 1 #YOUR CODE HERE
    gas_price = w3.eth.get_transaction(tx).gasPrice
    return gas_price

def get_gas(tx):
    gas = 1 #YOUR CODE HERE
    gas = w3.eth.get_transaction_receipt(tx).gasUsed
    return gas

def get_transaction_cost(tx):
    tx_cost = 1 #YOUR CODE HERE
    tx_cost = get_gas_price(tx) * get_gas(tx)
    return tx_cost

def get_block_cost(block_num):
    block_cost = 1  #YOUR CODE HERE
    transactions_list = w3.eth.get_block(block_num).transactions
    block_cost = 0
    for transaction in transactions_list:
        block_cost = block_cost + get_transaction_cost(transaction)
    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    max_tx = HexBytes('0xf7f4905225c0fde293e2fd3476e97a9c878649dd96eb02c86b86be5b92d826b6')  #YOUR CODE HERE
    transactions_list = w3.eth.get_block(block_num).transactions
    block_cost = 0
    maxblock_cost = 0
    for transaction in transactions_list:
        if get_transaction_cost(transaction) > block_cost
        maxblock_cost = block_cost
        max_tx = transaction
        
    return max_tx
