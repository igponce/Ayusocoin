# Despliegue

from brownie import Ayusocoin, Faucet, accounts, web3, network

from brownie.network import gas_price
from brownie.network.gas.strategies import GethMempoolStrategy
import os
import csv
from time import sleep


def Reyes2022(account, holders):

    # gas_strategy = GethMempoolStrategy(position=272) # ExponentialScalingStrategy("500 gwei", "1100 gwei")
    # gas_price(gas_strategy)

    token = Ayusocoin.at('0xa745005a2764cCbFEB1a8c6fCa178F896aF5d777')
    root = account.address
    initial_balance = token.balanceOf(root)

    # Pre-check
    maxbal = token.maxbalance_per_addr()
    alltokens = token.totalSupply()

    print(f"Prerequisite: max_balance({maxbal} == totalSupply({alltokens})")

    numtransfer = 0
    acum = 0

    for dest, balance in csv.reader(holders):
       wei = int(balance) * (10**8) if balance!="18080502" else int(balance) * (10**7) # Ponemos un cero de mas (no es culpa mía, son los reyes) 

       realbalance = token.balanceOf(dest)
       if realbalance == 0:
          print(f"Enviando a: {dest} , {wei} tokens")
          tx = token.transfer(dest, wei, {'from': account, 'required_confs': 0, gas_price: 70123 })
          numtransfer+=1
          acum += wei
       else:
          print(f"Balance {dest} = {realbalance} wei - skipping")

       sleep(7)

   
    print(f"""
    ----------[ RESULTADOS ]-------------
       Token  - address: {token.address}
       Balance Inicial: {initial_balance}
       Transferencias: {numtransfer}
       Total acumulado: {acum / (10**7)} (token)
    ----------[ Resultados ]-------------
    """)

def main():


    pk = os.environ.get('PRIVATE_KEY')
    deployment_account = accounts.add(pk) if pk != None else accounts[-1]

    saldo = deployment_account.balance() 
    # Confirmación a mano antes de hacer el despliegue!

    if (network.Chain().id == 1337):
      # Development / Integration network
      # Tenemos dos direcciones ETH de más
      # accounts[11] -> para test de metamask
      # accounts[12] -> para desplegar contratos
      accounts[0].transfer(accounts[-1].address, accounts[0].balance() / 2)
      accounts[1].transfer(accounts[-2].address, accounts[1].balance() / 2)

      # Desplegamos contrato para test solo en la red de pruebas
      token = deployment_account.deploy(Ayusocoin)
      alltokens = token.totalSupply()
      token.setMaxBalancePerAddress(alltokens, {'from': deployment_account})      
    
    holders = []
    with open('holders.csv', 'r') as fp:
       holders = fp.readlines()

    expected = "confirmar"
    print(f"""
    ##############################################################  
    Desplegando contratos

       RED: {network.Chain().id}
    
    Dirección despliegue: {deployment_account.address} (saldo: {web3.fromWei(saldo, 'ether')} Eth)

      Transacciones: {len(holders)}

      Gas: {deployment_account.estimate_gas()}

    ##############################################################

    Escribe "{expected}"" para desplegar
    """)

    if input("confirmar despliegue: ") != expected:
      exit(99)

    Reyes2022(deployment_account, holders)

    print("\nDone")
