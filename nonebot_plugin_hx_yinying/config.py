__author__ = "HuanXin"
from typing import Optional

import nonebot
from pydantic import BaseModel


class Config(BaseModel):
    # 插件版本号勿动！！！！
    hx_version: Optional[str] = "1.1.2"
    # 秩乱v你的appid
    yinying_appid: Optional[str] = None
    # 秩乱给你的token
    yinying_token: Optional[str] = None
    # 插件数据文件存储路径，可不填。
    hx_path: Optional[str] = None
    # 图像检查api，爱来自阿里云
    image_check_appid: Optional[str] = None
    image_check_token: Optional[str] = None

global_config = nonebot.get_driver().config