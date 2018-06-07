# -*- coding: utf-8 -*-
# @Project : P3 
# @Time    : 2018/6/7 14:02
# @Author  : 
# @File    : lirun.py
# @Software: PyCharm Community Edition

def lirun(per_get,per_current,catch):
    per_get=per_get/10.0
    per= per_get/per_current*0.8*100
    catch_lirun=per*catch*per_current/100
    print( '{}%'.format(per),catch_lirun)

lirun(1.35,3.41,20000)



