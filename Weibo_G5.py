#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo

import uiautomator2 as u2
import time
from Settings_G5 import Devices
import datetime

"""
热门微博滑动浏览，测试方法：往下2次，往上1次，往右滑到最右，往左滑到最左，
重复10分钟
"""


def weibotest(logger):
    # 引用Settings文件中的配置项
    device_settings = Devices()
    # 设备信息
    d = u2.connect_usb(device_settings.device)
    time.sleep(2)
    if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
        d.healthcheck()
    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("微博开始时间： %s" % (str(start_time).split('.')[0]))
    a = time.time()
    b = a
    while b - a < 600:  # 设置运行时间大于 b - a 时跳出循环,其中b - a单位是秒
        try:
            if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
                d.healthcheck()
                time.sleep(2)
            d.press("home")
            # 打开微博
            d.app_start("com.sina.weibo")
            logger.info("启动了微博")
            time.sleep(10)
            # 必须要运行监测器
            
            d.watcher('Permission_b').when(resourceId="com.sina.weibo:id/iv_close").click()
            d.watcher('Permission_i').when(text='不了，谢谢').click()
            d.watcher('Permission').when(text='以后再说').click(text='以后再说')  # 如果出现以后再说点击
           
            d.watcher("Permission_b").watched = True
            d.watcher("Permission_i").watched = True
            d.watcher("Permission").watched = True


            d.xpath('//*[@content-desc="首页"]').click()
            time.sleep(1)
            # 点击推荐
            d.xpath('//*[@text="关注"]')
            logger.info("点击了关注")
            # time.sleep(2)
            logger.info("开始上下滑动")
            # 滑动操作
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 1500, 500, 500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.swipe(500, 500, 500, 1500)
            time.sleep(15)
            d.press("home")

        except Exception as e:
            logger.error("微博元素定位出错！" + str(e))
            d.app_stop("com.sina.weibo")
        c = time.time()
        b = c
        time.sleep(1)
        d.press("home")

    end_time = datetime.datetime.now()
    logger.info("本轮微博结束时间： %s" % (str(end_time).split('.')[0]))
    expend_time = end_time - start_time
    logger.info("本轮微博总共耗时：%s" % ( str(expend_time).split('.')[0]))
