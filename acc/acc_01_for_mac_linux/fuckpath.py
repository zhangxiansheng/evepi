#coding=utf-8
#该脚本用来对json文件标准化以保证不同环境下的识别率

import os

NAME = "acc_01"

try:
    w = open( "/etc/%s/fuckpath.md" % NAME, "w" )
except:
    os.system( "sudo mkdir /etc/%s" % NAME )
    w = open( "/etc/%s/fuckpath.md" % NAME, "w" )

path = os.getcwd() + "/fuck.json"
w.write( path )
w.close()