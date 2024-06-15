# 如何使用？ 
## 一、更新记录

2024年6月15日11:09:46

第一次更新

## 二、使用说明

1、Fork项目到自己的仓库

2、点击Settings -> 点击选项卡 Secrets and variables -> 点击Actions -> New repository secret

(1)目前预设3个，再多个的话，需要对应调整下代码，也很简单

因为考虑cookie中的特殊字符，暂时不考虑用字符拼接多个，再去py里切割的方案

(2)关于Bark推送，不用的话填空即可


    | Name   | Secret                           |
    | ------ | ------------------------------- |
    | COOKIE1  | 第一个Cookie |
    | COOKIE2  | 第二个Cookie |
    | COOKIE3  | 第三个Cookie |
    | BARK_DEVICEKEY  | IOS应用Bark 推送密钥 |
    | BARK_ICON  | IOS应用Bark 推送的图标 |

3、点击Actions -> 选择quark-sign -> 点击Run workflow 运行即可

4、关于签到的定时时间

近期发现服务器会在后半夜维护，页面提示：维护中..请5:20以后访问

所以定时的时间尽量在这个后面，暂时不研究遇到维护情况自动后延签到的逻辑实现

quarksign.yml，调整 \- cron: 20 21 * * *，对应北京时间5:20

5、参考仓库

感谢 https://github.com/mushichou/quark_auto_sign 提供思路

