__author__ = "HuanXin"

import nonebot
from typing import Optional, Set, Any
from pydantic import BaseModel
from nonebot import get_plugin_config,require
from pathlib import Path
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

class Config(BaseModel):

    # 应用的appid
    yinying_appid: Optional[str] = None
    # 应用的token
    yinying_token: Optional[str] = None
    #自定义命令头，默认为hx chat yinying
    hx_chatcommand: Set[str] = ["hx","chat","yinying"]
    # 插件数据文件存储路径选择，为True则使用当前命令窗口目录，为False则使用插件目录。
    localstore_use_cwd : Optional[bool] = True
    plugin_cache_dir: Path = store.get_plugin_cache_dir()

class ConfigItem(BaseModel):
    """配置项定义"""
    key: str
    name: str
    value: Any
    description: Optional[str] = None

global_config = nonebot.get_driver().config
hxconfigs = get_plugin_config(Config)
