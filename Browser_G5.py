#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
from time import sleep
from Settings_G5 import Devices
import datetime
import sys

"""
打开浏览器，进入到人民网，上下滑动，反复操作5分钟
"""


def browser(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("浏览器结束时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")  # 回到首页
            # 进入格力定制版UC浏览器
            d.app_start("com.gree.explorer")
            logger.info("启动了浏览器")
            time.sleep(5)
            # 点击百度小图标
            d(text="人民网").click()
            logger.info("开始人民网新闻浏览")
            time.sleep(5)
            logger.info("开始上下滑动操作")
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            logger.info("结束人民网新闻浏览")
            # 返回上一层
            d.press('back')
            time.sleep(5)
            # 停止程序运行
            d.press("home")

        except Exception as e:
            logger.error("浏览器元素定位出错！" + str(e))
            d.app_stop("com.gree.explorer")
            pass
        c = time.time()
        b = c
        time.sleep(1)
        d.press('back')
        time.sleep(5)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮浏览器结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮浏览器总共耗时：%s" % (str(expend_time).split('.')[0]))
