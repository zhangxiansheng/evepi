#coding=utf-8

import serial

ser = serial.Serial('/dev/cu.usbserial', 115200 )


def get_bit():
    global ser
    return int( hex( ord( ser.read() ) ), 16 )

def get_bits( n ):
    global ser
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
nn = 50
s = nn
while 1:
    s = (s + 1) % nn
    if s==0: print "-" * 50
    
    # 加速度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x51 )
    ax = (( axh<<8)|axl)/32768.0*16
    ay = (( ayh<<8)|ayl)/32768.0*16
    az = (( azh<<8)|azl)/32768.0*16
    if az > 16: az = az - 32
    t = ((th<<8)|tl)/340.0 +36.53
    sum = axl + axh + ayl + ayh + azl + azh + tl + th - sum
    if s==0: print "ax={ax} ay={ay} az={az} t={t} sum={sum}".format( ax=ax, ay=ay, az=az, t=t, sum=sum )

    # 角速度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x52 )
    ax = (( axh<<8)|axl)/32768.0*2000
    ay = (( ayh<<8)|ayl)/32768.0*2000
    az = (( azh<<8)|azl)/32768.0*2000
    t = ((th<<8)|tl)/340.0 + 36.53
    sum = axl + axh + ayl + ayh + azl + azh + tl + th - sum
    if s==0: print "wx={ax} wy={ay} wz={az} t={t} sum={sum}".format( ax=ax, ay=ay, az=az, t=t, sum=sum )

    # 角度输出
    axl, axh, ayl, ayh, azl, azh, tl, th, sum = find( 0x55, 0x53 )
    ax = (( axh<<8)|axl)/32768.0*180
    ay = (( ayh<<8)|ayl)/32768.0*180
    az = (( azh<<8)|azl)/32768.0*180
    t = ((th<<8)|tl)/340.0 + 36.53
    sum = axl + axh + ayl + ayh + azl + azh + tl + th - sum
    if s==0: print "rx={ax} ry={ay} rz={az} t={t} sum={sum}".format( ax=ax, ay=ay, az=az, t=t, sum=sum )


