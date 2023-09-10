from web3 import Web3
from datetime import datetime

# print(serendale_contracts)

# mainnet urls
chain_url = {
    "harmony": "https://api.harmony.one",
    "avalanche": "https://api.avax.network/",
    "fantom": "https://xapi.fantom.network/",
}

current_chain = "harmony"
web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))

print("Please input wallet address here")
wallet_address = "0x900554698f30c589389fb4d860Dfa932f1d87039"
# wallet_address = input()

# 0x900554698f30c589389fb4d860Dfa932f1d87039 wallet 1 - about 598  txn
# 0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F wallet 2 - about 2000 txn
# 0x9950b438c5947C5cA7cDC225292f56B50a5c77B0 wallet 3 - about 1    txn


def generate_transaction_history_harmony():
    from pyhmy import account

    # if tx_list == tx_list2 when page size increase means we have already reached all transaction for this wallet
    # everything in DFK involves HRC20 as it only involves jewel (HRC20) and other items (HRC20 too)

    transactions = 1000
    tx_list = account.get_transaction_history(
        wallet_address,
        page=0,
        page_size=transactions,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )
    tx_list2 = account.get_transaction_history(
        wallet_address,
        page=0,
        page_size=transactions + 1000,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )

    while tx_list != tx_list2:
        transactions += 1000
        tx_list = account.get_transaction_history(
            wallet_address,
            page=0,
            page_size=transactions,
            include_full_tx=False,
            endpoint=chain_url[current_chain],
        )
        tx_list2 = account.get_transaction_history(
            wallet_address,
            page=0,
            page_size=transactions + 1000,
            include_full_tx=False,
            endpoint=chain_url[current_chain],
        )

    print("Total Harmony transaction for on wallet = " + str(len(tx_list)))
    return tx_list

if current_chain == "harmony":
    wallet_transactions = generate_transaction_history_harmony()
elif current_chain == "avalanche":
    print("Currently Not Supported")
elif current_chain == "fantom":
    print("Currently Not Supported")
else:
    print("Please input a valid chain")

#################################################################################################