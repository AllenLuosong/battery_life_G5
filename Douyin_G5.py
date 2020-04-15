#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
from time import sleep
from Settings_G5 import Devices
import datetime
import sys
import os
"""
抖音视频界面每隔15秒上下滑动一次，反复操作10分钟
"""


def douyin(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("抖音开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a

    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")  # 回到桌面
            # 进入抖音界面
            d.app_start("com.ss.android.ugc.aweme")
            logger.info("打开了抖音")
            time.sleep(10)
            # 必须要运行监测器
            d.watcher('Permission_c').when(text='好的').click()
            d.watcher('Permission_d').when(text='以后再说').click()
            d.watcher('Permission_j').when(text='我知道了').click()
            d.watcher('Permission_k').when(text='稍后').click()
            d.watcher('Permission_l').when(text='取消').click()
            d.watcher("Permission_c").watched = True
            d.watcher("Permission_d").watched = True
            d.watcher("Permission_j").watched = True
            d.watcher("Permission_k").watched = True
            d.watcher("Permission_l").watched = True


            # 定位关注
            d(text="关注").click()
            logger.info("点击了关注")
            time.sleep(15)
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
        except Exception as e:
            logger.error("抖音元素定位出错！" + str(e))
            d.app_stop("com.ss.android.ugc.aweme")

        c = time.time()
        b = c
        time.sleep(1)
        d.press("home")
    end_time = datetime.datetime.now()
    logger.info("本轮抖音结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮抖音总共耗时：%s" % (str(expend_time).split('.')[0]))
