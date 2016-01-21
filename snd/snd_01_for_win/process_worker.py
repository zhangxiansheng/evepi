# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs

# 没声音就输出1
# 有声音就输出0

# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( whether, sum_list, usb, bits ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    ser = serial.Serial( usb, bits )
    i = 0
    while True:
        res_read = ser.readline()[0]
        whether.value = res_read
        # 每1s的数据记录在list中不断更新
        i = (i+1) % 200
        sum_list[i] = int( res_read )

# socket server
def socket_server( whether, sum_list ):
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
                if data == "whether":
                    res = whether.value
                elif data == "sum":
                    res = str( sum(sum_list)/2.0 )
                else:
                    res = "-1"
                conn.sendall( res )
        except:
            conn.close()     #关闭连接

# Main process
if __name__ == "__main__":
    usb_arg, bits_arg = fuckargs.get("usb"), int( fuckargs.get("bits") )
    chr = multiprocessing.Value('c', '0')
    sum_list = multiprocessing.Array( 'i', [1]*200 )

    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

    p_serial = multiprocessing.Process( target=get_serial_info, args=(chr, sum_list, usb_arg, bits_arg) )
    p_socket = multiprocessing.Process( target=socket_server, args=(chr, sum_list,) )

    p_serial.start()
    p_socket.start()