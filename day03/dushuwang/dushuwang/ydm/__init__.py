#!/usr/bin/python3
# coding: utf-8
import os
from __future__ import absolute_import

from .ydm_client import YDMHttp


def ydm_api(filename):
    # 用户名
    username = 'disen_normal'

    # 密码
    password = 'disen8888'

    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid = 5100

    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey = '2a05b965cea25e3a378bc2955c4756a5'

    # 图片文件
    # filename = 'getimage.jpg'

    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004

    # 超时时间，秒
    timeout = 60

    # 初始化
    yundama = YDMHttp(username, password, appid, appkey)

    # 登陆云打码
    uid = yundama.login()

    # 查询余额
    # balance = yundama.balance();

    # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
    cid, result = yundama.decode(filename, codetype, timeout)

    print('cid: %s, result: %s' % (cid, result))

    # 删除验证码图片文件
    # os.remove(filename)

    return result
