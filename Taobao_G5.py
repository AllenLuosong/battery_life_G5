#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo
import os

import uiautomator2 as u2
import time
import datetime
from time import sleep
from Settings_G5 import Devices
import sys
"""
淘宝首页搜索中分别搜索女包、女鞋、女裤、女衣后滑动界面，反复操作5分钟		
"""


def taobaortest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("淘宝开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")  # 回到桌面
            # 启动淘宝
            d.app_start("com.taobao.taobao")
            logger.info("启动了淘宝")
            time.sleep(10)
            d.watcher('Permission_e').when(text='取消').click(text='取消')
            d.watcher('Permission_f').when(text='允许').click(text='允许')
            d.watcher('Permission_g').when(description="关闭").click(text='关闭')
            d.watcher("Permission_e").watched = True
            d.watcher("Permission_f").watched = True
            d.watcher("Permission_g").watched = True



           
            logger.info("开始搜索")
            # 定位搜索框
            d(description="搜索").click()
            time.sleep(2)
            logger.info("搜索女鞋")
            # 输入女鞋搜索
            d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("女鞋")
            # 点击搜索按钮
            d(resourceId="com.taobao.taobao:id/searchbtn").click()
            time.sleep(5)
            logger.info("开始滑动")
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            # 定位搜索框
            d(resourceId="com.taobao.taobao:id/searchEdit").click()
            # 文本清除
            d.clear_text()
            time.sleep(2)
            logger.info("搜索女装")
            d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("女装")
            # 点击搜索按钮
            d(resourceId="com.taobao.taobao:id/searchbtn").click()
            logger.info("开始滑动")
            time.sleep(2)
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)

            # 定位搜索框
            d(resourceId="com.taobao.taobao:id/search_bar_wrapper").click()
            d.clear_text()
            time.sleep(2)
            logger.info("搜索女包")
            d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("女包")
            # 点击搜索按钮
            d(resourceId="com.taobao.taobao:id/searchbtn").click()
            logger.info("开始滑动")
            time.sleep(2)
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)

            # 定位搜索框
            d(resourceId="com.taobao.taobao:id/search_bar_wrapper").click()
            d.clear_text()
            time.sleep(2)
            logger.info("开始搜索女裤")
            d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("女裤")
            # 点击搜索按钮
            d(resourceId="com.taobao.taobao:id/searchbtn").click()
            time.sleep(5)
            logger.info("开始滑动")
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.press("back")
            time.sleep(1)
            d.press("back")
            time.sleep(1)
            d.press("back")
        except Exception as e:
            logger.error("淘宝元素定位出错！" + str(e))
            d.app_stop("com.taobao.taobao")
        c = time.time()
        b = c
        time.sleep(1)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮淘宝结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮淘宝总共耗时：%s" % ( str(expend_time).split('.')[0]))
