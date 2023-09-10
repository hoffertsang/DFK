# import json

# contract_abi = json.load(open("abi/MasterGardener.json"))
# print(contract_abi)


import hashlib
import hmac
import json
from datetime import datetime

import pandas
from requests import get
from requests.auth import AuthBase

URL = 'https://api.coinbase.com'

class Auth(AuthBase):
    VERSION = b'2021-03-30'

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def __call__(self, request):
        timestamp = datetime.now().strftime('%s')
        message = f"{timestamp}{request.method}{request.path_url}{request.body or ''}"
        signature = hmac.new(self.API_SECRET.encode(),
                             message.encode('utf-8'),
                             digestmod=hashlib.sha256)
        signature_hex = signature.hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_hex,
            'CB-ACCESS-TIMESTAMP': timestamp.encode(),
            'CB-ACCESS-KEY': self.API_KEY.encode(),
            'CB-VERSION': self.VERSION,
            'Content-Type': 'application/json'
        })
        return request


class Coinbase:
    df_accounts = None

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self._accounts()

    def _request(self, request_path):
        auth = Auth(self.API_KEY, self.API_SECRET)
        return get(f'{URL}{request_path}', auth=auth)

    def _accounts(self):
        request_path = '/v2/accounts'
        r = self._request(request_path)
        df = pandas.json_normalize(json.loads(r.content)['data'])
        df = df[['id', 'balance.amount','balance.currency']]
        self.df_accounts = df.loc[df['id'] != df['balance.currency']]

    def _get_transactions(self, id):
        request_path = f'/v2/accounts/{id}/transactions'
        r = self._request(request_path)
        df = pandas.json_normalize(json.loads(r.content)['data'])
        return df

    def transactions(self):
        df_tr = []
        for i in self.df_accounts.index:
            df_tr.append(self._get_transactions(self.df_accounts['id'][i]))
        df = pandas.concat(df_tr, ignore_index=True)
        return df
