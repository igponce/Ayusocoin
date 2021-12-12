
from brownie import Ayusocoin, Faucet, accounts, web3, network
import os

"""
Desplegamos contratos SOLO en nuestra testnet privada.
En la red publica hay que usar Contract.at("address").
"""

def DeployContracts(account):
   
    # Despliega el token 
    token = account.deploy(Ayusocoin)

    # Despliega el faucet - damos 1000.000000 tokens por address.
    faucet = account.deploy(Faucet,token.address, 1000_0000000)
    
    root = account.address
    
    alltokens = token.totalSupply()
    
    # Direcciones iniciales de envío
    
    addresses = [
      '0xF874CC8A4A035ee8BB2e264600cc281Bae171321',
      '0x0E1A67bC08aE03E5F9FE9857e575C702326Df72E',
      '0xdCd2F6210000F5c1c1e97BDB08F2c8E0879aABb5',
      '0xa03af4993912C6b8c48Cb3AB234D7101A514714E'
    ]
    
    # Enviamos tokens iniciales a las paper wallet
    for addr in addresses:
      token.transfer(addr, 12345, {'from': account.address})
    
    balance_restante = token.balanceOf(root)
    token.setMaxBalancePerAddress(alltokens, {"from": root})
    
    token.transfer(faucet.address, balance_restante, {'from': root })

    print(f"Token - address: {token.address}\nFaucet - address: {faucet.address}")

    return token, faucet


def main():

    if (network.Chain().id == 1337):
      # Development / Integration network
      # Tenemos dos direcciones ETH de más
      # accounts[10] -> para test de metamask
      # accounts[11] -> para desplegar contratos
      accounts[0].transfer(accounts[-1].address, accounts[0].balance() / 2)
      accounts[1].transfer(accounts[-2].address, accounts[1].balance() / 2)
      deployment_account = accounts[11]
      token, faucet = DeployContracts(deployment_account) 
    else:
      pk = os.environ['PRIVATE_KEY'] # RAISE EXCEPTION if not exists
      deployment_account = accounts.add(pk) 
      token = Ayusocoin.at('0xa745005a2764cCbFEB1a8c6fCa178F896aF5d777')
      faucet = Faucet.at('0x0b70A904C77b90eBa8c3619dbE810669c193917d')
    
    # Recogemos datos antes de operar   

    saldo_despliegue = deployment_account.balance() 
    saldo_faucet = token.balanceOf(faucet.address)
    saldo_tope = token.maxbalance_per_addr()
    total_tokens = token.totalSupply()

    # Confirmación a mano antes de hacer el despliegue!

    expected = "confirmar"
    print(f"""
    ##############################################################  
    
    NEW FAUCET

       RED: {network.Chain().id}
    
    Dirección: {deployment_account.address} (saldo: {web3.fromWei(saldo_despliegue, 'ether')} Eth)

       Direcciones contratos:

          - {deployment_account.get_deployment_address(0)} - Token
               Max Balance Per Address = {saldo_tope}
          - {faucet.address} - Faucet
               Saldo Faucet: {saldo_faucet}

      Gas: {deployment_account.estimate_gas()}

    ##############################################################

    Escribe "{expected}"" para desplegar
    """)

    if input("confirmar despliegue: ") != expected:
      exit(99)

    ## Deshacemos operaciones ##

    faucet2 = deployment_account.deploy(Faucet,token.address, 1000_0000000)

    tx = faucet.Recovertokens({'from': deployment_account})
    print(tx.info())

    tx = token.transfer(faucet2.address, saldo_faucet / 2)
    print(tx.info())


    saldo_final_despliegue = deployment_account.balance()

    print(f"""
    ###############################################################
    
    Estado final:

       Saldo Faucet: {token.balanceOf(faucet.address)} 
       Saldo Faucet2: {token.balanceOf(faucet2.address)}
       Saldo tokens Despliegue: {token.balanceOf(deployment_account)}

       Eth Consumido: {  web3.fromWei(saldo_despliegue-saldo_final_despliegue, 'ether') }

    #################################################################
    """)


