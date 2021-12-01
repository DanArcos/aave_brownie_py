Learn how to programmatically work with Aave. Conceptually we can work with other protocols as well

1. Swap ETH for WETH - done with get_weth()

2. Deposit some ETH into Aave
2. Borrow some asset with the ETH collateral
    1. Sell that borrowed asset. (Short Selling)
3. Repay everything back.

Testing:
Unit Tests: Mainnet-fork. We don't need to use mocks. If you have no oracles, we can fork the mainnet.
Integration Test: Kovan