# Despliegue

from brownie import Ayusocoin, Faucet, accounts

token = accounts[0].deploy(Ayusocoin)
faucet = accounts[0].deploy(Faucet,token.address, 100_000000)

alltokens = token.totalSupply()

# Direcciones iniciales de envío

addresses = [
  '0x0E1A67bC08aE03E5F9FE9857e575C702326Df72E',
  '0xdCd2F6210000F5c1c1e97BDB08F2c8E0879aABb5',
  '0xa03af4993912C6b8c48Cb3AB234D7101A514714E'
]

# Enviamos tokens iniciales a las paper wallet que
for addr in addresses:
  token.transfer(addr, 1000_000, {'from': accounts[0].address})

balance_restante = token.getBalance({'from': accounts[0].address})
token.transfer(faucet.address, balance_restante, {'from': accounts[0].address})
token.setMaxBalancePerAddress(cantidad_max, {"from": root})
