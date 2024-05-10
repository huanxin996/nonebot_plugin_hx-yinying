__author__ = "HuanXin"
from typing import List, Optional, Union
import nonebot
from pydantic import BaseModel,AnyHttpUrl,Field


class Config(BaseModel):
    # 插件版本号勿动！！！！
    hx_version: Optional[str] = "1.2.0"
    # 秩乱v你的appid
    yinying_appid: Optional[str] = None
    # 秩乱给你的token
    yinying_token: Optional[str] = None
    # 插件数据文件存储路径，可不填。
    hx_path: Optional[str] = None
    # 图像检查api，爱来自阿里云
    image_check_appid: Optional[str] = None
    image_check_token: Optional[str] = None
    #图床api修改
    smms_api_url: AnyHttpUrl = Field(default="https://sm.ms/api/v2")
    #图床token填入(优先使用这个，当这个不存在时尝试使用用户名称和密码获取token)
    smms_token: Optional[str] = None
    #smms图床token获取
    smms_username: Optional[str] = None
    smms_password: Optional[str] = None

global_config = nonebot.get_driver().config

class EmptyData(BaseModel):
    pass

class FileInfo(BaseModel):
    width: int
    height: int
    filename: str
    storename: str
    size: int
    path: str
    hash: str
    url: str
    delete: str
    page: str
    file_id: Optional[int] = None
    created_at: Optional[str] = None


class ApiResponse(BaseModel):
#smms图库api返回
    success: bool
    code: str
    message: Optional[str] = None
    images: Optional[str] = None
    data: Union[List[FileInfo], FileInfo, EmptyData, None] = None