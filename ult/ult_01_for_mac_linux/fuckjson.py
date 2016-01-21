#coding=utf-8
#该脚本用来对json文件标准化以保证不同环境下的识别率

f = open( "config.json" ).read()

whether_find = 1
while whether_find > -1:
    whether_find = f.find( "/*" )
    if whether_find > -1:
        whether_over = f.find( "*/" )
        f = f[:whether_find] + f[whether_over+3:]

f = f.replace( "'", '"' )

w = open( "fuck.json", "w" )
w.write( f )
w.close()