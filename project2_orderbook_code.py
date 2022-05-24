#!/usr/bin/env python
# coding: utf-8

# In[6]:


import time
import requests
import pandas as pd
import datetime
import os

while(1):
    
    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 
    
    df = bids.append(asks)
    
    timestamp = last_update_time = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    req_time = req_timestamp.split(' ')[0]
    
    def write_csv(fn, df):
        df.to_csv(fn, index=False, header=False, mode = 'a')
        
    _list_ex = ['bithumb']
    csv_dir = '/Users/youngb/Bigdataanalysis/'
    _dict_url = {}
    currency = ''
        
    for ex in _list_ex:
        book_fn = '%s/%s-only-%s-%s-book.csv'% (csv_dir, req_time, ex, currency)
        book_df = df
        write_csv(book_fn, book_df)

    print (df)

    time.sleep(4.9)


# In[ ]:




