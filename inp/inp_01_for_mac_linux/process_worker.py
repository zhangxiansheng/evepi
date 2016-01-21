# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs
import json

# 没有被按下的状态是1
# 被按下的状态是0

# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( whether, pre_whether, now_status, action ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    while True:
        pre_whether.value = whether.value
        whether.value = ser.readline()[0]
        action.value = pre_whether.value + whether.value
        if action.value == '01':
            now_status.value = ( now_status.value + 1 ) % 2

# socket server
def socket_server( whether, pre_whether, now_status, action ):
    on_off_dict = { 0: "off", 1: "on" }
    action_dict = { "11": "released", \
                    "10": "pressing", \
                    "00": "pressed", \
                    "01": "releasing" }
    
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    host = fuckargs.get( "host" )  # Symbolic name meaning all available interfaces
    port = int( fuckargs.get("port") ) # Arbitrary non-privileged port
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )   #定义socket类型，网络通信，TCP
    s.bind( (host, port) )   #套接字绑定的IP与端口
    s.listen( 5 )         #开始TCP监听
    while True:
        conn, addr = s.accept()   #接受TCP连接，并返回新的套接字与IP地址
        # print 'Connected by', addr    #输出客户端的IP地址
        try:
            while True:
                data=conn.recv(1024)    #把接收的数据实例化
                res = { "on_off_status" : on_off_dict.get(now_status.value), \
                        "now_result": whether.value, \
                        "pre_result": pre_whether.value, \
                        "action": action_dict.get(action.value) }
                res = json.dumps( res )
                conn.sendall( res )
        except:
            conn.close()     #关闭连接

# Main process

ser = serial.Serial( fuckargs.get("usb"), int( fuckargs.get("bits") ) )
chr = multiprocessing.Value('c', '1')
pre_chr = multiprocessing.Value('c', '1')
action_chr = multiprocessing.Array('c', '11')
status_chr = multiprocessing.Value( 'i', 0 )

os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

p_serial = multiprocessing.Process( target=get_serial_info, args=(chr, pre_chr, status_chr, action_chr, ) )
p_socket = multiprocessing.Process( target=socket_server, args=(chr, pre_chr, status_chr, action_chr, ) )

p_serial.start()
p_socket.start()