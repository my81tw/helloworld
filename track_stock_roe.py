#!/usr/bin/python3
import requests
import re
from bs4 import BeautifulSoup
import datetime
import json
import logging
import time
from collections import deque 
from lxml import etree
from io import StringIO
import random

logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)07s %(module)s - %(funcName)s: %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
info=logging.info

def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url

def getIndex(s, i): 
  
    # If input is invalid. 
    if s[i] != '{': 
        return -1
  
    # Create a deque to use it as a stack. 
    d = deque() 
  
    # Traverse through all elements 
    # starting from i. 
    for k in range(i, len(s)): 
  
        # Pop a starting bracket 
        # for every closing bracket 
        if s[k] == '}': 
            d.popleft() 
  
        # Push all starting brackets 
        elif s[k] == '{': 
            d.append(s[i]) 
  
        # If deque becomes empty 
        if not d: 
            return k 
  
    return -1

def get_stock_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        # "Cookie": "cookie=WVRveU9udHpPakk2SW1sMklqdHpPakUyT2lJQldvaFBDSzNSdDBJcVViYkhqamJsSWp0ek9qVTZJbU55ZVhCMElqdHpPalkwT2lJUmw3U2VXUUNRM0RxUEhqb2RSQl92cHRwcl80bmZUNV9WX1RYSEdtMFZ0OThfb1lDQmNnWTFNTC9YZVBmbU5YN19rM2RCSE5mY3ZDVllaWjdFNGloUklqdDk%3D; stockid_records_flag=1; stock_popup_stocknews=1; stockid_records=YToyOntpOjA7aToyMzU3O2k6MTtpOjM3MDI7fQ%3D%3D; stock_config=YTozOntzOjc6IlN0b2NrSWQiO047czozOiJ0YWciO2k6MTtzOjQ6InR5cGUiO2k6MDt9"
        # "Cookie": "stock_user_uuid=f0d5b6ba-a7c4-40ae-afff-f7ad83e248c0; stock_id=paf78801; cookie=WVRveU9udHpPakk2SW1sMklqdHpPakUyT2lJQldvaFBDSzNSdDBJcVViYkhqamJsSWp0ek9qVTZJbU55ZVhCMElqdHpPalkwT2lJUmw3U2VXUUNRM0RxUEhqb2RSQl92cHRwcl80bmZUNV9WX1RYSEdtMFZ0OThfb1lDQmNnWTFNTC9YZVBmbU5YN19rM2RCSE5mY3ZDVllaWjdFNGloUklqdDk%3D; stockid_records_flag=1; stock_popup_stocknews=1; stockid_records=YToyOntpOjA7aToyMzU3O2k6MTtpOjM3MDI7fQ%3D%3D; stock_config=YTozOntzOjc6IlN0b2NrSWQiO047czozOiJ0YWciO2k6MTtzOjQ6InR5cGUiO2k6MDt9"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        session = requests.Session()
        response = session.get(url, headers=headers)
        index_of_net_value=response.text.find("每股淨值")
        # info("index_of_net_value="+str(index_of_net_value))
        net_value_match=re.findall(r"[-+]?\d*\.\d+|\d+", response.text[index_of_net_value:response.text.find("</td>", index_of_net_value)])
        # info(net_value_match)
        if(len(net_value_match)==0):
            net_value=''
        else:
            net_value=net_value_match[0]
        # info(net_value)
        index_of=response.text.find("股東權益報酬率")
        td_end_index=response.text.find("</td>", index_of)
        td_end_index=response.text.find("</td>", td_end_index+1)
        # info("index_of="+str(index_of))
        # info("td_end_index="+str(td_end_index))
        roe=response.text[index_of:td_end_index]
        roe=re.findall(r"[-+]?\d*\.\d+|\d+", roe)[0]+"%"
        # info(roe)
        # ret = {}
        # ret["net_value"]=net_value
        # ret["roe"]=roe
        # info(ret)
        return net_value, roe

def all_stock_info():
    """
    2357
0050
1402
2379
3702

2892
2891
2886
3045
8422
1232
1101
2002
2542
2881
2412
1326
3034
2301

4506
4706
1210
2356
0056
00692
00713
00701
00850
    """
    stock_ids="""
2357
0050
1402
2379
3702
    """
    stocks=stock_ids.split('\n')
    final=[]
    for s in stocks:
        s=s.strip()
        if(len(s)>0):
            info("get_stock_info "+s)
            if(s.startswith("00")):
                ret=None
            else:
                ret=get_stock_info("https://tw.stock.yahoo.com/d/s/company_"+s+".html")
            if(ret is not None):
                info(ret)
                final.append("{0}\t{1}\t{2}".format(s, ret[0], ret[1]))
                # info("{0}\t{1}\t{2}".format(s, ret[0], ret[1]))
            else:
                final.append('')
            time.sleep(random.randint(0, 5))
        else:
            final.append('')
    for f in final:
        print(f)
if __name__ == "__main__":
    all_stock_info()
