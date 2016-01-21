# coding=utf-8
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import *
from fabric.colors import *
import json
import socket

@task
def start():
    print green( "starting …" )
    # 读取json
    local( "python fuckjson.py" )
    f = file( "fuck.json" )
    data = json.load( f )
    
    # check
    usb_ports = local( "python -m serial.tools.list_ports", capture=True )
    check_res = True
    print green( "Checking…" )
    print "+" + "-"*30
    for key in data:
        # 检查usb接口
        usb = data[ key ][2]
        if usb_ports.find( usb ) > -1:
            print green( "%s: %s is going" % (key,usb) )
        else:
            print red( "%s: %s is warning" % (key,usb) )
            check_res = False
        
        # 检查socket接口
        host = data[ key ][0]
        port = data[ key ][1]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 定义socket类型，网络通信
            s.connect( (host, port) )       # 要连接的IP与端口
            s.close()
            print red( "%s  %s: %d  is be used" % ( key, host, port ) )
            check_res = False
        except:
            print green( "%s: %s:%d  is ready for you" % ( key, host, port ) )
        print "+" + "-"*30
        
    if not check_res:
        print red( "You have errors above, please fix it before you start." )
        return

    # 将fuck.json的绝对路径告诉放在/etc/XXX/fuckpath.md
    local( "python fuckpath.py" )

    # start each process
    for key in data:
        host = data[key][0]
        port = data[key][1]
        usb = data[key][2]
        local( "START /B python process_worker.py --host=%s --port=%s --usb=%s" % ( host, port, usb ) )
        print green( "%s:%s is starting %s" % (host, port, usb) )
    print green( "Aready Start All Processes" )

@task
def status():
    # 判断usb端口
    # 判断socket端口
    
    # 读取json
    local( "python fuckjson.py" )
    f = file( "fuck.json" )
    data = json.load( f )
    
    # 判断usb接口是否松动
    usb_ports = local( "python -m serial.tools.list_ports", capture=True )
    print "+" + "-"*30
    for key in data:
        # 判断usb接口
        usb = data[ key ][2]
        if usb_ports.find( usb ) > -1:
            print green( "%s: %s is going" % (key,usb) )
        else:
            print red( "%s: %s is warning" % (key,usb) )
        # 判断socket接口
        host = data[ key ][0]
        port = data[ key ][1]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 定义socket类型，网络通信
            s.connect( (host, port) )       # 要连接的IP与端口
            s.close()
            print green( "%s  %s: %d  open" % ( key, host, port ) )
        except:
            print red( "%s: %s:%d  closed" % ( key, host, port ) )
        print "+" + "-"*30


@task
def stop():
    fp = open( "pid_repo", "r" )
    for eachline in fp:
        try:
            local( "TASKKILL /PID %d /F" % int(eachline) )
        except:
            print red( "aready" )
    w = open( "pid_repo", "w" )
    w.write( "" )
    w.close()
    print green( "Aready Stop All Processes" )

@task
def restart():
    stop()
    start()

@task
def usb():
    local( "python -m serial.tools.list_ports" )
