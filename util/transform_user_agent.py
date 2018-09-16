#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 20:57
# @Author  : HEHE
# @Site    : 
# @File    : transform_user_agent.py
# @Software: PyCharm

import csv

"""                                                                     # 结论，pandas输出不能以逗号结尾，没有结尾符号，没有
def transfrorm_UserAgents(uafile,py_uafile):
    user_agent = []
    df = pd.read_csv(uafile, header= None,index_col=None,dtype=str)
    print(df)
    df[2] = None
    df.to_csv(py_uafile, header=False, index=False,sep=',',quoting=1)
"""

def transfrorm_UserAgents(uafile, py_uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip())
        uaf.close()

    with open(py_uafile,'w') as wuaf:
        for ua in uas:
            print(ua.decode('utf-8'))
            wuaf.writelines(ua.decode('utf-8') + ',\n')
        wuaf.close()




if __name__ == '__main__':
    uafile = r'G:\PythonProjectWorkPlace\bilibili-user\user_agents.txt'
    py_uafile = r'G:\PythonProjectWorkPlace\BiliBili_User\user_agents.csv'
    transfrorm_UserAgents(uafile,py_uafile)