import requests
import json
from web3 import Web3
from datetime import datetime

# mainnet urls
chain_url = {
    "harmony": "https://api.harmony.one",
    "avalanche": "https://api.avax.network/",
    "fantom": "https://xapi.fantom.network/",
}

current_chain = "harmony"
web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))

# get Historical DFKGOLD/JEWEL transaction history
token_pair_address = "0x321EafB0aeD358966a90513290De99763946A54b"
from pyhmy import account

# if tx_list == tx_list2 when page size increase means we have already reached all transaction for this wallet
# everything in DFK involves HRC20 as it only involves jewel (HRC20) and other items (HRC20 too)

transactions = 1000
tx_list = account.get_transaction_history(
    token_pair_address,
    page=0,
    page_size=transactions,
    include_full_tx=False,
    endpoint=chain_url[current_chain],
)
tx_list2 = account.get_transaction_history(
    token_pair_address,
    page=0,
    page_size=transactions + 1000,
    include_full_tx=False,
    endpoint=chain_url[current_chain],
)

while tx_list != tx_list2:
    transactions += 1000
    tx_list = account.get_transaction_history(
        token_pair_address,
        page=0,
        page_size=transactions,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )
    tx_list2 = account.get_transaction_history(
        token_pair_address,
        page=0,
        page_size=transactions + 1000,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )

print(len(tx_list))
print(tx_list)

tx_hash = "0xa2b868114199e2c1aa49f627873d48aaa9992c1b56e83c913c8d2685787e564b"


def get_DFKGOLD_price(block_number):
    UniswapV2Factory_address = "0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7"
    UniswapV2Factory_abi = json.load(open("abi/UniswapV2Factory.json"))
    contract = web3.eth.contract(address=UniswapV2Factory_address, abi=UniswapV2Factory_abi)
    # functions = get_functions(contract)
    DFKGOLD_address = web3.toChecksumAddress("0x3a4edcf3312f44ef027acfd8c21382a5259936e7")
    JEWEL_address = web3.toChecksumAddress("0x72Cb10C6bfA5624dD07Ef608027E366bd690048F")
    TokenPair_address = contract.functions.getPair(DFKGOLD_address, JEWEL_address).call()
    # Resulting Pair Address 0x321EafB0aeD358966a90513290De99763946A54b
    print(TokenPair_address)
    UniswapV2Pair_abi = json.load(open("abi/UniswapV2Pair.json"))
    # print(token_pair)
    LP_contract = web3.eth.contract(address=TokenPair_address, abi=UniswapV2Pair_abi)
    tokens_reserve = LP_contract.functions.getReserves().call(block_identifier=block_number)
    print(tokens_reserve)
    return tokens_reserve