from web3 import Web3
#from datetime import datetime
import datetime
from transactionHistory import wallet_transactions, web3
from contract_address import serendale_contracts, serendale_erc20_only
from bs4 import BeautifulSoup 
from pycoingecko import CoinGeckoAPI 
import requests

def get_jewel_usd_price():
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime("12-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
    end = datetime.datetime.strptime("25-12-2021", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

    x = list(range(len(date_generated)))
    jewel_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated[:-1]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        jewel_usd[count] = (cg.get_coin_history_by_id(id='defi-kingdoms', date=date.strftime(x[count])))['market_data']['current_price']['usd']
    jewel_usd[len(date_generated)-1] = cg.get_price(ids='defi-kingdoms', vs_currencies='usd')["defi-kingdoms"]["usd"]
    return jewel_usd

def get_dfktears_jewel_price():  ##maybe wrong
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime("13-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
    end = datetime.datetime.strptime("25-12-2021", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

    x = list(range(len(date_generated)))
    dfktears_jewel = list(range(len(date_generated)))
    count = -1
    for date in date_generated[0:5]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=date.strftime(x[count])))['market_data']['current_price']['eur'] 
    dfktears_jewel[5] = 0.22827 #18/12/2021 no price history
    count = 5
    for date in date_generated[6:len(date_generated)-1]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=date.strftime(x[count])))['market_data']['current_price']['eur']
    dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]
    return dfktears_jewel

dfktears_jewel = get_dfktears_jewel_price()
jewel_usd = get_jewel_usd_price()

def get_jewel_usd_price_date(date):
    start =  start = datetime.datetime.strptime(date, "%d-%m-%Y")
    end = datetime.datetime.strptime("25-12-2021", "%d-%m-%Y")
    count = len(jewel_usd) - (end-start).days - 1
    jewel_usd_date = jewel_usd[count]

    return jewel_usd_date  

def get_dfktears_jewel_price_date(date): ##maybe wrong
    start =  start = datetime.datetime.strptime(date, "%d-%m-%Y")
    end = datetime.datetime.strptime("25-12-2021", "%d-%m-%Y")
    count = len(dfktears_jewel) - (end-start).days - 1
    dfktears_jewel_date = dfktears_jewel[count]

    return dfktears_jewel_date

def get_crpyto_price(x):  
    if x == 'dfkshvas_jewel':
        url = 'https://geckoterminal.com/one/pools/0xb270556714136049b27485f1aa8089b10f6f7f57'  #dfkshave/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])

    if x == 'dfkgold_jewel':
        url = 'https://geckoterminal.com/one/pools/0x321eafb0aed358966a90513290de99763946a54b'  #dfkgold/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    if x == 'jewel_wone':
        url = 'https://geckoterminal.com/one/pools/0xeb579ddcd49a7beb3f205c9ff6006bb6390f138f' #jewel/wone
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    if x == 'xjewel_wone':
        url = 'https://geckoterminal.com/one/pools/0xfdab6b23053e22b74f21ed42834d7048491f8f32' #xjewel/wone
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])

    if x =='dfktears_jewel':
        url = 'https://geckoterminal.com/one/pools/0xc79245ba0248abe8a385d588c0a9d3db261b453c?utm_source=coingecko&utm_medium=referral&utm_campaign=livechart' #dfktears/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    return price


def hash_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)

    timestamp_unix = web3.eth.get_block(block_number).timestamp
    timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    # print(timestamp)
    return timestamp, block_number


def scan_log(receipt, tx_hash):
    timestamp, block_number = hash_timestamp(tx_hash)
    transactions = []
    for log in receipt["logs"]:
        if log["address"] in serendale_erc20_only:

            token = serendale_erc20_only[log["address"]]
            address_from = log.topics[1]
            address_to = log.topics[2]
            value = web3.toInt(hexstr=log.data)

            if token == "JEWEL":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * float(get_jewel_usd_price_date(timestamp[:10]))
                #value = value * jewel_usd
            
            if token == "xJEWEL":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                #xjewel_jewel = get_crpyto_price("xjewel_wone") /get_crpyto_price("jewel_wone")
                value = float(web3.fromWei(value, "ether")) * float(get_jewel_usd_price_date(timestamp[:10])) * (get_crpyto_price("xjewel_wone") /get_crpyto_price("jewel_wone"))
                #value = value * xjewel_jewel * jewel_usd
            
            if token == "DFKSHVAS":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * float(get_jewel_usd_price_date(timestamp[:10])) * (get_crpyto_price("dfkshvas_jewel")) * (10**18)
                #value = value * (get_crpyto_price("dfkshvas_jewel")) * jewel_usd * (10**18)
            
            if token == "Silverfin" or token == "DFKGLDVN":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 100 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 100 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "DFKSWFTHSL":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 75 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 75 * (get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "Shimmerskin":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 60 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 60 * (get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "Sailfish":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 50 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 50 * (get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "Redgill" or token == "DFKRDLF":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 15 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 15 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "DFKAMBRTFY":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 12.5 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 12.5 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "DFKDRKWD":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 10 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 10 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "Ironscale" or token == "Lanterneye" or token == "DFKRCKRT":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 5 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 5 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "DFKRGWD" or token == "DFKBLOATER":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * 2.5 * (get_crpyto_price("dfkgold_jewel")) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * 2.5 *(get_crpyto_price("dfkgold_jewel")) * jewel_usd * (10**18)
            
            if token == "DFKTEARS":
                #jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
                value = float(web3.fromWei(value, "ether")) * get_dfktears_jewel_price_date(timestamp[:10]) * float(get_jewel_usd_price_date(timestamp[:10])) * (10**18)
                #value = value * get_dfktears_jewel_price_date(timestamp[:10]) * jewel_usd * (10**18)
        
            transactions += [[timestamp, address_from, address_to, value, token]]
            print([timestamp, block_number, address_from, address_to, value, token])

    return transactions

def DFK_filter(wallet_transactions):
    print("Pulling transaction details...")
    DFK_transactions = {}
    for tx_hash in wallet_transactions:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        # print(receipt)
        if receipt.logs != []:
            for key in serendale_contracts.keys():
                if key == receipt["from"] or key == receipt["to"]:
                    # only find block and timestamp when it is DFK contract
                    DFK_transactions[tx_hash] = scan_log(receipt, tx_hash)
                    # print(DFK_transactions[tx_hash])
                    break
                elif key == receipt.logs[0]["address"]:
                    # only find block and timestamp when it is DFK contract
                    DFK_transactions[tx_hash] = scan_log(receipt, tx_hash)
                    # print(DFK_transactions[tx_hash])
                    break
    print("Completed!")
    return DFK_transactions

DFK_transactions = DFK_filter(wallet_transactions)

# print(DFK_transactions)
print("Total DFK Transactions = " + str(len(DFK_transactions)))


