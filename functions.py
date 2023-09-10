from web3 import Web3

def transaction_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)

    timestamp_unix = web3.eth.get_block(block_number).timestamp

    timestamp = datetime.utcfromtimestamp(timestamp_unix).strftime("%Y-%m-%d %H:%M:%S")
    # print(timestamp)
    return timestamp
