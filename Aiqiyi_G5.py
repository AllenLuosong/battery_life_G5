#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
from Settings_G5 import Devices
import datetime

"""
搜索楚乔传第一集观看10分钟
"""


def aiqiyitest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("爱奇艺开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")
            # 打开微博
            d.app_start("com.qiyi.video")
            logger.info("启动了爱奇艺")
            time.sleep(10)
            # 必须要运行监测器
            d.watcher('Permission_a').when(text='允许').click()
            d.watcher('Permission_b').when(resourceId="com.qiyi.video:id/dialog_close").click()
            d.watcher('Permission_i').when(text='不了，谢谢').click()
            d.watcher('Permission').when(text='暂不升级').click(text='暂不升级')  # 如果出现以后再说点击
            d.watcher("Permission_a").watched = True
            d.watcher("Permission_b").watched = True
            d.watcher("Permission_i").watched = True
            d.watcher("Permission").watched = True

            # 点击搜索框
            d.click(0.347, 0.073)
            time.sleep(1)
            logger.info("输入楚乔传搜索")
            # 输入楚乔传并搜索
            d(focused=True).set_text("楚乔传")
            d(text="搜索").click()
            time.sleep(2)
            d.click(0.118, 0.429)
            logger.info("开始播放第一集")
            time.sleep(2)
            if (d(text="继续播放").exists):
                d(text="继续播放").click()
            i = 0
            while i < 10:
                d.swipe(500, 1800, 500, 1000)
                time.sleep(30)
                d.swipe(500, 1000, 500, 1800)
                time.sleep(30)
                i += 1
            c = time.time()
            b = c

        except Exception as e:
            logger.error("爱奇艺元素定位出错！" + str(e))
            d.app_stop("com.qiyi.video")

        logger.info("10分钟播放结束")
        d.press("back")
        time.sleep(2)
        d.press("back")
        time.sleep(2)
        d.press("back")
        time.sleep(1)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮爱奇艺结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮爱奇艺总共耗时：%s" % (str(expend_time).split('.')[0]))
