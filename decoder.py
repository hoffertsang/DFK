from web3 import Web3
import json
from DFK_addresses import serendale_contracts, serendale_erc20_only

web3 = Web3(Web3.HTTPProvider("https://api.s0.t.hmny.io/"))


def get_ERC20_balance(token_address, wallet_address):
    with open("abi/ERC20.json") as f:
        erc20_abi = json.load(f)

    checksum_token_address = Web3.toChecksumAddress(token_address)
    contract = web3.eth.contract(address=checksum_token_address, abi=erc20_abi)

    token_balance = contract.functions.balanceOf(wallet_address).call()

    if (
        serendale_erc20_only[token_address] == "Jewel"
        or serendale_erc20_only[token_address] == "xJewel"
    ):
        token_balance = web3.fromWei(token_balance, "ether")

    wallet_balance = [serendale_erc20_only[token_address], token_balance]
    return wallet_balance


def get_wallet_balance(wallet_address):
    wallet_balance = []
    for key in serendale_erc20_only.keys():
        wallet_balance += [get_ERC20_balance(key, wallet_address)]
        print(get_ERC20_balance(key, wallet_address))
    return wallet_balance


# wallet_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"  # wallet 2000 trnasctions
# wallet_balance = get_wallet_balance(wallet_address)

#########################################################################################


# contract_address = "0xdb30643c71ac9e2122ca0341ed77d09d5f99f924" master gardener contract


def get_functions(contract):
    for function in contract.all_functions():
        print(function)
    return


# contract_abi = json.load(open("abi/MasterGardener.json"))
# contract_address = web3.toChecksumAddress("0xdb30643c71ac9e2122ca0341ed77d09d5f99f924")
# contract = web3.eth.contract(address=contract_address, abi=contract_abi)
# get_functions(contract)
# tx_hash = "0xea4b827431c316a6fb47b07a22594aac30a9e294e5af6806db59189deebd0d2e"
# receipt = web3.eth.get_transaction_receipt(tx_hash)


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


# # current block = 20819027
blockNumber = web3.eth.block_number #get latest block
Gold_price = get_DFKGOLD_price(block_number= blockNumber)
error = False
while error == False:
    print("blockNumber = " + str(blockNumber))
    try:
        Gold_price = get_DFKGOLD_price(block_number= blockNumber)
        blockNumber -= 1
    except:
        error = True

print(blockNumber)

# last run 20819142