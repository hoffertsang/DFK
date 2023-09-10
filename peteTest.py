from web3 import Web3
from DFK_addresses import serendale_contracts, serendale_erc20_only


chain_url = {
    "harmony": "https://api.harmony.one",
    "avalanche": "https://api.avax.network/",
    "fantom": "https://xapi.fantom.network/",
}

current_chain = "harmony"
web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))

tx_hash = "0x0ef364d0047ffd4c70a4ad8178758cc0f419447b8f5b61977b9295bc642b64fc"
receipt = web3.eth.get_transaction_receipt(tx_hash)
print(type(receipt))
# print(receipt)

# event quest = "0x0ef364d0047ffd4c70a4ad8178758cc0f419447b8f5b61977b9295bc642b64fc"
# jewel transfer = "0x4eec584fda88e8e123c4c598275fab118520b080de4e68be6d0fd4cfa79fdd27"


def get_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)

    timestamp_unix = web3.eth.get_block(block_number).timestamp

    from datetime import datetime

    timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime("%Y-%m-%d %H:%M:%S")
    # print(timestamp)
    return timestamp


# scan through the logs to find ERC20 tokens


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
            print([timestamp, address_from, address_to, value, token])
        except:
            pass
    return transactions


# print(scan_erc20_log(receipt, tx_hash))

dict = {
    "pete": 1,
    "hoffer": 2,
}

if "random" in dict:
    print("yes")
else:
    print("no")
