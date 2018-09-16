#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 13:55
# @Author  : HEHE
# @Site    : 
# @File    : bilibili_v1_3.py
# @Software: PyCharm

from urllib import request,parse

headers = {
'Host': 'api.bilibili.com',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'Accept': '*/*',
'Referer': 'https://space.bilibili.com/22/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
}

url = 'https://api.bilibili.com/x/space/upstat?mid=521444&jsonp=jsonp&callback=__jp5'

req = request.Request(url = url, headers = headers, method= 'GET')

response = request.urlopen(req)

print(response.read().decode('utf-8'))
