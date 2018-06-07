# -*- coding: utf-8 -*-
# @Project : P3 
# @Time    : 2018/6/7 11:14
# @Author  : 
# @File    : fenhong.py
# @Software: PyCharm Community Edition
from requests_html import HTMLSession
import re
import time
stock_list_url= 'http://quote.eastmoney.com/stock_list.html'
l=HTMLSession()
lrsp=l.get(stock_list_url)
list_table=lrsp.html.find('#quotesearch',first=True)
stocks=list_table.find('a')
stock_list=[]
pat=re.compile(r'.*?\((6|00).*?\)')
for st in stocks:
    tt=st.text
    if re.match(pattern=pat,string=tt):
        code=tt[-7:-1]
        name=tt[:-8]
        stock_list.append((name,code))
print(len(stock_list))
intres_stock=[
    ('华域汽车','600741'),
    ('上汽集团','600104'),
    ('伊利股份','600887'),
    ('厦门空港','600897'),
    ('中国平安','601318'),
    ('上海建工','600170')
]
for stock_name,stock_code in stock_list:

    url='http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{}.phtml'.format(stock_code)
    #公告日期 送股(股)	转增(股)	派息(税前)(元) 进度	除权除息日	股权登记日	红股上市日	查看详细
    try:
        S = HTMLSession()
        rsp = S.get(url)
        # price=rsp.html.find('#itemCurrent',first=True).text
        # print(price)
        tbody=rsp.html.find('#sharebonus_1 > tbody',first=True)
        trs=tbody.find('tr')
        print('{:^15}{:^15}'.format(stock_name,stock_code),end='')
        for td in [x for x in trs[0].find('td')]:
            print('{:^15}'.format(td.text),end='')
        print('')
        time.sleep(2)
    except Exception as e:
        print(e)
    # for tr in trs:
    #     for td in [x for x in tr.find('td')]:
    #         print('{:^15}'.format(td.text),end='  ')
    #     print('')
