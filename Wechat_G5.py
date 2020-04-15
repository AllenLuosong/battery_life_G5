#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo
import os

import uiautomator2 as u2
import time
import datetime
from Settings_G5 import Devices

"""
给gelitest发送文本消息/语音/图片，然后浏览朋友圈
反复操作10分钟
"""


def wechattest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("微信开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")
            # 启动微信
            d.app_start("com.tencent.mm")
            logger.info("启动了微信")
            # 暂停
            time.sleep(5)
            # 点击微信
            d(text='微信').click()
            time.sleep(5)
            # 点击通讯录
            d(text='通讯录').click()
            time.sleep(2)
            logger.info("点击通讯录")
            d(text='群聊').click()
            time.sleep(2)
            d(text='gelitest').click()
            logger.info("点击群聊")
            time.sleep(1)
            # 点击输入框
            d.click(200,2300)
            d.set_fastinput_ime(False)
            time.sleep(1)
            # 清除输入框
            d(focused=True).set_text("格力续航测试123ABC")
            d.set_fastinput_ime(False)
            time.sleep(1)
            # 点击发送按钮
            d(text='发送').click()
            logger.info("发送文字")
            time.sleep(2)
            # 点击+号
            d(description = "更多功能按钮，已折叠").click()
            # d.click(0.948, 0.907)
            time.sleep(1)
            # 选择相册按钮
            d(text="相册").click()
            time.sleep(1)
            #点击第1张图片
            d(className='android.widget.CheckBox').click()
            time.sleep(1)
            # 通过发送按钮文本字样定位
            d(text='发送(1/9)').click()
            logger.info("发送图片")
            time.sleep(2)
            # 切换到按住说话
            d.click(0.083, 0.974)
            time.sleep(1)
            # 定位到语音输入按钮
            # d(resourceId="com.tencent.mm:id/aqa").click()
            # 点击“按住说话”按钮3秒
            d(description='按住说话').long_click(3)
            logger.info("发送语音")
            # d(resourceId="com.tencent.mm:id/aqd").long_click(3)
            time.sleep(1)
            d(description='切换到键盘').click()
            time.sleep(1)
            # 返回到上一界面
            d.press("back")
            time.sleep(2)
            d.press("back")
            time.sleep(2)
            d.app_start("com.tencent.mm")
            time.sleep(1)
            # 定位到发现
            d(text='发现').click()
            time.sleep(2)
            # 定位到朋友圈
            d(text='朋友圈').click()
            logger.info("浏览朋友圈上下滑动")
            time.sleep(15)
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
            time.sleep(2)
            # 返回到桌面
            d.press("home")
        except Exception as e:
            logger.error("微信元素定位出错！" + str(e))
            d.app_stop("com.tencent.mm")
        c = time.time()
        b = c
        time.sleep(2)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮微信结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮微信总共耗时：%s" % (str(expend_time).split('.')[0]))


