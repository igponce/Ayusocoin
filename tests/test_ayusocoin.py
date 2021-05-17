import pytest

from brownie import accounts, Ayusocoin, Airdrop

@pytest.fixture
def token():
   return accounts[0].deploy(Ayusocoin)

@pytest.fixture
def airdrop():
   return accounts[0].deploy(Airdrop)

def test_contract_deployer_tiene_todo_balance(token):
    assert token.balanceOf(accounts[0].address) == 47000000 * 1000000 * 1000
