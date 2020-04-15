#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
from Settings_G5 import Devices
import datetime

"""
今日头条浏览新闻10分钟
"""


def toutiao(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("今日头条开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")
            # 打开微博
            d.app_start("com.ss.android.article.news")
            logger.info("启动了今日头条")
            time.sleep(10)
            # 必须要运行监测器
            d.watcher('Permission_a').when(text='允许').click()
            d.watcher('Permission_b').when(resourceId="com.sina.weibo:id/iv_close").click()
            d.watcher('Permission_i').when(text='不了，谢谢').click()
            d.watcher('Permission').when(text='以后再说').click(text='以后再说')  # 如果出现以后再说点击
            d.watcher("Permission_a").watched = True
            d.watcher("Permission_b").watched = True
            d.watcher("Permission_i").watched = True
            d.watcher("Permission").watched = True
            d.click(0.935, 0.135)
            time.sleep(2)
            d(text="关注").click()
            time.sleep(10)
            logger.info("开始滑动关注栏目")
            d.swipe(500, 1500, 500, 500)
            time.sleep(10)
            d.swipe(500, 1500, 500, 500)
            time.sleep(10)
            d.swipe(500, 500, 500, 1500)
            time.sleep(10)
            d.swipe(500, 500, 500, 1500)
            time.sleep(10)
            d.click(0.935, 0.135)
            time.sleep(2)
            d(text="深圳").click()
            time.sleep(10)
            logger.info("开始滑动深圳栏目")
            d.swipe(500, 1500, 500, 500)
            time.sleep(10)
            d.swipe(500, 1500, 500, 500)
            time.sleep(10)
            d.swipe(500, 500, 500, 1500)
            time.sleep(10)
            d.swipe(500, 500, 500, 1500)
            time.sleep(10)

            c = time.time()
            b = c

        except Exception as e:
            logger.error("今日头条元素定位出错！" + str(e))
            d.app_stop("com.ss.android.article.news")

    logger.info("今日头条新闻浏览结束")
    time.sleep(1)
    d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮今日头条结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮今日头条总共耗时：%s" % ( str(expend_time).split('.')[0]))

