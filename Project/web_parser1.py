import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from pprint import pprint
import copy
import re

url = "https://www.optionstrategist.com/calculators/free-volatility-data"
res = requests.get(url)
page = res.content
def web_parser1():
    url = "https://www.optionstrategist.com/calculators/free-volatility-data"
    res = requests.get(url)
    page = res.content
    soup = BeautifulSoup(page, "html.parser")
    tag = soup.find_all("pre")
    tagstr = tag[0].text
    match1 = re.sub(r"[\d]{1,3}%ile","", tagstr)
    match2 = re.sub(r"\*","", match1)
    match3 = re.sub(r"\d{1,3}/","", match2)
    
    alist = match3.split()[17:]
    blist = []
    
    for item in alist:
        blist += item.split()
    for item in blist:
        if (item == '****************************************************************' or item == 'McMillan' or item == 'Analysis'):
            index = blist.index(item)
            blist.pop(index)
        if (item == 'www.optionstrategist.com' or item == '*' or item == '800-724-1817' or item == 'generated'):
            index = blist.index(item)
            blist.pop(index)

    clist = copy.deepcopy(blist)
    for item in clist:
        if (item == '800-724-1817' or item == 'Corp.' or item == 'Copyright'):
            clist.remove(item)
            
    dlist = copy.deepcopy(clist)
    for item in dlist:
        if item == 'Copyright'or item == 'Data' or item == 'by':
            dlist.remove(item)
    
    elist = copy.deepcopy(dlist)
    for item in elist:
        if item == '2021' or item == 'by':
            elist.remove(item)
    
    flist = copy.deepcopy(elist)
    for item in flist:
        if item == 'Analysis':
            flist.remove(item)
                
    rawlist = flist[97:]
    rawlist.remove('(option')
    rawlist.remove('symbols)')
    newlist = rawlist[2546:]
    
    
    
    rawlist1 = [newlist[i:i+7] for i in range(0,len(newlist),7)]
#     newlist1.insert(0, "[Symbol,hv20,hv50,hv100,Date,curiv, smth, close]")

    for item in rawlist1:
        year = item[4][0:2]
        month = item[4][2:4]
        day = item[4][4:6]
        item[4] = month + "/" + day + "/" + year    
    
    df = pd.DataFrame(rawlist1, columns = ['Symbol', 'HV-20', 'HV-50', 'HV-100', "Date", "Current IV", "Close"])
    
    indices = df.loc[(df['HV-20'].isin(['0.0'])) & (df['HV-50'].isin(['0.0'])) & (df['HV-100'].isin(['0.0']))].index
    dfremovable = df.loc[(df['HV-20'].isin(['0.0'])) & (df['HV-50'].isin(['0.0'])) & (df['HV-100'].isin(['0.0']))]
#     print(dfremovable)
#     print(indices)
    indexlist = [i for i in indices]
#     print(indexlist)
    df.drop(indexlist, inplace=True)
    df.reset_index(inplace = True)
    df.drop(["index"], axis = 1, inplace=True)
#     print(df)

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    
    data = flist[111:2645]
    datalist = [data[i:i+7] for i in range(0,len(data),7)]
#     df2 = pd.DataFrame(flist, columns = ['Future/Index', 'HV-20', 'HV-50', 'HV-100', "Date", "Current IV", "Close"])
#     display(df)
    for item in datalist:
        for i,j in enumerate(item):
            if j == "OPTION":
                datalist.insert(i+1,"N/A")
    pprint(datalist)
   




############ Function Call ############
web_parser1()