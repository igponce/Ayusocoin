# Despliegue

from brownie import Ayusocoin, Faucet, accounts, web3
import os

    
def main():

    pk = os.environ.get("PRIVATE_KEY")
    deployment_account = accounts.add(pk) if pk != None else accounts[0]
    root = deployment_account.address

    saldo = deployment_account.balance() 
    # Confirmación a mano antes de hacer el despliegue!

    token = Ayusocoin.at("0xa745005a2764cCbFEB1a8c6fCa178F896aF5d777") 
    faucet = Faucet.at("0x0b70A904C77b90eBa8c3619dbE810669c193917d")
    
    
    alltokens = token.totalSupply()
    limite_por_direccion = token.maxbalance_per_addr()

    root_balance = token.balanceOf(root)
    faucet_balance = token.balanceOf(faucet.address)


    print(f"""
    ##############################################################  
    Desplegando contratos
    
    Dirección: {deployment_account.address} (saldo: {web3.fromWei(saldo, 'ether')} Eth)

       Direcciones contratos:

          - {deployment_account.get_deployment_address(0)} - Token
          - {deployment_account.get_deployment_address(1)} - Faucet

      Gas: {deployment_account.estimate_gas()}

      Max_Balance_Per_address {limite_por_direccion}

      Root_balance => {root_balance}
      Faucet_balance => {faucet_balance}


    ##############################################################

    """)


