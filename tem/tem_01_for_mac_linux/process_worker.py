# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs

# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( result_str ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    while True:
        result_str.value = ser.readline()[:-1]

# socket server
def socket_server( result_str ):
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
                conn.sendall( result_str.value )
        except:
            conn.close()     #关闭连接

# Main process

ser = serial.Serial( fuckargs.get("usb"), int( fuckargs.get("bits") ) )
string_dict = multiprocessing.Array( "c", '{"temp":-10000, "humi":-10000, "tol":-20000}')

os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

p_serial = multiprocessing.Process( target=get_serial_info, args=(string_dict,) )
p_socket = multiprocessing.Process( target=socket_server, args=(string_dict,) )

p_serial.start()
p_socket.start()