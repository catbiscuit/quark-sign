import json
import os
import random
import re
import time
from urllib.parse import unquote

import requests


class Quark:
    '''
    Quark类封装了登录验证、签到、领取签到奖励的方法
    '''

    def __init__(self, user_data):
        '''
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        '''
        self.param = user_data

    def convert_bytes(self, b):
        '''
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        '''
        b = b / (1024 * 1024)
        if len(str(b).split('.')[0]) < 4:
            return f"{round(b, 1)} MB"  # 返回 MB
        else:
            b = b / 1024
            if len(str(b).split('.')[0]) < 4:
                return f"{round(b, 1)} GB"  # 返回 GB
            else:
                b = b / 1024
                return f"{round(b, 1)} TB"  # 返回 TB

    def get_growth_info(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        response = requests.get(url=url, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        '''
        执行用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        response = requests.post(url=url, json=data, params=querystring).json()
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def do_sign(self):
        '''
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        '''
        msg = ""
        log = ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if growth_info:
            log = (
                f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
                f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
                f"签到累计容量：")
            if "sign_reward" in growth_info['cap_composition']:
                log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            else:
                log += "0 MB\n"
            if growth_info["cap_sign"]["sign_daily"]:
                log += (
                    f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                    f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})"
                )
            else:
                sign, sign_return = self.get_growth_sign()
                if sign:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})"
                    )
                else:
                    log += f"❌ 签到异常: {sign_return}"
        else:
            log += f"❌ 签到异常: 获取成长信息失败"
        msg += log + "\n"
        return msg

def bark(device_key, title, content, bark_icon):
    if not device_key:
        return 2

    url = "https://api.day.app/push"
    headers = {
        "content-type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "title": title,
        "body": content,
        "device_key": device_key
    }

    if not bark_icon:
        bark_icon = ''
    if len(bark_icon) > 0:
        url += '?icon=' + bark_icon
        print('拼接icon')
    else:
        print('不拼接icon')

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp_json = resp.json()
    if resp_json["code"] == 200:
        print(f"[Bark]Send message to Bark successfully.")
    if resp_json["code"] != 200:
        print(f"[Bark][Send Message Response]{resp.text}")
        return -1
    return 0

def main():
    bark_device_key = os.environ.get('BARK_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')

    wait = random.randint(4, 13)
    time.sleep(wait)

    message_all = []
    title = 'quark-签到结果'
    message = ''
    for i in range(1, 4):
        cookie = os.environ.get('COOKIE_QUARK' + str(i))
        if not cookie:
            cookie = ''

        if len(cookie) > 0:
            # 获取user_data参数
            user_data = {}  # 用户信息
            for a in cookie.replace(" ", "").split(';'):
                if not a == '':
                    user_data.update({a.split('=')[0]: unquote(a.split('=')[1])})

            msg = Quark(user_data).do_sign()
            if not msg:
                msg = ''
            if len(msg) > 0:
                message_all.append(msg)
        else:
            print('COOKIE_QUARK' + str(i) + ' 为空,不执行签到')

        sm = random.randint(15, 43)
        time.sleep(sm)

    if not message_all:
        message = '暂无执行结果'
    else:
        message_all = '\n'.join(message_all)
        message_all = re.sub('\n+', '\n', message_all).rstrip('\n')
        message = message_all

    bark(bark_device_key, title, message, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()
