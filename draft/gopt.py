import requests
import requests_cache
import pandas as pd

def get_opt_quote(ticker_symbol):
    chain = []
    #url = 'http://www.google.com/finance/option_chain?q=%s&output=json' %(ticker_symbol)
    url = 'http://www.google.com/finance/option_chain'
    params = {
        'q': ticker_symbol,
        'output': 'json'
    }
    response = requests.get(url, params=params)
    dat = response.text
    k = fix_json(dat)
    opts = eval(k)
    exp = opts['expirations']

    #df = pd.DataFrame(dat)
    #print(df)
    del opts['puts']
    del opts['calls']
    print(opts)

    for expiry in exp:
        print(expiry)
        params = {
            'q': ticker_symbol,
            'output': 'json',
            'expy': expiry['y'],
            'expm': expiry['m'],
            'expd': expiry['d'],
        }
        response = requests.get(url, params=params)
        dat = response.text

        lines = fix_json(dat)
        chain.append(eval(lines))
    return chain

def fix_json(k):
    q=['cid','cp','s','cs','vol','expiry','underlying_id','underlying_price',
     'p','c','oi','e','b','strike','a','name','puts','calls','expirations',
     'y','m','d']
    for i in q:
        try:
            k=k.replace('{%s:'%i,'{"%s":'%i)
            k=k.replace(',%s:'%i,',"%s":'%i)
        except: pass
    return k

filename = "gopt"
expire_after = 5*60
requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
quote = get_opt_quote('GOOG')
#print(quote)