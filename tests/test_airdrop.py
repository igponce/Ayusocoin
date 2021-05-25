import pytest
import logging
from brownie import accounts, Airdrop, Ayusocoin, exceptions

@pytest.fixture
def token_airdrop():
   token = accounts[0].deploy(Ayusocoin)
   airdrop = accounts[0].deploy(Airdrop,token.address, 100_000000)
   token.transfer(airdrop.address, 10000_000000, {'from': accounts[0].address})
   return (token, airdrop)

def test_airdrop_has_balance(token_airdrop):
    token, airdrop = token_airdrop
    assert token.balanceOf(airdrop.address) > 0

def test_airdrop_can_claim(token_airdrop):
    token, airdrop = token_airdrop 
    wallet = accounts[1].address
    assert token.balanceOf(wallet) == 0
    airdrop.Claim(wallet, {'from': wallet})
    balance = token.balanceOf(wallet)
    claimed = airdrop.ClaimedAmount(wallet)

    assert balance > 0
    assert claimed > 0
    assert balance == claimed


def test_airdrop_clain_only_once(token_airdrop):
    token, airdrop = token_airdrop

    wallet = accounts[2].address
    balance_before = token.balanceOf(wallet)

    airdrop.Claim(wallet, {'from': wallet})
    balance_afterclaim1 = token.balanceOf(wallet)

    with pytest.raises(exceptions.VirtualMachineError):
       airdrop.Claim(wallet, {'from': wallet})

    balance_afterclaim2 = token.balanceOf(wallet)
    claimed = airdrop.ClaimedAmount(wallet) == 0

    assert balance_before == 0
    assert balance_afterclaim1 > 0
    assert balance_afterclaim2 == balance_afterclaim1

