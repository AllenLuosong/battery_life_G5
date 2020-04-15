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
后置摄像头拍一张照，点击图库，把刚刚拍的放大缩小，
然后前置摄像头拍一张照，点击图库，把刚刚拍的放大缩小，
反复操作3分钟

"""


def camertest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("相机开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)

            d.app_start("com.gree.camera")
            logger.info("打开相机应用")
            # 暂停
            time.sleep(5)
            # 点击拍照按钮（后置摄像头）
            d(resourceId="com.gree.camera:id/photo_shutter_button_photo").click()
            logger.info("点击了后置拍照")
            time.sleep(5)
            # 点击图库按钮
            d(resourceId="com.gree.camera:id/thumbnailimg").click()
            logger.info("切换到了图库")
            # 图片放大缩小 两指从坐标（x,y） (m,n)移动到（a,b） (c,d)
            time.sleep(2)

            d().gesture((0.317, 0.333), (0.779, 0.673), (0.385, 0.425), (0.504, 0.509))
            logger.info("缩放图片")
            # 返回
            time.sleep(5)
            d.press("back")
            time.sleep(2)
            logger.info("切换前置摄像头")
            # 切换到前摄像头
            d(resourceId="com.gree.camera:id/switch_camera_facing").click()
            time.sleep(5)
            # 点击拍照按钮（前置摄像头）
            d(resourceId="com.gree.camera:id/photo_shutter_button_photo").click()
            logger.info("点击了拍照")
            time.sleep(5)
            # 点击图库按钮
            d(resourceId="com.gree.camera:id/thumbnailimg").click()
            logger.info("切换到了图库")
            # 图片放大缩小 两指从坐标（x,y） (m,n)移动到（a,b） (c,d)
            time.sleep(2)

            d().gesture((0.317, 0.333), (0.779, 0.673), (0.385, 0.425), (0.504, 0.509))
            logger.info("缩放图片")
            # 返回
            d.press("back")
            time.sleep(5)
            # 返回前置摄像头
            d(resourceId="com.gree.camera:id/switch_camera_facing").click()
            time.sleep(5)


        except Exception as e:
            logger.error("相机元素定位出错！" + str(e))
            d.app_stop("com.gree.camera")
            pass
        c = time.time()
        b = c
        time.sleep(2)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮相机结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮相机总共耗时：%s" % (str(expend_time).split('.')[0]))
