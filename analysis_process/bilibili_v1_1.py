#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 16:41
# @Author  : HEHE
# @Site    : 
# @File    : bilibili_user.py
# @Software: PyCharm

from urllib import request,parse
import gzip                                                 # 用于解压网页

headers = {                                                 # 构造请求头
'Host': 'space.bilibili.com',
'Connection': 'keep-alive',
#'Content-Length': 16,
'Accept': 'application/json, text/plain, */*',
'Origin': 'https://space.bilibili.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'https://space.bilibili.com/521444/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

url = 'https://space.bilibili.com/ajax/member/GetInfo'      # 请求地址

dict = {'mid': 521444, 'csrf': None }                       # post中发送的字段

data = bytes(parse.urlencode(dict), encoding='utf8')

req = request.Request(url = url, data = data, headers = headers,method='POST' )   # 构造请求

response = request.urlopen(req)                                                   # 请求页面

html = gzip.decompress(response.read())                                           # 解压缩页面

print(html.decode('utf-8'))

