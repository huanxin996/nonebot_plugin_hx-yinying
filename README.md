<!--
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

 * @Author         : huanxin996
 * @Date           : 2024-4-17
 * @LastEditors    : huanxin996
 * @LastEditTime   : 2024-4-26
 * @Description    : None
 * @GitHub         : https://github.com/huanxin996
-->

<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://skin.huanxinbot.com/"><img src="https://skin.huanxinbot.com/api/hx_img.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_hx-yinying

_✨ Hx vs YinYing(在线与银影进行对话的插件) ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-hx-yinying">
    <img src="https://skin.huanxinbot.com/api/pypi.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
</p>

## 安装
pip安装
```dotenv
pip install nonebot-plugin-hx-yinying
```
nb plugin安装
```dotenv
nb plugin install nonebot-plugin-hx-yinying
```


## 使用方式

通用:

- @Bot 或者回复即可

OneBot:

- @Bot
- 回复Bot


<details>
  <summary><b style="font-size: 1.5rem">指令集</b></summary>

/hx
- 别名：chat
- 主要对话命令

/刷新对话
- 别名：clear
- 主动刷新对话

/导出对话
- 别名：getchat
- 导出对话记录，没有对话记录会出错。

/设置全局配置
- 别名：设置配置全局，globalset
- 设置bot的全局配置

/导出全局配置
- 别名：getset_global
- 导出bot的全局配置
- 该命令包含在"设置全局配置"里

/模型列表
- 别名：modellist，chat模型列表
- 发送bot可用模型

/切换模型 [模型id]
- 别名：qhmodel，切换chat模型，模型切换
- 切换bot当前使用的模型
- 私聊群聊动态响应，如果在群内输入则切换群内加载的模型，私聊输入则切换私聊的。

/easycyber
- 别名：easycyber设置，hxworld
- 模型easycyberfurry主要配置
- 内有多个指令

/控制台操作
- 别名：管理控制台，setstart
- 模型easycyberfurry的角色投稿管理，即将更新cyber的角色投稿管理
- 内有多个指令

/确认版本
- 别名：旅行伙伴确认，版本确认
- 确认bot当前使用的版本和当前加载的模型。区分群聊和私聊动态响应

/sd [名称] [设定]
- 别名：旅行伙伴加入，设定加入
- [名称]可为空，即发送 旅行伙伴加入 [设定]
- [设定]不可为空，必填
- 载入用户的设定信息和自定义昵称












</details>
<br>

## 配置项

> [!WARNING]
> GitHub 仓库中的文档为最新 DEV 版本，配置方式请参考 [PyPI](https://pypi.python.org/pypi/nonebot-plugin-hx-yinying) 上的文档。

> [!WARNING]
> 秩乱(乱乱)的联系方式如下，QQ:1660466270，官方qq群聊:175334224 [官网链接](https://chat.wingmark.cn/) .

> [!WARNING]
> 请注意，该项目是接入了乱乱的项目，你需要遵守api使用的 [规范](https://wingmark.feishu.cn/docx/NFgJddgQAotygKxXiu6cpyg5nqr)。

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。
<details>
  <summary><b style="font-size: 1.5rem">配置项列表</b></summary>

### yinying_appid

- 类型：`str`
- 默认值：`None`
- 说明：你的appid
- 重要：必填

### yinying_token

- 类型：`str`
- 默认值：`None`
- 说明：这里写你找秩乱获取到的api_key
- 重要：必填

### hx_path
- 类型：`str`
- 默认值：`None`
- 说明：这里是插件本地配置的存储目录
- 重要：非必填

### SUPERUSERS
- 类型：`list`
- 默认值：`None`
- 说明：这里是超级管理员（插件）
- 重要：必填（你需要这个来管理该插件）

### image_check_appid
- 类型：`str`
- 默认值：`None`
- 说明：这里是阿里云图像检查的appid
- 重要：非必填

### image_check_token
- 类型：`str`
- 默认值：`None`
- 说明：这里是阿里云图像检查的token
- 重要：非必填

### smms_token
- 类型：`str`
- 默认值：`None`
- 说明：这里是smms的token（图床）
- 重要：非必填（可在填写smms_username和smms_password）后通过bot窗口获取。

### smms_username
- 类型：`str`
- 默认值：`None`
- 说明：这里是smms的账号id（图床）
- 重要：非必填必填（若smm_token为空，则需要填写账号密码）

### smms_password
- 类型：`str`
- 默认值：`None`
- 说明：这里是smms的密码（图床）
- 重要：非必填（若smm_token为空，则需要填写账号密码）

</details>
<br>

配置文件示例（默认模板）

```dotenv
yinying_appid=你的appid
yinying_token=你的token(不带bearer)
hx_path=C:\Users\user\Desktop
SUPERUSERS=["114514"]
image_check_appid=你的appid
image_check_token=你的token
smms_token=你获取到的token
smms_username=114514
smms_password=114514
```

## 本地各类config详解

<details>
<summary><b style="font-size: 1.3rem">config_global.json</b></summary>

在写了在写了
</details>
<br>

<details>
<summary><b style="font-size: 1.3rem">config_group.json</b></summary>

在写了在写了
</details>
<br>

<details>
<summary><b style="font-size: 1.3rem">config_user.json</b></summary>

在写了在写了
</details>
<br>

## Contributors ✨


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

