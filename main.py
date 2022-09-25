#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time

import robot.sdk.wcferry as WxSDK
from robot.base_robot import BaseRobot
from robot.configuration import Config


class Robot(BaseRobot):
    def __init__(self, sdk: WxSDK, config: Config) -> None:
        super().__init__(sdk, config)

    def processMsg(self, msg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        """

        self.printRawMsg(msg)  # 打印信息

        # 如果在群里被 @，回复发信人：“收到你的消息了！” 并 @他
        if self.isGroupChat(msg):  # 是群消息
            if self.isAt(msg):   # 被@
                if msg.roomId in self.config.GROUPS:  # 在配置的响应的群列表里
                    self.sendTextMsg(msg.roomId, "收到你的消息了！", msg.wxId)

        # 非群聊信息
        elif msg.type == 37:     # 好友请求
            self.autoAcceptFriendRequest(msg)

        elif msg.type == 10000:  # 系统信息
            nickName = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
            if nickName:
                # 添加了好友，更新好友列表
                self.allContacts[msg.wxId] = nickName


def main():
    robot = Robot(WxSDK, Config())
    robot.initSDK()
    robot.enableRecvMsg()

    while True:
        time.sleep(1)
        # 不让进程退出，否则机器人就退出了


if __name__ == "__main__":
    main()
