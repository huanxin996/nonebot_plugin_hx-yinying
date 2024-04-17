<!--
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

 * @Author         : huanxin
 * @Date           : 2024-4-17 00:04:25
 * @LastEditors    : huanxin
 * @LastEditTime   : 2024-4-18 00:04:25
 * @Description    : None
 * @GitHub         : https://github.com/huanxin
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
  <a href="https://pypi.python.org/pypi/nonebot-plugin-status">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-status.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
</p>

## 使用方式

通用:

- @Bot 或者回复即可

OneBot:

- @Bot
- 回复Bot

## 配置项

> [!WARNING]
> GitHub 仓库中的文档为最新 DEV 版本，配置方式请参考 [PyPI](https://pypi.org/project/nonebot-plugin-status/) 上的文档。

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

### yinying_model

- 类型：`str`
- 默认值：`None`
- 说明：选择使用银影的模型

### yinying_token

- 类型：`str`
- 默认值：`None`
- 说明：这里写你找秩乱获取到的api_key


### hx_api_yinying

- 类型：`str`
- 默认值：`None`
- 说明：yinying的api地址


## hx_path
- 类型：`str`
- 默认值：`None`
- 说明：银影对话的用户数据存储路径(不写将使用默认配置)

## hx_reply
- 类型：`bool`
- 默认值：`False`
- 说明：bot发送chat消息时是否回复
- 注意：该项启用时hx_reply_at将被忽略

## hx_reply_at
- 类型：`bool`
- 默认值：`False`
- 说明：bot发送chat消息时不回复时是否艾特

## yinying_limit
- 类型：`int`
- 默认值：`12`
- 说明：对于银影对话限制的次数


配置文件示例（默认模板）

```dotenv
hx_api_yinying=https://地址
yinying_model=模型
yinying_token=你的token(不带bearer)
hx_reply_at=False
yinying_limit=12
```


## Contributors ✨


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

