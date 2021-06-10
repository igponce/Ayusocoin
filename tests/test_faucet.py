import pytest
import logging
from brownie import accounts, Faucet, Ayusocoin, exceptions

@pytest.fixture
def token_faucet():
   token = accounts[0].deploy(Ayusocoin)
   faucet = accounts[0].deploy(Faucet,token.address, 100_000000)
   token.transfer(faucet.address, 10000_000000, {'from': accounts[0].address})
   return (token, faucet)

def test_faucet_has_balance(token_faucet):
    token, faucet = token_faucet
    assert token.balanceOf(faucet.address) > 0

def test_faucet_can_claim(token_faucet):
    token, faucet = token_faucet 
    wallet = accounts[1].address
    assert token.balanceOf(wallet) == 0
    faucet.Claim(wallet, {'from': wallet})
    balance = token.balanceOf(wallet)
    claimed = faucet.ClaimedAmount(wallet)

    assert balance > 0
    assert claimed > 0
    assert balance == claimed


def test_faucet_clain_only_once(token_faucet):
    token, faucet = token_faucet

    wallet = accounts[2].address
    balance_before = token.balanceOf(wallet)

    faucet.Claim(wallet, {'from': wallet})
    balance_afterclaim1 = token.balanceOf(wallet)

    with pytest.raises(exceptions.VirtualMachineError):
       faucet.Claim(wallet, {'from': wallet})

    balance_afterclaim2 = token.balanceOf(wallet)
    claimed = faucet.ClaimedAmount(wallet) == 0

    assert balance_before == 0
    assert balance_afterclaim1 > 0
    assert balance_afterclaim2 == balance_afterclaim1

