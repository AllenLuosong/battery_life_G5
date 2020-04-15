#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
import datetime
from time import sleep
from Settings_G5 import Devices

"""
王者登录界面进行测试,反复操作5分钟			

"""


def wangzherongyaotest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 开启uiautomator 防止重复启动
    d.service("uiautomator").start()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("王者荣耀开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 300:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.app_start('com.tencent.tmgp.sgame')
            logger.info("启动王者荣耀")
            time.sleep(30)
            
        except Exception as e:
            logger.error("王者荣耀元素定位出错！" + str(e))
            d.app_stop('com.tencent.tmgp.sgame')

        c = time.time()
        b = c
        time.sleep(2)
        d.app_stop('com.tencent.tmgp.sgame')

    end_time = datetime.datetime.now()
    logger.info("本轮王者荣耀结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮王者荣耀总共耗时：%s" % (str(expend_time).split('.')[0]))
