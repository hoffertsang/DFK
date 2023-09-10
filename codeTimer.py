import timeit

start = timeit.default_timer()

# Start Timer

from web3 import Web3
from datetime import datetime
from DFK_addresses import serendale_contracts, serendale_erc20_only

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
    tx_list = generate_transaction_history_harmony()
elif current_chain == "avalanche":
    print("Currently Not Supported")
elif current_chain == "fantom":
    print("Currently Not Supported")
else:
    print("Please input a valid chain")

#################################################################################################

# Once we get a tx_list for an associated address (the list name will be the same for all chains)


def get_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)

    timestamp_unix = web3.eth.get_block(block_number).timestamp

    timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime("%Y-%m-%d %H:%M:%S")
    # print(timestamp)
    return timestamp


def scan_erc20_log(receipt, tx_hash):
    timestamp = get_timestamp(tx_hash)
    transactions = []
    for log in receipt["logs"]:
        try:
            token = serendale_erc20_only[log["address"]]
            address_from = log.topics[1]
            address_to = log.topics[2]
            value = web3.toInt(hexstr=log.data)
            transactions += [[timestamp, address_from, address_to, value, token]]
            # print([timestamp, address_from, address_to, value, token])
        except:
            pass
    return transactions


def DFK_filter(tx_list):
    print("Pulling transaction details...")
    DFK_transactions = {}
    for tx_hash in tx_list:

        receipt = web3.eth.get_transaction_receipt(tx_hash)
        # print(receipt)

        for key in serendale_contracts.keys():
            if key == receipt["from"]:
                # only find block and timestamp when it is DFK contract
                DFK_transactions[tx_hash] = scan_erc20_log(receipt, tx_hash)
                print(DFK_transactions[tx_hash])
                break
            elif key == receipt["to"]:
                # only find block and timestamp when it is DFK contract
                DFK_transactions[tx_hash] = scan_erc20_log(receipt, tx_hash)
                print(DFK_transactions[tx_hash])
                break
            else:
                try:
                    key == receipt.logs[0]["address"]
                    # only find block and timestamp when it is DFK contract
                    DFK_transactions[tx_hash] = scan_erc20_log(receipt, tx_hash)
                    print(DFK_transactions[tx_hash])
                    break

                except:
                    pass

    print("Completed!")
    return DFK_transactions


DFK_transactions = DFK_filter(tx_list)
# print(DFK_transactions)
print("Total DFK Transactions = " + str(len(DFK_transactions)))

# End Timer

stop = timeit.default_timer()
print("Time: ", stop - start)

