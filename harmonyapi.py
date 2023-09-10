import requests
import json

wallet_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
# 0x900554698f30c589389fb4d860Dfa932f1d87039 wallet 1 - about 598  txn

# 0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F wallet 2 - about 2000 txn
#   one1ct8umgxdnq79ayswq5lsnpts330yyre0hcrwwq

# 0x9950b438c5947C5cA7cDC225292f56B50a5c77B0 wallet 3 - about 1    txn


harmony_url = "https://api.s0.t.hmny.io/"


def get_transaction_count(wallet_address, harmony_url):
    txn_history = {
        "jsonrpc": "2.0",
        "method": "hmyv2_getTransactionsCount",
        "params": [wallet_address, "1"],
        "id": 1,
    }
    response = requests.post(harmony_url, json=txn_history).json()
    print(type(response))
    print(response)
    transaction_count = response
    print(transaction_count)
    # print("transaction_count = " + str(transaction_count))
    return transaction_count


def get_harmony_txHistory(wallet_address, harmony_url):
    txn_history = {
        "jsonrpc": "2.0",
        "method": "hmy_getTransactionsHistory",
        "params": [
            {
                "address": wallet_address,
                "pageIndex": 0,
                "pageSize": 2000,
                # "fullTx": true,
                "txType": "ALL",
                "order": "ASC",
            }
        ],
        "id": 1,
    }
    response = requests.post(harmony_url, json=txn_history).json()
    print(type(response))
    tx_list = response["result"]["transactions"]
    print(tx_list)
    print("tx_list = " + str(len(tx_list)))
    return tx_list


tx_list = get_harmony_txHistory(wallet_address, harmony_url)

# transaction_count = get_transaction_count(wallet_address, harmony_url)

