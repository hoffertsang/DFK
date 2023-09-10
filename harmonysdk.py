from web3 import Web3

# basic stuff
chain_url = {
    "harmony": "https://harmony-0-rpc.gateway.pokt.network",
    "avalanche": "https://api.avax.network/",
    "fantom": "https://xapi.fantom.network/",
}
current_chain = "harmony"
web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))

wallet_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
# 0x900554698f30c589389fb4d860Dfa932f1d87039 wallet 1 - about 598  txn
# 0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F wallet 2 - about 2000 txn
# 0x9950b438c5947C5cA7cDC225292f56B50a5c77B0 wallet 3 - about 1    txn

# Harmony python SDK
from pyhmy import account

# Transaction History Hashes
transactions = 2000
tx_list = account.get_transaction_history(
    wallet_address,
    page=0,
    page_size=transactions,
    include_full_tx=False,
    endpoint=chain_url[current_chain],
)

transaction_history_count = len(tx_list)
print("transaction_history_count = " + str(transaction_history_count))

# Transactions
test_net = chain_url[current_chain]
test_address = wallet_address

tx_count = account.get_transactions_count(
    test_address, tx_type="ALL", endpoint=test_net
)

print("tx_count = " + str(tx_count))

balance = account.get_balance(test_address, endpoint=test_net)
print("balance = " + str(balance))
