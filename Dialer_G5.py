#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo


import uiautomator2 as u2
import time
from time import sleep
import datetime
from Settings_G5 import Devices
import sys

"""
拨打紧急电话112通话20秒然后挂断
反复操作5分钟
"""


def dialer(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("拨号开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 300:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")  # 回到桌面
            # 进入拨号界面
            d.app_start("com.android.dialer")  
            time.sleep(5)

            logger.info("点击112开始拨号")

            d(resourceId="com.android.dialer:id/one").click()
            time.sleep(1)
            d(resourceId="com.android.dialer:id/one").click()
            time.sleep(1)
            d(resourceId="com.android.dialer:id/two").click()
            time.sleep(1)
            d(resourceId="com.android.dialer:id/dialpad_floating_action_button").click()
            time.sleep(30)
            d(resourceId="com.android.dialer:id/incall_end_call").click()
            logger.info("结束112拨号")
            time.sleep(5)
            d.app_stop("com.android.dialer")  


        except Exception as e:
            logger.error("dialer元素定位出错！" + str(e))
            d.app_stop("com.android.dialer") 
            
        c = time.time()
        b = c
        time.sleep(5)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮拨号结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮拨号总共耗时：%s" % (str(expend_time).split('.')[0]))
