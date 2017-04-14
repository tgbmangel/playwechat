#coding:cp936
import urllib.request
import itchat,time
import datetime
from itchat.content import *
import requests, json
import threading
from itchat.content import *

hh='http://web.juhe.cn:8080/finance/stock/hs?gid=sh601009'

# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     # cont = alice.respond(msg['Text'])
#     print(msg["Content"])
#     cont = requests.get('http://www.tuling123.com/openapi/api?key=f9edc634f48e406bb2d6d30132ff8293&info=%s' % msg['Content']).content
#     m = json.loads(cont)
#     itchat.send(m['text'], msg['FromUserName'])
#     if m['code'] == 200000:
#         itchat.send(m['url'], msg['FromUserName'])
#     if m['code'] == 302000:
#         itchat.send(m['list'], msg['FromUserName'])
#     if m['code'] == 308000:
#         itchat.send(m['list'], msg['FromUserName'])

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    #if msg['IsAt']:
    # for (k,v) in msg.items():
    #     print(k,v)
    cont = requests.get('http://www.tuling123.com/openapi/api?key=f9edc634f48e406bb2d6d30132ff8293&info=%s' % msg['Content']).content
    m = json.loads(cont)
    print(m)
    time.sleep(1.5)
    #print(msg['FromUserName'])
    if msg['FromUserName']==get_chatroom_username(u'三板桥Style') or msg['FromUserName']==get_chatroom_username(u'信计'):
        if msg['Content']=='':
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], "- -@"), msg['FromUserName'])
        itchat.send(m['text'], msg['FromUserName'])
        if m['code'] == 200000:
            itchat.send(m['url'], msg['FromUserName'])
        if m['code'] == 302000:
            itchat.send(m['list'], msg['FromUserName'])
        if m['code'] == 308000:
            itchat.send(m['list'], msg['FromUserName'])

def itchat_run():
    itchat.run()

def stock_data(stockid):
    try:
        sinaurl='http://hq.sinajs.cn/list='
        res=urllib.request.urlopen(sinaurl+stockid)
        data=res.read()
        data=data.decode('gbk', 'ignore')
        StockdataList=data.split("\"")[1].split(',')
        return StockdataList
    except Exception as e:
        print(e)
        exit(0)

def send_stock_price(stockid,taget_price,user):
    StockdataList=stock_data(stockid)
    stockName,now_price=StockdataList[0],float(StockdataList[3])
    if now_price>taget_price:
        MoreThanMessage="[%s] 当前价格: %s 高于目标价 %s" %(stockName,str(now_price),str(taget_price))
        itchat.send(MoreThanMessage,toUserName=user)
        print(MoreThanMessage)
    else:
        LessThanMessage="[%s] 当前价格: %s 少于目标价 %s" %(stockName,str(now_price),str(taget_price))
        #itchat.send("[%s] 当前价格: %s 少于目标价 %s" %(stockName,str(now_price),str(taget_price)),toUserName=user)
        print(LessThanMessage)

def send_shoupanzongjie(stockid,user):
    StockdataList=stock_data(stockid)
    stockName,open_price,tomorrow_price,now_price,top_price,minimum_price,turnover=\
        StockdataList[0],StockdataList[1],float(StockdataList[2]),float(StockdataList[3]),float(StockdataList[4]),float(StockdataList[5]),float(StockdataList[8])/100.0/10000
    rate_price=(now_price-tomorrow_price)/tomorrow_price
    Shoupanmessage="[%s] 今日总结：\n开盘价格：%s \n收盘价格: %s \n涨跌幅：%.2f%%\n最高价：%s \n最低价：%s\n成交量：%.2f 万手" \
                   %(stockName,str(open_price),str(now_price),rate_price*100,str(top_price),str(minimum_price),turnover)
    imageurl="http://image.sinajs.cn/newchart/daily/n/%s.gif" %stockid
    urllib.request.urlretrieve(imageurl,stockid+".gif")
    image_gif=stockid+".gif"
    #itchat.upload_file(image_gif)
    print(Shoupanmessage)
    itchat.send(Shoupanmessage,toUserName=user)
    itchat.send_image(image_gif,toUserName=user)

def star_at(*FuWu_List):
    #FuWu_List=[[x,y,z],]
    while 1:
        a=datetime.datetime.today()
        for x in FuWu_List:
            stockid,taget_price,user=x[0],x[1],x[2]
            #SendStockPrice(HNFZ,taget_price,chatroomUserName)
            send_stock_price(stockid,taget_price,user)
        if a.hour>14 and a.minute>5:
            break
        time.sleep(90)
def get_chatroom_username(room_name):
    chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
    return  chatroomUserName

if __name__=="__main__":
    #
    SQJT="sh600104"
    THGF="sz002419"
    BYD='sz002594'
    HOWY="sz002084"
    #USER
    Father="wxid_9r9d2qe5df3o22"
    dingwei="wei_dingw"
    chenlu="chenlucrv"
    #
    itchat.auto_login(hotReload=True)
    chatroomUserName=get_chatroom_username(u'经济研讨')
    #print(chatroomUserName)
    #
    FuWu_chelu_THGF=[THGF,16.5,chenlu]
    FuWu_myself_SQJT=[SQJT,30,Father]
    FuWu_myself_BYD=[BYD,55,Father]
    FuWu_dingwei=[HOWY,13.88,dingwei]
    #
    threading.Thread(target=itchat_run).start()
    star_at(FuWu_chelu_THGF,FuWu_myself_SQJT,FuWu_myself_BYD,FuWu_dingwei)
    #
    send_shoupanzongjie(THGF,chatroomUserName)
    send_shoupanzongjie(SQJT,Father)
    send_shoupanzongjie(BYD,Father)
    send_shoupanzongjie(HOWY,chatroomUserName)
