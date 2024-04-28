###原作：https://github.com/mobyw/nonebot-plugin-smms
from io import BytesIO
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import ValidationError
import requests
from nonebot import get_driver,get_plugin_config
from nonebot.log import logger
from nonebot.drivers import HTTPClientMixin, Request
from .config import Config, ApiResponse, FileInfo
plugin_config = get_plugin_config(Config)

#尝试获取smms的用户token
def smms_gettoken():
    fails = 0
    while True:
        try:
            if fails >= 20:
                token = False
                break
            json = {
                "username": f"{plugin_config.smms_username}",
                "password": f"{plugin_config.smms_password}"
            }
            ret = requests.post(url="https://sm.ms/api/v2/token",data=json,timeout=50)
            if ret.status_code == 200:
                json = ret.json()
                token = json["data"]["token"]
            else:
                continue
        except:
            fails += 1
            logger.warning(f"{ret}")
            logger.warning("网络状况不佳，获取token失败！，正在重新尝试")
        else:
            break
    return token

class SMMS:
    driver: HTTPClientMixin
    headers: Dict[str, Any]

    def __init__(self):
        driver = get_driver()
        if not isinstance(driver, HTTPClientMixin):
            raise RuntimeError(
                f"你的bot配置文件里没有支持httpx "
                "http client requests! "
                "你需要在配置文件里添加\nDRIVER=~fastapi+~httpx"
            )
        if plugin_config.smms_token is None:
            logger.warning("[Hx]:No smms token is set!,尝试使用用户名称和密码来获取token")
            if plugin_config.smms_username is None or plugin_config.smms_password is None:
                 raise RuntimeError("[Hx]:未知用户！！！")
            else:
                token = smms_gettoken()
                logger.warning(f"[Hx]smms token: {token},推荐将此值填入.env文件或.env.prod文件中")
                self.driver = driver
                self.headers = {"Authorization": f"{token}"}
        else:
            self.driver = driver
            self.headers = {"Authorization": plugin_config.smms_token}

    async def upload(self, file: Union[bytes, Path, BytesIO]) -> Optional[FileInfo]:
        if isinstance(file, Path):
            smfile = file.read_bytes()
        elif isinstance(file, BytesIO):
            smfile = file.getvalue()
        else:
            smfile = bytes(file)
        request = Request(
            "POST",
            url=f"{plugin_config.smms_api_url}/upload",
            headers=self.headers,
            files={"smfile": smfile},
            timeout=60,
        )
        logger.debug("[Hx]尝试将qq图片上传至smms")
        response = await self.driver.request(request)
        if response.status_code != HTTPStatus.OK or response.content is None:
            logger.error(
                f"[Hx]smms上传失败 失败返回code: {response.status_code}"
            )
            return None
        try:
            content = ApiResponse.parse_raw(response.content)
        except ValidationError as e:
            logger.error(f"[Hx]上传失败 错误捕获为: {e}")
            return None
        if isinstance(content.images, str):
            logger.warning(f"[Hx]该图片已在库里！请勿重复发送图片or上传")
            #其实这里可以加个返回重复值的判断，但是我懒得写了
            return content.images
        elif not content.success or not isinstance(content.data, FileInfo):
            logger.error(f"[Hx]smms上传失败，smms_api返回信息: {content.message}")
            return None
        return content.data.url

    async def delete(self, hash: str):
        request = Request(
            "GET",
            url=f"{plugin_config.smms_api_url}/delete/{hash}",
            headers=self.headers,
            timeout=60,
        )
        logger.debug("[Hx]尝试从smms图床删除图片")
        response = await self.driver.request(request)
        logger.debug(
            f"[Hx]smms 删除api返回信息: {response.status_code} {response.content}"
        )
        if response.status_code != HTTPStatus.OK or response.content is None:
            logger.error(
                f"[Hx]smms删除图片失败 失败返回code: {response.status_code}"
            )
            return False
        try:
            content = ApiResponse.parse_raw(response.content)
        except ValidationError as e:
            logger.error(f"[Hx]删除失败 错误捕获为: {e}")
            return False
        if not content.success:
            logger.error(f"[Hx]删除失败 api返回信息: {content.message}")
            return False
        return True