<!--
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

 * @Author         : huanxin996
 * @Date           : 2024-4-17
 * @LastEditors    : huanxin996
 * @LastEditTime   : 2024-4-22
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

## 配置项

> [!WARNING]
> GitHub 仓库中的文档为最新 DEV 版本，配置方式请参考 [PyPI](https://pypi.python.org/pypi/nonebot-plugin-hx-yinying) 上的文档。

> [!WARNING]
> 秩乱(乱乱)的联系方式如下，QQ:1660466270，官方qq群聊:175334224 [官网链接](https://chat.wingmark.cn/) .

> [!WARNING]
> 请注意，该项目是接入了乱乱的项目，你需要遵守api使用的 [规范](https://wingmark.feishu.cn/docx/NFgJddgQAotygKxXiu6cpyg5nqr)。

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

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

配置文件示例（默认模板）

```dotenv
yinying_appid=你的appid
yinying_token=你的token(不带bearer)
hx_path=C:\Users\user\Desktop
```


## Contributors ✨


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

