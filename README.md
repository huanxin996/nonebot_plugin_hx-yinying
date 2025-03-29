<p align="center">
  <a href="https://github.com/huanxin996/nonebot_plugin_hx-yinying"><img src="https://raw.githubusercontent.com/huanxin996/nonebot_plugin_hx-yinying/main/.venv/hx_img.png" width="200" height="200" alt="yinying"></a>
</p>

<div align="center">

# Nonebot Plugin HX-YinYing

_✨ 一个基于 NoneBot2 的赛博小狼对话插件 ✨_

</div>

<p align="center">
  <a href="https://github.com/huanxin996/nonebot_plugin_hx-yinying/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/huanxin996/nonebot_plugin_hx-yinying.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-hx-yinying">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-hx-yinying" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
  <a href="https://github.com/huanxin996/nonebot_plugin_hx-yinying/releases">
    <img src="https://img.shields.io/github/v/release/huanxin996/nonebot_plugin_hx-yinying?include_prereleases" alt="release">
  </a>
  <a href="https://github.com/huanxin996/nonebot_plugin_hx-yinying/issues">
    <img src="https://img.shields.io/github/issues/huanxin996/nonebot_plugin_hx-yinying" alt="issues">
  </a>
</p>

## 📝 介绍

一个基于 NoneBot2 的赛博小狼对话插件，支持多种对话模式和配置选项。

## 🎯 特性

- 支持多种对话模式
- 可配置的角色系统
- 完善的权限管理
- 内置违禁词过滤
- 支持黑名单管理

## 💿 安装

<details>
<summary>使用 pip 安装（推荐）</summary>

```bash
pip install nonebot-plugin-hx-yinying
```
</details>

<details>
<summary>使用 nb-cli 安装</summary>

```bash
nb plugin install nonebot-plugin-hx-yinying
```
</details>

## ⚙️ 配置项

在 NoneBot2 项目的 `.env` 文件中添加下列配置项：

<details>
<summary>基础配置</summary>

```env
# YinYing 配置
YINYING_APPID="your_appid"              # API ID
YINYING_TOKEN="your_token"              # API Token
YINYING_SUPERUSERS=["123456"]           # 超级管理员列表
YINYING_DATA_DIR="C:/path/to/data"      # 数据存储目录（可选）

# 模型配置
YINYING_DEFAULT_MODEL="gpt3.5"          # 默认模型（可选）
YINYING_MAX_TOKENS=2000                 # 最大令牌数（可选）
```
</details>

## 🎮 使用方法

<details>
<summary>基础命令</summary>

```
yinying <内容>      # 直接对话
yinying text <内容>  # 发送消息
yinying help        # 显示帮助信息
```
</details>

<details>
<summary>配置管理</summary>

```
yinying.config help                    # 显示配置帮助
yinying.config global <键名> <值>      # 设置全局配置
yinying.config cyber <模式>            # 设置赛博世界模式
```
</details>

<details>
<summary>管理员功能</summary>

```
yinying.config admin blacklist add <用户ID>     # 添加用户到黑名单
yinying.config admin blacklist remove <用户ID>  # 从黑名单移除用户
yinying.config admin banword add <词语>         # 添加违禁词
yinying.config admin banword remove <词语>      # 移除违禁词
```
</details>

## 📋 TODO

- [ ] 多模型支持
- [ ] 角色记忆系统
- [ ] 对话导出功能
- [ ] Web 管理界面
- [ ] 对话历史管理
- [ ] 更多自定义选项

## 🤝 贡献

1. Fork 本仓库
2. 创建新的分支：`git checkout -b feature/xxxx`
3. 提交你的更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/xxxx`
5. 提交 Pull Request

## 🐛 问题反馈

如果您在使用过程中遇到任何问题，欢迎：

- [提交 Issue](https://github.com/huanxin996/nonebot_plugin_hx-yinying/issues/new)

## 📄 更新日志

<details>
<summary>点击展开</summary>

### v1.4.10 (2024-03-xx)
- 实现基础对话功能
- 添加配置管理系统
- 支持角色定制化
</details>

## 🙏 鸣谢

- [NoneBot2](https://github.com/nonebot/nonebot2)
- [其他依赖项...]

## 📄 许可

本项目采用 [MIT](./LICENSE) 许可证。