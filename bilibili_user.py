#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 17:05
# @Author  : HEHE
# @Site    : 
# @File    : bilibili_user.py
# @Software: PyCharm

from urllib import request,parse
from user_agents import user_agent
from multiprocessing.dummy import Pool as ThreadPool
import logging
import gzip
import random
import json
import time
import sys
import csv
import re


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


# FileHandler
file_handler = logging.FileHandler('output.log')
file_handler.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_request(url, my_header, method='GET', my_timeout= 5, num_retries = 10, data=None, uid=None):
    """
    构造请求函数
    :param url: 请求URL
    :param my_header: 请求头
    :param method: 请求方式
    :param my_timeout: 请求超时时间
    :param num_retries: 出错时，重复请求次数
    :param data: POST时，请求数据
    :param uid: 用户id
    :return: 返回请求页面
    """
    try:
        logger.debug('正在请求页面：%s, 用户ID为:%s' % (url, uid))
        req = request.Request(url = url, headers=my_header, method= method ,data=data)
        return request.urlopen(req,timeout= my_timeout)
    except:   # 若上面代码执行错误，这重新执行
        if num_retries>0:
            time.sleep(3)
            logger.info('获取网页出错，3S后将获取倒数第：%d 次, 用户ID为%s' % (num_retries,uid))
            my_header['User-Agent'] = random.choice(user_agent)          # 请求出现问题，有可能是请求头的问题，所以换一下
            logger.debug('当前请求的请求头为：%s' % my_header['User-Agent'])
            return get_request(url = url, my_header= my_header, method= method, num_retries = num_retries-1, data=data,uid=uid)

def get_user_base_information(user_id):
    """
    构造基本页面的请求头需要的信息
    :param user_id: 用户ID
    :return user_base_information: 用字典存放的UP主信息
    """
    head = {                                                 # 构造请求头
    'Host': 'space.bilibili.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://space.bilibili.com',
    'User-Agent': random.choice(user_agent),
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://space.bilibili.com/%s/' % user_id,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    logger.debug('当前请求的请求头为：%s'  % head['User-Agent'])

    url = 'https://space.bilibili.com/ajax/member/GetInfo'  # 请求地址
    dict = {'mid': user_id, 'csrf': '31396f8b9e1a5bd90aadcf54730ff553'}  # post中发送的字段
    data = bytes(parse.urlencode(dict), encoding='utf8')
    response = get_request(url=url, data=data, my_header=head, method='POST', uid =user_id)
    html = gzip.decompress(response.read()).decode('utf-8')  # 解压缩页面
    logger.debug('页面请求成功： %s, 用户ID为: %s' % (url, user_id))

    return analysis_base_inform(html,url, user_id)

def analysis_base_inform(html, url= None, user_id=None):
    """
    获取B站up主的基本信息，包括用户ID、昵称、性别、头像、等级、个性签名、个人认证、注册时间、生日等
    :param html: 请求到的页面
    :return: 用字典存放的UP主信息
    """
    user_base_information = {}
    js_dict = json.loads(html)

    status_json = js_dict['status'] if 'status' in js_dict.keys() else False
    if status_json == True:
        js_dict = js_dict['data']
        user_base_information['mid'] = js_dict['mid']
        user_base_information['name'] = js_dict['name']
        user_base_information['sex'] = js_dict['sex']
        user_base_information['face'] = js_dict['face']
        try:
            regtime_local = time.localtime(js_dict['regtime'])
            user_base_information['regtime'] = time.strftime("%Y-%m-%d %H:%M:%S",regtime_local)
        except:
            user_base_information['regtime'] = ''

        try:
            user_base_information['birthday'] = js_dict['birthday']
        except:
            user_base_information['birthday'] = ''
        user_base_information['sign'] = js_dict['sign']
        user_base_information['current_level'] = js_dict['level_info']['current_level']
        user_base_information['desc'] = js_dict['official_verify']['desc']
        user_base_information['coins'] = js_dict['coins']
        user_base_information['fans_badge'] = js_dict['fans_badge']
    else:
        logger.warning('当前页面无信息: %s, 用户ID为： %s' % (url,user_id) )
        user_base_information = None      # 页面不存在的情况

    return user_base_information

def get_user_follow_fans(user_id):
    """
    获取B站up主的粉丝，关注数，以及观看量等链接
    :param user_id:  用户ID
    :return follow_fans:  用字典存放的UP主的其他信息
    """
    follow_fans_others = {}
    head = {
    'Host': 'api.bilibili.com',
    'Connection': 'keep-alive',
    'User-Agent': random.choice(user_agent),
    'Accept': '*/*',
    'Referer': 'https://space.bilibili.com/%s/' % str(user_id),
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    logger.debug('当前请求的请求头为：%s' % head['User-Agent'])

    url1 = 'https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp&callback=__jp4' % str(user_id)
    response1 = get_request(url=url1,uid=user_id, my_header=head).read().decode('utf-8')
    follow_fans_dict1 = re.search(r'{"mid".+?}', response1)
    if follow_fans_dict1 is not None:
        js_follow_fans_dict1 = json.loads(follow_fans_dict1.group())
        follow_fans_others['following'] = js_follow_fans_dict1['following']
        follow_fans_others['follower'] = js_follow_fans_dict1['follower']
    else:
        follow_fans_others = None
        logger.warning('当前页面无信息: %s' % url1)
        return follow_fans_others


    url2 = 'https://api.bilibili.com/x/space/upstat?mid=%s&jsonp=jsonp&callback=__jp5' % str(user_id)
    response2 = get_request(url=url2,uid=user_id, my_header=head).read().decode('utf-8')
    follow_fans_dict2 = re.search(r'{"archi.+?}}', response2)
    if follow_fans_dict2 is not None:
        js_follow_fans_dict2 = json.loads(follow_fans_dict2.group())
        follow_fans_others['archive_view'] = js_follow_fans_dict2['archive']['view']
        follow_fans_others['article_view'] = js_follow_fans_dict2['article']['view']
    else:
        follow_fans_others = None
        logger.warning('当前页面无信息: %s,用户ID为： %s' % (url2, user_id))
        return follow_fans_others

    return follow_fans_others




def put_into_database(information, user_id):
    """
    将UP主的信息存放进csv文件中，每个文件3000条信息左右
    """
    csv_size = 3000
    pre_page = (user_id-1)//csv_size+1
    page = user_id//csv_size+1
    file_name = 'resource\information_%s.csv' % page
    fieldnames = ['mid', 'name', 'sex', 'face', 'regtime', 'birthday', 'sign', 'current_level', 'desc', 'coins',
                  'fans_badge', 'following', 'follower', 'archive_view', 'article_view']
    try:
        if pre_page != page:
            pre_page += 1
            with open(file_name, 'a', newline='', errors='ignore') as f:
                f_csv = csv.DictWriter(f, fieldnames=fieldnames)
                f_csv.writeheader()
        with open(file_name, 'a', newline='', errors='ignore') as f:
            f_csv = csv.DictWriter(f,fieldnames = fieldnames)
            f_csv.writerow(information)
    except Exception as e :
        logger.warning('用户%s的信息写入出错')
        logger.warning(e)


def start_clawer(user_id):
    time.sleep(2)
    logger.info('开始爬取第%d个用户信息 ' % user_id)
    user_base_information = get_user_base_information(user_id)
    follow_fans = get_user_follow_fans(user_id)
    if user_base_information is not None:
        if follow_fans is not None:
            user_base_information.update(follow_fans)
            logger.debug(user_base_information)
            print(user_base_information.keys())
        put_into_database(user_base_information, user_id)
    else:
        logger.warning('用户%d的信息未爬取' % user_id)




if __name__ == '__main__':
    logger.info('爬虫开始抓取用户信息')
    pool = ThreadPool(processes=4)
    i = 1
    j = 10000
    for k in range(37020):
        pool.map(start_clawer,[t for t in range(i+k*10000,j+k*10000+1)])
    """
    for i in range(1,370200000):
        pool.apply_async(start_clawer, (i,))
    pool.close()
    pool.join()
    """



