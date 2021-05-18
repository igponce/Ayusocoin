import pytest
import logging
from brownie import accounts, Ayusocoin, Airdrop, exceptions

@pytest.fixture
def token():
   return accounts[0].deploy(Ayusocoin)

@pytest.fixture
def airdrop():
   return accounts[0].deploy(Airdrop)

def test_contract_deployer_tiene_todo_balance(token):
    assert token.balanceOf(accounts[0].address) == 47000000 * 1000000 * 1000


def test_erc20_transfer(token):

    tokens_ok = 2000000000

    start_balance = token.balanceOf(accounts[0])
    assert token.balanceOf(accounts[1].address) == 0

    token.transfer(accounts[1].address, tokens_ok, {'from': accounts[0].address})
    assert token.balanceOf(accounts[1].address) == tokens_ok
    assert token.balanceOf(accounts[0].address) + token.balanceOf(accounts[1].address) == start_balance


def test_erc20_transfer_sobre_saldo(token):

   start_balance = token.balanceOf(accounts[0])
   
   with pytest.raises(exceptions.VirtualMachineError):
      token.transfer(accounts[1].address, 
                     start_balance + 1,
                     {'from': accounts[0].address})
   

def test_erc20_transfer_sobre_saldo(token):

   start_balance = token.balanceOf(accounts[0])
   with pytest.raises(exceptions.VirtualMachineError):
       ret = token.transfer(
                     accounts[1].address, 
                     start_balance + 1,
                     {'from': accounts[0].address, 'origin': accounts[2].address}
            )


def test_erc20_transfer_limits(token): 

    tokens_ko = 1 + (10000 * 1000000)
    balance0 = token.balanceOf(accounts[0])
    balance2 = token.balanceOf(accounts[2])

    assert balance2 == 0
    
    with pytest.raises(exceptions.VirtualMachineError):
       numTokens = 1_000 * 1000000 # 10.000 con 6 decimales 
       token.transfer(accounts[2].address, tokens_ko, {'from': accounts[0].address})

    assert balance0 == token.balanceOf(accounts[0])
    assert balance2 == token.balanceOf(accounts[2])


def test_erc20_transfer_from_sin_permiso(token):
    # Esto se tiene que hacer desde un contrato pero vamos a simularlo

    orig, dest = accounts[0].address, accounts[1].address
    origbal, destbal = token.balanceOf(orig), token.balanceOf(dest)
   
    with pytest.raises(exceptions.VirtualMachineError):
       token.transferFrom(orig, dest, 1000)

    # Balances sin cambiar
    assert origbal == token.balanceOf(orig)
    assert destbal == token.balanceOf(dest)

def test_erc20_transferFrom_sobre_permiso (token):
    # Esto se tiene que hacer desde un contrato pero vamos a simularlo

    orig, dest = accounts[0].address, accounts[1].address
    origbal, destbal = token.balanceOf(orig), token.balanceOf(dest)

    numtokens = 100_000_000 # 100.000000 tokens

    token.approve(dest, numtokens)
   
    with pytest.raises(exceptions.VirtualMachineError):
       token.transferFrom(orig, dest, numtokens + 1)

    # Balances sin cambiar
    assert origbal == token.balanceOf(orig)
    assert destbal == token.balanceOf(dest)

    # transferencia dentro de lo permitido
    token.transferFrom(orig, dest, numtokens)
    assert destbal + numtokens == token.balanceOf(dest)
    assert origbal - numtokens == token.balanceOf(orig)

def test_erc20_transferFrom_cambia_allowance(token):

    numtokens = 100_000_000;
    orig = accounts[0].address;
    dest = accounts[5].address;
    token.approve(dest, numtokens)
    token.transferFrom(orig, dest, numtokens / 2)

    assert token.allowance(orig, dest) == numtokens / 2

def test_erc20_allowance_ilimitado(token):
    # Cuando el allowance es uint256max, no se cambia.
    allowance_ilimitado = 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff
    numtokens = 100_000_000;
    orig = accounts[0].address;
    dest = accounts[6].address;
    token.approve(dest, allowance_ilimitado)
    assert token.allowance(orig, dest) == allowance_ilimitado
     

def test_totalSupply(token):

   token.totalSupply() < token.balanceOf(accounts[0].address)
