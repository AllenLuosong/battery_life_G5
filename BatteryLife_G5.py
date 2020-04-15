#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Allen Luo


import datetime
import logging
import os
import re
import subprocess
import sys
import threading
import time

import schedule
import uiautomator2 as u2
from dingtalkchatbot.chatbot import DingtalkChatbot

import Browser_G5
import Camera_G5
import Dialer_G5
import Douyin_G5
import QQ_G5
import Taobao_G5
import Wangzherongyao_G5
import Wechat_G5
import Weibo_G5
import Aiqiyi_G5
import Toutiao_G5
from Settings_G5 import Devices

#############
#
# 构建一个实现统计应用程序耗电的程序
# 开启双线程运行，一个线程执行应用程序常规操作，另一个监控当前电量。
# 将测试日志以时间格式命名写进当前目录中，并发送钉钉消息通知测试结束
# 微信，QQ各两个测试账号，实现账号之间信息互发
##############

# 定义一个处理打印日志的方法
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('[%(asctime)s]-[%(name)s]-[%(levelname)s]-%(message)s')
file_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
result_root = '{}//'.format(file_time)
if not os.path.exists(result_root):  # 如果目录不存在则创建
    os.makedirs(result_root)
logfile = result_root + '{}.log'.format(file_time)
handler = logging.FileHandler(logfile)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


device_settings = Devices()
d = u2.connect_usb(device_settings.device)

def test_pre():
    # 使用usb连接电脑，测试开始前模拟执行如下命令，模拟断电，正常耗电。
    os.system("adb shell dumpsys battery unplug")
    # 测试开始前重置电量信息
    os.system("adb shell dumpsys batterystats --reset")
    print('\033[1;40;43m 测试运行中，请谨慎关闭窗口... \033[0m')  # 有高亮
    print('\033[1;40;32m 测试运行中，请谨慎关闭窗口... \033[0m')  # 有高亮
    print('\033[1;31;40m 测试运行中，请谨慎关闭窗口... \033[0m')  # 有高亮


def get_device():
    # 连接手机
    try:
        # 引用Settings文件中的配置项
        logger.info("设备串号：%s" % device_settings.device)
        d.healthcheck()
        if not d.info['screenOn']:  # 监测屏幕是否休眠 如是则解锁点亮屏幕
            d.healthcheck()  # 解锁屏幕
            time.sleep(1)
        # 开启uiautomator 防止重复启动
        d.service("uiautomator").start()
        # 如果没有找到设备 10秒后关闭程序
    except BaseException as e:
        logger.error("设备连接异常" + str(e))
        i = 11
        a = 1
        while a < i:
            i = i - 1
            time.sleep(1)
            print("%s 秒后将关闭窗口" % i)
        sys.exit()


def get_battery():
    """
    定义该方法获取当前测试设备的电池电量
    写死G5手机电池总电量为5000毫安时
    通过电池电量损耗判断是否退出程序
    :return:
    """
    cmd = "adb shell dumpsys batterystats"
    out_count = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE).stdout.readlines()
    for line in out_count:
        line_ = line.decode('utf-8').strip()
        # 构建一个正则表达式获取电量信息，输出电池容量Capacity及消耗电量drain
        # re.findall匹配出的结果为一个列表，会输出空列表
        electric_Capacity = re.findall('Capacity:(.*)Computed drain', line_)
        electric_drain = re.findall('Computed drain:(.*)actual drain', line_)
        # 获取列表不为空的数据
        if len(electric_Capacity) != 0 and len(electric_drain) != 0:
            # 将列表转化为字符串
            Capacity_str = "".join(electric_Capacity)
            drain_str = "".join(electric_drain)
            # Capacity = Capacity_str.strip().replace(',', '')
            Capacity = 5000
            drain = drain_str.strip().replace(',', '')
            remian = float(Capacity) - float(drain)
            logger.info("电池总电量：%s" % Capacity)
            logger.info("已用电量：%s" % drain)
            logger.info("剩余电量：%s" % str(remian))

            # 判断耗电量是否大于等于电池总量 float(Capacity)
            if float(drain) >= float(Capacity):
                # 将电池信息格式化输出
                b = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                # 导出测试结束电池电量信息
                os.system("adb shell dumpsys batterystats > %sbatterystats.txt" % b)
                logger.info("电池数据已下载")
                # 导出测试结束时内存信息
                os.system("adb shell dumpsys meminfo > %smeminfo.txt" % b)
                logger.info("内存数据已下载")
                # 获取测试结束时间
                end_time = datetime.datetime.now()
                logger.info("结束测试时间： %s" % (str(end_time).split('.')[0]))
                # 计算耗时
                expend_time = end_time - start_time
                logger.info("总共耗时： %s" % (str(expend_time).split('.')[0]))
                # 测试结束后模拟恢复供电
                os.system("adb shell dumpsys battery reset")
                logger.info("已供电")
                logger.info("--------**测试结束**--------")
                d.press("home")  # 回到桌面
                time.sleep(5)
                # WebHook地址
                webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
                          '=1c7fcc4ca062b497c3ff8af75608cf65ed4c719bf71a838b3e81efe19c281556 '
                # 初始化机器人小丁
                xiaoding = DingtalkChatbot(webhook)
                # 通知指定的用户
                at_mobiles = ['13530195722']
                # 测试结束Markdown消息@指定用户
                xiaoding.send_text(msg='G5续航测试结束！耗时：' + (str(expend_time).split('.')[0]), at_mobiles=at_mobiles, is_at_all=False)
                time.sleep(5)
                sys.exit()


def run_test():
    """
    定义run_test运行应用程序，执行常规操作
    :return:
    """
    n = 1
    while True:

        Aiqiyi_G5.aiqiyitest(logger)
        logger.info("--------**第%s轮爱奇艺结束**--------" % n)
        time.sleep(5)

        Douyin_G5.douyin(logger)
        logger.info("--------**第%s轮抖音结束**--------" % n)
        time.sleep(5)


        QQ_G5.qqtest(logger)
        logger.info("--------**第%s轮QQ结束**--------" % n)
        time.sleep(5)

        Dialer_G5.dialer(logger)
        logger.info("--------**第%s轮拨号结束**--------" % n)
        time.sleep(5)

        d.press('power')  # 熄屏
        logger.info("5分钟熄屏开始")
        time.sleep(300)
        d.healthcheck()  # 唤醒解锁屏幕
        logger.info("5分钟熄屏结束")
        time.sleep(1)

        Taobao_G5.taobaortest(logger)
        logger.info("--------**第%s轮淘宝结束**--------" % n)
        time.sleep(5)

        Browser_G5.browser(logger)
        logger.info("--------**第%s轮浏览器结束**--------" % n)
        time.sleep(5)

        Camera_G5.camertest(logger)
        logger.info("--------**第%s轮相机结束**--------" % n)
        time.sleep(5)

        d.press('power')  # 熄屏
        logger.info("5分钟熄屏开始")
        time.sleep(300)
        d.healthcheck()  # 唤醒解锁屏幕
        logger.info("5分钟熄屏结束")
        time.sleep(1)

        Wangzherongyao_G5.wangzherongyaotest(logger)
        logger.info("--------**第%s轮王者荣耀结束**--------" % n)
        time.sleep(5)

        Weibo_G5.weibotest(logger)
        logger.info("--------**第%s轮微博结束**--------" % n)
        time.sleep(5)

        Wechat_G5.wechattest(logger)
        logger.info("--------**第%s轮微信结束**--------" % n)
        time.sleep(5)

        Toutiao_G5.toutiao(logger)
        logger.info("--------**第%s轮头条结束**--------" % n)
        time.sleep(5)

        d.press('power')  # 熄屏
        logger.info("5分钟熄屏开始")
        time.sleep(300)
        d.healthcheck()  # 唤醒解锁屏幕
        logger.info("5分钟熄屏结束")
        time.sleep(1)

        logger.info("--------**第%s轮测试结束**--------" % n)
        n += 1


def screen_light():
    """
    设置手机常亮亮度为125
    G5的亮度最大值为255
    将亮度条拉倒最大执行adb shell settings get system screen_brightness所得最大亮度值
    :return:
    """


    try:
        logger.info("将手机自动亮度调节功能关闭")
        os.popen("adb shell settings put system screen_brightness_mode 0")
        time.sleep(1)
        logger.info("设置常亮亮度为125")
        os.popen("adb shell settings put system screen_brightness 125")
    except Exception as e:
        logger.error("设置亮度出错" + str(e))
        d.press("home")


def set_audio():
    """
    设置媒体音量值为5
    根据adb shell media volume --get 获取最大音量值为15
    :return:
    """
    try:
        logger.info("将音量值设置为5")
        os.popen("adb shell media volume --set 5")
    except Exception as e:
        logger.error("设置音量出错" + str(e))
        d.press("home")


if __name__ == "__main__":
    #############
    # 执行多线程操作
    #############


    test_pre()
    get_device()
    screen_light()
    set_audio()

    # 获取测试开始时间
    start_time = datetime.datetime.now()
    logger.info("开始测试时间： %s" % (str(start_time).split('.')[0]))

    threading.Thread(target=get_battery, args=()).start()
    threading.Thread(target=run_test, args=(), daemon=True).start()  # 设置daemon守护线程 随着主线程的退出而退出
    schedule.every(2).seconds.do(get_battery)  # 每2秒刷新一下获取电量
    while True:
        schedule.run_pending()
        time.sleep(1)
