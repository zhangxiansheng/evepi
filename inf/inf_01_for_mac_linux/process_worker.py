# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs

# 感应到了就输出1
# 没感应到就输出0

# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( whether ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    while True:
        whether.value = ser.readline()[0]

# socket server
def socket_server( whether ):
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
                res = whether.value
                conn.sendall( res )
        except:
            conn.close()     #关闭连接

# Main process

ser = serial.Serial( fuckargs.get("usb"), int( fuckargs.get("bits") ) )
chr = multiprocessing.Value('c', '0')

os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

p_serial = multiprocessing.Process( target=get_serial_info, args=(chr,) )
p_socket = multiprocessing.Process( target=socket_server, args=(chr,) )

p_serial.start()
p_socket.start()