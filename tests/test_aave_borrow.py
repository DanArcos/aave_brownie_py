import web3
from brownie import interface, config, network
from scripts.aave_borrow import get_asset_price, get_lending_pool, approve_erc20
from scripts.helpful_scripts import get_account
from web3 import Web3


def test_get_asset_price():
    asset_price = get_asset_price()
    print(f"The latest DAI/ETH price is {asset_price}")
    assert asset_price > 0


def test_get_lending_pool():
    lending_pool = get_lending_pool()

    # Assert that the lending pool has something in it
    assert lending_pool != None


def test_approve_erc20():
    # ARRANGE
    # Get the account
    account = get_account()

    # Get the lending pool
    lending_pool = get_lending_pool()

    # Get the ERC20 addrss
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    # Get the amount
    amount = 0.1
    amount = Web3.toWei(amount, "ether")

    # ACT
    approved = approve_erc20(amount, lending_pool.address, erc20_address, account)
    print(f"Approved is: {approved}")

    # ASSERT
    assert approved != None
