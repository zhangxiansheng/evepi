# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs

# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( input_str ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    while True:
        if input_str.value.find("$_$") > -1:
            print len( input_str.value )
            input_json_list, input_str.value = input_str.value[:-3].split("$_$"), ""
            for input_json in input_json_list:
                print input_json
                ser.write( input_json )

# socket server
def socket_server( input_str ):
    
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    host = fuckargs.get( "host" )  # Symbolic name meaning all available interfaces
    port = int( fuckargs.get("port") ) # Arbitrary non-privileged port
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )   #定义socket类型，网络通信，TCP
    s.bind( (host, port) )   #套接字绑定的IP与端口
    s.listen( 5 )         #开始TCP监听
    input_str.value = ""
    while True:
        conn, addr = s.accept()   #接受TCP连接，并返回新的套接字与IP地址
        # print 'Connected by', addr    #输出客户端的IP地址
        try:
            while True:
                data=conn.recv(1024)    #把接收的数据实例化
                # 如果不为空
                if len(data) > 11:
                    
                    # 阻塞与等待一下吧，目前折中的做法吧
                    while 1:
                        will_input_str = input_str.value + data + "$_$"
                        if len( will_input_str ) < 40000: break
                    
                    input_str.value = will_input_str
                
                conn.sendall( "done" )  ### 这里暂时约定做“伪回应”
        except:
            conn.close()     #关闭连接

# Main process

ser = serial.Serial( fuckargs.get("usb"), int( fuckargs.get("bits") ) )
string_dict = multiprocessing.Array( "c", "fuck"*10000 ) # 为字符串设置内存大小为40000个字符长度
os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

p_serial = multiprocessing.Process( target=get_serial_info, args=(string_dict,) )
p_socket = multiprocessing.Process( target=socket_server, args=(string_dict,) )

p_serial.start()
p_socket.start()