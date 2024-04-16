__author__ = "HuanXin"
from typing import Optional

import nonebot
from pydantic import BaseModel


class Config(BaseModel):
    # 配置文件版本号
    hx_version: int = 1

    # model，如 yinying-v3
    yinying_model: Optional[str] = None
    furbar_model: Optional[str] = None

    yinying_token: Optional[str] = None

    # api地址
    hx_api_yinying: Optional[str] = None
    hx_api_furbar: Optional[str] = None
    hx_path: Optional[str] = None
    # bot回复消息时是否艾特
    hx_reply_at: bool = False

    yinying_limit: int = 12

global_config = nonebot.get_driver().config