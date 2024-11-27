import nonebot
from typing import Optional, Set
from pydantic import BaseModel

class Config(BaseModel):
    # 插件版本号勿动！！！！
    hx_version: Optional[str] = "1.4.0"
    # 秩乱v你的appid
    yinying_appid: Optional[str] = None
    #自定义命令头，默认为hx chat yinying
    hx_chatcommand: Set[str] = {"chat","yinying"}
    yinying_token: Optional[str] = None
    # 插件数据文件存储路径，可不填。
    hx_path: Optional[str] = None

global_config = nonebot.get_driver().config