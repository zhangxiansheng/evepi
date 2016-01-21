# coding=utf-8

import multiprocessing
import serial
import socket
import os
import fuckargs
import json
import time

def get_bit():
    return int( hex( ord( ser.read() ) ), 16 )

def get_bits( n ):
    s = int( hex( ord( ser.read() ) ), 16 )
    s = [s]
    if n == 1:
        return s
    else:
        return s + get_bits( n-1 )

def find( head1, head2 ):
    s = get_bit()
    while s != head1:
        s = get_bit()
    s = get_bit()
    if s != head2:
        return find( head1, head2 )
    else:
        return get_bits(9)

def get_now_result():
    
    # 加速度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x51 )
    ax = (( axh<<8)|axl)/32768.0*16
    ay = (( ayh<<8)|ayl)/32768.0*16
    az = (( azh<<8)|azl)/32768.0*16
    if az > 16: az = az - 32
    if ax > 16: ax = ax - 32
    if ay > 16: ay = ay - 32
    t1 = ((th<<8)|tl)/340.0 +36.53

    # 角速度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x52 )
    wx = (( axh<<8)|axl)/32768.0*2000
    wy = (( ayh<<8)|ayl)/32768.0*2000
    wz = (( azh<<8)|azl)/32768.0*2000
    if wz > 2000: wz = wz - 4000
    if wx > 2000: wx = wx - 4000
    if wy > 2000: wy = wy - 4000
    t2 = ((th<<8)|tl)/340.0 + 36.53

    # 角度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x53 )
    rx = (( axh<<8)|axl)/32768.0*180
    ry = (( ayh<<8)|ayl)/32768.0*180
    rz = (( azh<<8)|azl)/32768.0*180
    t3 = ((th<<8)|tl)/340.0 + 36.53
    
    # 平均温度
    t = (t1 + t2 + t3) / 3.0
    
    # unix/linux 时间戳
    now = time.time()

    res_dict = { "ax" : ax, \
                 "ay" : ay, \
                 "az" : az, \
                 "wx" : wx, \
                 "wy" : wy, \
                 "wz" : wz, \
                 "rx" : rx, \
                 "ry" : ry, \
                 "rz" : rz, \
                 "temp" : t, \
                 "timestamp" : now }

    res_dict_str = json.dumps( res_dict )

    return res_dict_str


# 串口通讯
# 频率的决定者以硬件的串口通讯频率决定
def get_serial_info( result_str, usb, bits ):
    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid
    ser = serial.Serial( usb, bits )
    while True:
        result_str.value = get_now_result()

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
if __name__ == "__main__":
    usb_arg, bits_arg = fuckargs.get("usb"), int( fuckargs.get("bits") )
    string_dict = multiprocessing.Array( "c", '{"ax":-10000, "ay":-10000, "az":-10000,"wx":-10000,"wy":-10000,"wz":-10000,"rx":-10000,"ry":-10000,"rz":-10000,"temp":-10000,"timestamp":-100000000000001450420046.871339}'*3)

    os.system( "echo %d >>pid_repo" % os.getpid() ) # store the pid

    p_serial = multiprocessing.Process( target=get_serial_info, args=(string_dict, usb_arg, bits_arg,) )
    p_socket = multiprocessing.Process( target=socket_server, args=(string_dict,) )

    p_serial.start()
    p_socket.start()
