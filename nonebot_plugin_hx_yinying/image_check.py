# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_imageaudit20191230
import io,requests
from nonebot import get_plugin_config
from nonebot.log import logger
from urllib.request import urlopen
from alibabacloud_imageaudit20191230.client import Client
from alibabacloud_imageaudit20191230.models import ScanImageAdvanceRequestTask, ScanImageAdvanceRequest
from alibabacloud_tea_util.models import RuntimeOptions
from .smms import SMMS
from PIL import Image
from .config import Config as config_hx
from alibabacloud_tea_openapi.models import Config


hx_config = get_plugin_config(config_hx)

config = Config(
  access_key_id=hx_config.image_check_appid,
  access_key_secret=hx_config.image_check_token,
  endpoint='imageaudit.cn-shanghai.aliyuncs.com',
  region_id='cn-shanghai'
)

async def image_upload(url:str)->str:
    smms = SMMS()
    url = url.replace("https","http")
    img0 = urlopen(url).read()
    image = Image.open(io.BytesIO(img0))
    imgByteArr = io.BytesIO()
    image.save(imgByteArr,format="png")
    file = await smms.upload(imgByteArr)
    if file:
        logger.debug(f"[Hx]图片上传成功，图床链接为:{file}")
        return file
    else:
        logger.error("[Hx]图片上传失败")
        return False




async def image_check(url:str)->str:
    img0 = await image_upload(url)
    if hx_config.image_check_appid == None or hx_config.image_check_token == None:
        logger.warning("[Hx]未配置图像检测，若因图像违规导致被封开发者id，插件开发者概不负责！！！")
    if img0:
        logger.debug("[Hx]尝试检查图片【爱来自阿里】")
        runtime_option = RuntimeOptions()
        img = requests.get(img0).content
        task1 = ScanImageAdvanceRequestTask()
        task1.image_urlobject=io.BytesIO(img)
        scan_image_request = ScanImageAdvanceRequest(
        task=[task1],
        scene=['porn']
        )
        try:
            client = Client(config)
            response = client.scan_image_advance(scan_image_request, runtime_option)
            back = response.body.to_map()
            msg0 = back["Data"]["Results"][0]["SubResults"][0]["Rate"]
            logger.debug(msg0)
            if msg0 <= 0.6:
                logger.warning(f"[Hx]图片违规，请重新上传")
                msg = False
            else:
                msg = img0
            return msg
        except Exception as e:
            return False
    else:
        return False