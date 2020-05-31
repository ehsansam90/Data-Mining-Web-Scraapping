import mysql.connector
import requests
import re
from bs4 import BeautifulSoup

list_rgn = list()
list_yb = list()
list_sqrm = list()
prc_list = list()

for i in range(1,2):
    r = requests.get('https://dodota.com/realestate/search/?deal_type=1&v1=1&citycode=1&region_code=thr&page_num='+str(i))
    soup = BeautifulSoup(r.text, 'html.parser')

    rgns = soup.find_all('a', attrs={'itemprop': 'url'})  #پیدا کردن مناطق
    for rgn in rgns:
        cas = re.sub(r'\s+', '', rgn.text)
        if len(re.findall(r'منطقه\d+', cas)) != 0:
            list_rgn.append(re.findall(r'منطقه\d+', cas))

    built_years = soup.find_all('span', attrs={'class':'rd'})    #پیدا کردن سال ساخت
    for by in built_years:
        yb = re.findall(r'1\d{3}',by.text)
        if len(yb) !=0:
            list_yb.append(yb)


    sqr_meters = soup.find_all('span',attrs={'class':'rd'})     #پیدا کردن متر مربع
    for sqrm in sqr_meters:
        sqr_m = re.findall(r'\d+\sمتر مربع',sqrm.text)
        if len(sqr_m) !=0:
            list_sqrm.append(sqr_m)

    all_price = soup.find_all('span', attrs={'class':'rd'})
    for prc in all_price:
        price = (re.sub(r'\s','',prc.text))
        prs_m = re.findall(r'\d+\/*\d*میلیونتومان',price)
        if len(prs_m) !=0:
            prc_list.append(prs_m)

if len(list_yb) < len(list_rgn):
    for i in range(0,len(list_rgn)-len(list_yb)):
        list_yb.append('-')

print(list_yb)
list_rgn.reverse()
print(list_rgn)
list_sqrm.reverse()
print(list_sqrm)
prc_list.reverse()
print(prc_list)








