# 如何使用？ 
## 一、更新记录

2024年7月15日16:08:42
调整逻辑

2024年6月15日11:09:46
初始化

## 二、使用说明

1、Fork项目到自己的仓库

2、点击Settings -> 点击选项卡 Secrets and variables -> 点击Actions -> New repository secret

(1)目前预设3个，再多个的话，需要对应调整下代码，也很简单

因为考虑cookie中的特殊字符，暂时不考虑用字符拼接多个，再去py里切割的方案

(2)关于Bark推送，不用的话填空即可


    | Name   | Secret                           |
    | ------ | ------------------------------- |
    | COOKIE_QUARK1  | 第一个Cookie |
    | COOKIE_QUARK2  | 第二个Cookie |
    | COOKIE_QUARK3  | 第三个Cookie |
    | BARK_DEVICEKEY  | IOS应用Bark 推送密钥 |
    | BARK_ICON  | IOS应用Bark 推送的图标 |

3、点击Actions -> 选择quark-sign -> 点击Run workflow 运行即可

4、关于签到的定时时间

quarksign.yml，调整 \- cron: 20 21 * * *，对应北京时间5:20