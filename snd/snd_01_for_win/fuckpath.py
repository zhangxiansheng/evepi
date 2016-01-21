#coding=utf-8
#该脚本用来对json文件标准化以保证不同环境下的识别率

import os

NAME = "snd_01"

try:
    w = open( r"C:\evepi\%s\fuckpath.md" % NAME, "w" )
except:
    os.system( "MD C:\evepi" )
    os.system( "MD C:\evepi\%s" % NAME )
    w = open( r"C:\etc\%s\fuckpath.md" % NAME, "w" )

path = os.getcwd() + "\\fuck.json"
w.write( path )
w.close()