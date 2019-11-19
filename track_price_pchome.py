import requests
import re
from bs4 import BeautifulSoup
import datetime
import json
from collections import deque 

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

def get_converted_price(price):

    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price)) # Thanks to https://medium.com/@oorjahalt
    return converted_price

def get_query_result(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        # print(page.content)
        jj=json.loads(page.content)
        for i in jj["prods"]:
            print(i["name"], i["price"])

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

def get_prod_detail(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        # print(page.content)
        str=page.content.decode("utf-8")
        firstIdx = str.find("{")
        # print(firstIdx)
        secondIdx = str.find("{", firstIdx+1)
        # print(secondIdx)
        close_bracket = getIndex(str, secondIdx)
        # print(close_bracket)
        j=str[secondIdx:close_bracket]+"}"
        # print(j)
        jj=json.loads(j)
        # print(list(jj.keys())[0])
        prod = jj[list(jj.keys())[0]]
        print(prod["Name"], prod["Price"]["P"])
        # for i in jj["prods"]:
        #     print(i["name"], i["price"])

headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
details = {"name": "", "price": 0, "deal": True, "url": ""}
# get_query_result("https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=ssd&page=1&sort=sale/dc")
get_prod_detail("https://24h.pchome.com.tw/ecapi/ecshop/prodapi/v2/prod/DRAH6C-A9008F563-000&fields=Seq,Id,Name,Nick,Store,PreOrdDate,SpeOrdDate,Price,Discount,Pic,Weight,ISBN,Qty,Bonus,isBig,isSpec,isCombine,isDiy,isRecyclable,isCarrier,isMedical,isBigCart,isSnapUp,isDescAndIntroSync,isFoodContents,isHuge,isEnergySubsidy,isPrimeOnly,isPreOrder24h,isWarranty,isLegalStore,isFresh,isBidding,isSet,Volume,isArrival24h&_callback=jsonp_prod&1574058600?_callback=jsonp_prod")