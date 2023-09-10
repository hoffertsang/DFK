from pycoingecko import CoinGeckoAPI   #pip install pycoingecko
##https://github.com/man-c/pycoingecko
##https://www.coingecko.com/en/api/documentation 
##refer to coinlist json if need other coin

#currentprice = cg.get_price(ids='bitcoin', vs_currencies='usd') 

cg = CoinGeckoAPI()
# currentpricejewel = cg.get_price(ids='defi-kingdoms', vs_currencies='usd')  ## get jewel price
#historypricejewel = cg.get_coin_history_by_id(id='defi-kingdoms', date='10-12-2021') ## get hisotrical jewel price
#print(currentpricejewel)
# print(historypricejewel['market_data']['current_price']['usd'])
#historypricedfktears = cg.get_coin_history_by_id(id='gaias-tears', date='23-12-2021') ## get hisotrical jewel price
#print(historypricedfktears['market_data']['current_price']['usd'])

##code to work on scanner, need to think of invert timestam from "2021-12-10" to "10-12-2021", and do calcution to print price


#for dfkgold_jewel, jewel_wone, xjewel_wone price

from bs4 import BeautifulSoup 
import requests


def get_crpyto_price(x):  

  if x == 'dfkgold_jewel':
    url = 'https://geckoterminal.com/one/pools/0x321eafb0aed358966a90513290de99763946a54b'  #dfkgold
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

# dfkgold = get_crpyto_price("dfkgold_jewel")
# print(dfkgold)
# xjewel_jewel = get_crpyto_price("xjewel_wone") /get_crpyto_price("jewel_wone")
# print(xjewel_jewel)




# Silverfin: 100 Gold
# Shimmerskin: 60 Gold
# Sailfish: 50 Gold
# Redgill: 15 Gold
# Ironscale: 5 Gold
# Lanterneye: 5 Gold
# DFKBLOATER: 2.5 Gold 

# DFKGLDVN: 100 Gold
# DFKSWFTHSL: 75 Gold
# DFKRDLF: 15 Gold
# DFKAMBRTFY: 12.5 Gold
# DFKDRKWD: 10 Gold
# DFKRCKRT: 5 Gold
# DFKRGWD: 2.5 Gold

import datetime


def get_jewel_usd_and_dfktears_jewel_price():
  cg = CoinGeckoAPI()
  start = datetime.datetime.strptime("13-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
  end = datetime.datetime.strptime("23-12-2021", "%d-%m-%Y")
  date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

  x = list(range(len(date_generated)))
  #jewel_usd = list(range(len(date_generated)))
  dfktears_jewel = list(range(len(date_generated)))
  count = -1
  for date in date_generated:
    count +=1
    x[count] = str(date.strftime("%d-%m-%Y"))
    #jewel_usd[count] = (cg.get_coin_history_by_id(id='defi-kingdoms', date=date.strftime(x[count])))['market_data']['current_price']['usd']
    dummy = cg.get_coin_history_by_id(id='gaias-tears', date='23-12-2021')
    dfktears_jewel[count] = dummy['market_data']['current_price']['eur']

  return dfktears_jewel
  #return jewel_usd, dfktears_jewel

#jewel_usd = get_jewel_usd_and_dfktears_jewel_price()
#print(jewel_usd)
cg = CoinGeckoAPI()
currentpricegaiastears = cg.get_price(ids='gaias-tears', vs_currencies='eur')
dfktears_jewel = (cg.get_coin_history_by_id(id='gaias-tears', date='23-12-2021'))['market_data']['current_price']['eur']

print(dfktears_jewel)
print(currentpricegaiastears)

dfktears = get_crpyto_price("dfktears_jewel")
print(dfktears)








