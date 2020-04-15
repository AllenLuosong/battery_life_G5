#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
import datetime
from Settings_G5 import Devices
import sys

"""
给gelitest发一条消息，两张图片，反复操作10分钟
"""


def qqtest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("QQ开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            # 启用qq
            d.app_start("com.tencent.mobileqq")
            logger.info("打开了QQ")
            time.sleep(5)
            # 点击联系人
            d.xpath('//*[@text="联系人"]').click()
            logger.info("点击了联系人")
            time.sleep(2)
            # 点击群聊
            d(text="群聊").click()
            time.sleep(2)
            d(text="gelitest").click()
            logger.info("点击gelitest")
            time.sleep(1)
            # 点击发送消息 输入文字
            d(resourceId="com.tencent.mobileqq:id/input").click()
            time.sleep(1)
            d(focused=True).set_text("格力续航测试123ABC")
            time.sleep(2)
            # 点击发送按钮
            d(text="发送").click()
            logger.info("发送了文字")
            time.sleep(2)
            # 点击图片
            d.click(0.267, 0.621)
            time.sleep(2)
            # 选中前两张图片
            d.click(0.421, 0.674)
            time.sleep(1)
            d.click(0.889, 0.683)
            time.sleep(2)
            # 点击发送按钮
            d(text="发送(2)").click()
            logger.info("发送了图片")
            time.sleep(2)
            # 返回上一个页面
            d.press("back")
            time.sleep(2)
            d.press("back")
            # 返回主页面
            time.sleep(2)
            d.press("home")

        except Exception as e:
            logger.error("QQ元素定位出错！" + str(e))
            d.app_stop("com.tencent.mobileqq")

        c = time.time()
        b = c
        time.sleep(1)

    end_time = datetime.datetime.now()
    logger.info("本轮QQ结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮QQ总共耗时：%s" % (str(expend_time).split('.')[0]))
