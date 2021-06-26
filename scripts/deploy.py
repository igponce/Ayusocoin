# Despliegue

from brownie import Ayusocoin, Faucet, accounts


def DeployContracts():
    
    token = accounts[0].deploy(Ayusocoin)
    faucet = accounts[0].deploy(Faucet,token.address, 1000_000000)
    
    root = accounts[0].address
    
    alltokens = token.totalSupply()
    
    # Direcciones iniciales de envío
    
    addresses = [
      '0xF874CC8A4A035ee8BB2e264600cc281Bae171321',
      '0x0E1A67bC08aE03E5F9FE9857e575C702326Df72E',
      '0xdCd2F6210000F5c1c1e97BDB08F2c8E0879aABb5',
      '0xa03af4993912C6b8c48Cb3AB234D7101A514714E'
    ]
    
    # Enviamos tokens iniciales a las paper wallet que
    for addr in addresses:
      token.transfer(addr, 12345, {'from': accounts[0].address})
    
    balance_restante = token.balanceOf(root)
    token.setMaxBalancePerAddress(alltokens, {"from": root})
    
    token.transfer(faucet.address, balance_restante, {'from': root })
    token.setMaxBalancePerAddress(10_000_000000, {"from": root})

    print(f"Token - address: {token.address}\nFaucet - address: {faucet.address}")

def main():

    print("Desplegando contratos")
    DeployContracts()
