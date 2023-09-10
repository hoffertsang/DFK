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
    start = datetime.datetime.strptime("13-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
    end = datetime.datetime.strptime("24-12-2021", "%d-%m-%Y")
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
    end = datetime.datetime.strptime("24-12-2021", "%d-%m-%Y")
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
    end = datetime.datetime.strptime("24-12-2021", "%d-%m-%Y")
    count = len(jewel_usd) - (end-start).days - 1
    jewel_usd_date = jewel_usd[count]

    return jewel_usd_date  

def get_dfktears_jewel_price_date(date): ##maybe wrong
    start =  start = datetime.datetime.strptime(date, "%d-%m-%Y")
    end = datetime.datetime.strptime("24-12-2021", "%d-%m-%Y")
    count = len(dfktears_jewel) - (end-start).days - 1
    dfktears_jewel_date = dfktears_jewel[count]

    return dfktears_jewel_date