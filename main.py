import json
import os
import random
import re
import time
from urllib.parse import urlencode

import requests


class Quark:
    def __init__(self, cookie):
        self.cookie = cookie

    def get_growth_info(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        headers = {"cookie": self.cookie}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        payload = {"sign_cyclic": True}
        headers = {"cookie": self.cookie}
        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring).json()
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def get_account_info(self):
        url = "https://pan.quark.cn/account/info"
        querystring = {"fr": "pc", "platform": "pc"}
        headers = {"cookie": self.cookie}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def do_sign(self):
        msg = ""
        # 验证账号
        account_info = self.get_account_info()
        if not account_info:
            msg = f"\n❌该账号登录失败，cookie无效"
        else:
            log = f" 昵称: {account_info['nickname']}"
            msg += log + "\n"
            # 每日领空间
            growth_info = self.get_growth_info()
            if growth_info:
                if growth_info["cap_sign"]["sign_daily"]:
                    log = f"✅ 执行签到: 今日已签到+{int(growth_info['cap_sign']['sign_daily_reward'] / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})"
                    msg += log + "\n"
                else:
                    sign, sign_return = self.get_growth_sign()
                    if sign:
                        log = f"✅ 执行签到: 今日签到+{int(sign_return / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})"
                        msg += log + "\n"
                    else:
                        msg += f"✅ 执行签到: {sign_return}\n"

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

    wait = random.randint(5, 52)
    time.sleep(wait)

    message_all = []
    title = 'quark-签到结果'
    message = ''
    for i in range(1, 4):
        cookie = os.environ.get('COOKIE' + str(i))
        if not cookie:
            cookie = ''

        if len(cookie) > 0:
            msg = Quark(cookie).do_sign()
            if not msg:
                msg = ''
            if len(msg) > 0:
                message_all.append(msg)
        else:
            print('COOKIE' + str(i) + ' 为空,不执行签到')

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
