#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 13:20
# @Author  : HEHE
# @Site    : 
# @File    : bilibili_v1.2.py
# @Software: PyCharm

from urllib import request,parse

headers={
'Host': 'api.bilibili.com',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'Accept': '*/*',
'Referer': 'https://space.bilibili.com/521444/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

url = 'https://api.bilibili.com/x/relation/stat?vmid=521444&jsonp=jsonp&callback=__jp4'

req = request.Request(url=url,headers = headers,method='GET')

response = request.urlopen(req)

print(response.read().decode('utf-8'))