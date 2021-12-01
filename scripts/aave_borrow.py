# WETH is ERC20 version of ETH


from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import network, config, interface
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_Address = config["networks"][network.show_active()]["weth_token"]

    # Get Weth
    # Get ERC20
    if network.show_active() in ["mainnet-fork"]:
        get_weth()  # Get .1 WETH

    # Deposit WETH into AAVE
    # Get Lending Pool Contract
    lending_pool = get_lending_pool()

    # Approve another contract using our ERC20 token
    approve_erc20(amount, lending_pool.address, erc20_Address, account)

    print("Depositing ETH now")
    tx = lending_pool.deposit(
        erc20_Address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited")

    # Onto borrow. But how much can we actually?
    # We need user account data.
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

    print("Let's borrow DAI")
    # Will return ETH/DAI
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    print(f"The current DAI/ETH Price is {dai_eth_price}")

    borrow_buffer = 0.95
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * borrow_buffer)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # Now we will borrow
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI")


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"the DAI/ETH price is {converted_latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_colalteral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_colalteral_eth = Web3.fromWei(total_colalteral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")

    print(f"You have {total_colalteral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} ETH")

    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # Find out where aave is located
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
