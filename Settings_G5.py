# --coding:utf-8–
import os

"""
存储测试相关的配置信息

"""


class Devices:
    # 设备串号
    def __init__(self):
        cmd_output = os.popen("adb devices", "r").read().split()[4:]
        if len(cmd_output) < 1:
            print("检测到当前没有连接设备，请插入设备后重试！")

        for i in range(len(cmd_output)):
            if i % 2 == 0:  # 列表位置为偶数的全部为设备序列号，将device字符除去
                device_id = cmd_output[i]
                self.device = device_id
