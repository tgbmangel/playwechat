import itchat
import time

itchat.auto_login(hotReload=True)
all_firends=itchat.get_friends()[1:]
def find_firend_user_name_by_nick_name(firends_list,wechat_nick_name):
    user_name='UserName'
    nick_name='NickName'
    _get_list=[]
    for x in firends_list:
        if wechat_nick_name in x[nick_name]:
            _get_list.append(x)
    print(_get_list)
    return _get_list

def send_message_to_nick_name(wechat_nick_name):
    UserList=find_firend_user_name_by_nick_name(all_firends,wechat_nick_name)
    for _u in UserList:
        itchat.send("Hello {}!".format(_u.NickName),toUserName=_u.UserName)
        print('message sended')

send_message_to_nick_name("西边有片云")

