# Despliegue

from brownie import Ayusocoin, Faucet, accounts, web3, network
import os


def DeployContracts(account):

    import pdb; pdb.set_trace()
    
    token = Ayusocoin.at('0xa745005a2764cCbFEB1a8c6fCa178F896aF5d777')
    # token = account.deploy(Ayusocoin)
    root = account.address
    alltokens = token.balanceOf(root)

    #token.setMaxBalancePerAddress(alltokens, {"from": root})
    """
    token.transfer(
      '0xF874CC8A4A035ee8BB2e264600cc281Bae171321',
      123456_000000 ,
      {'from': root, 'required_confs': 0 })
    """
    faucet = account.deploy(Faucet,token.address, 1000_0000000)
    
    alltokens = token.totalSupply()
    
    # Direcciones iniciales de envío
    
    addresses = [
      '0xF874CC8A4A035ee8BB2e264600cc281Bae171321',
      '0x0E1A67bC08aE03E5F9FE9857e575C702326Df72E',
      '0xdCd2F6210000F5c1c1e97BDB08F2c8E0879aABb5',
      '0xa03af4993912C6b8c48Cb3AB234D7101A514714E',
      '0x01e01E209557230996a30C01555B0799e9C48216'
    ]
    
    # Enviamos tokens iniciales a las paper wallet
    for addr in addresses:
      token.transfer(addr, 12345, {'from': account.address, 'required_confs': 0})
    
    balance_restante = token.balanceOf(root)
    token.setMaxBalancePerAddress(alltokens, {"from": root, 'required_confs': 0 })
    
    token.transfer(faucet.address, balance_restante, {'from': root, 'required_confs': 0 })
    token.setMaxBalancePerAddress(10_000_0000000, {"from": root, 'required_confs': 0 })

    print(f"""
    ----------[ RESULTADOS ]-------------
       Token  - address: {token.address}
       Faucet - address: {faucet.address}
    ----------[ Resultados ]-------------
    """)

def main():

    if (network.Chain().id == 1337):
      # Development / Integration network
      # Tenemos dos direcciones ETH de más
      # accounts[11] -> para test de metamask
      # accounts[12] -> para desplegar contratos
      accounts[0].transfer(accounts[-1].address, accounts[0].balance() / 2)
      accounts[1].transfer(accounts[-2].address, accounts[1].balance() / 2)
    
    pk = os.environ.get('PRIVATE_KEY')
    deployment_account = accounts.add(pk) if pk != None else accounts[-1]

    saldo = deployment_account.balance() 
    # Confirmación a mano antes de hacer el despliegue!

    expected = "confirmar"
    print(f"""
    ##############################################################  
    Desplegando contratos

       RED: {network.Chain().id}
    
    Dirección despliegue: {deployment_account.address} (saldo: {web3.fromWei(saldo, 'ether')} Eth)

       Direcciones contratos:

          - f{deployment_account.get_deployment_address(0)} - Token

      Gas: {deployment_account.estimate_gas()}

    ##############################################################

    Escribe "{expected}"" para desplegar
    """)

    if input("confirmar despliegue: ") != expected:
      exit(99)

    DeployContracts(deployment_account)
