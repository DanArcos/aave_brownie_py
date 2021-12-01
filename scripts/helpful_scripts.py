from brownie import interface, config, network, accounts

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=0, id=None):

    # If there's a value for index use accounts[index]
    if index:
        print("Return account as index value was supplied")
        return accounts[index]

    # If there's an id supplied, load the account based on the id value
    if id:
        print("Return account as id value was supplied")
        return accounts.load(id)

    # Otherwise it must be implied that its a local development blockchain
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("We are working on a local blockchain")
        print("Returning accounts[0]")
        return accounts[0]

    # If nothing else, return from testnet
    # From key would be our private key
    if network.show_active() in config["networks"]:
        print("We are working on a test net")
        return accounts.add(config["wallets"]["from_key"])
    return None
