__author__ = "HuanXin"
from typing import Optional

import nonebot
from pydantic import BaseModel


class Config(BaseModel):
    # 插件版本号勿动！！！！
    hx_version: Optional[str] = "1.1.0"
    # 你的appid
    yinying_appid: Optional[str] = None
    yinying_token: Optional[str] = None
    hx_path: Optional[str] = None

global_config = nonebot.get_driver().config