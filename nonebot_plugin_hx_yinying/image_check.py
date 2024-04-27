# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_imageaudit20191230
import os
import io
from nonebot import get_plugin_config
from urllib.request import urlopen
from alibabacloud_imageaudit20191230.client import Client
from alibabacloud_imageaudit20191230.models import ScanImageAdvanceRequestTask, ScanImageAdvanceRequest
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from .config import Config

hx_config = get_plugin_config(Config)

config = Config(
  # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html
  # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html
  # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
  access_key_id=hx_config.image_check_appid,
  access_key_secret=hx_config.image_check_token,
  endpoint='imageaudit.cn-shanghai.aliyuncs.com',
  region_id='cn-shanghai'
)

async def image_upload(url:str)->str:
    img = urlopen(url).read()
    task = ScanImageAdvanceRequestTask()
    task.image_urlobject=io.BytesIO(img)
    #等更新

async def image_check(url:str)->str:
    runtime_option = RuntimeOptions()
    img = urlopen(url).read()
    task = ScanImageAdvanceRequestTask()
    task.image_urlobject=io.BytesIO(img)
    scan_image_request = ScanImageAdvanceRequest(
    task=[
        task
    ],
    scene=[
        'logo',
        'porn'
    ]
    )
    try:
        client = Client(config)
        response = client.scan_image_advance(scan_image_request, runtime_option)
        print(response.body)
    except Exception as error:
        print(error)
        print(error.code)