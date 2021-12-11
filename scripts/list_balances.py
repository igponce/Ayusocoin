# Lista balances (ether) de las cuentas

from brownie import Ayusocoin, Faucet, accounts

# Imprime informacion sobre red y cuentas

def main():
  for acc in accounts:
    print(f"Wallet: {acc}:\n\tEther: {acc.balance()}")

