# coding=utf-8
# 取得参数的模块

import sys

def get( key ):
    global args_dict
    return args_dict.get( key )

args_list = sys.argv
args_dict = { "host": "localhost", "port": "50027", "bits": "9600" }

for arg in args_list:
    arg_change = arg.replace( '==', '=' )
    arg_find = arg_change.find( '=' )
    if arg_find > -1:
        key = arg_change[:arg_find]
        key = key.replace( "-", "" )
        value =  arg_change[arg_find+1:]
        args_dict[ key ] = value