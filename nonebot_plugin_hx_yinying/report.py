from io import BytesIO
import os
from PIL import Image,ImageFilter
from .chat import(
    file_get,
    path_in,
    create_dir_usr,
)
from nonebot import get_plugin_config
from nonebot_plugin_htmlrender import template_to_pic
from pathlib import Path
from loguru import logger
import traceback
import sys
from nonebot.message import run_postprocessor
from nonebot.adapters.onebot.v11 import (
   Bot,  MessageEvent ,MessageSegment
)
from .config import Config

##由星佑的oops修改而来
file = path_in()
image_dir = str(Path(__file__).parent / "error_report")
hx_config = get_plugin_config(Config)

#背景图片尝试模糊处理（下一步更新）
async def pictures_bj(file, radius)-> BytesIO:
    if not file:
        return False
    else:
        try:
            img_data = file_get(file)
            image = Image.open(img_data)
            if not isinstance(radius, int) or radius < 0:
                raise ValueError("radius必须是非负整数")
            blur_radius = int(radius)
            blur_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
            if os.path.exists(f"{image_dir}/file/image"):
                blur_image.save(f"{image_dir}/file/image/bg_mohu.png",format="png")
                return True
            else:
                create_dir_usr(f"{image_dir}/file/image")
                blur_image.save(f"{image_dir}/file/image/bg_mohu.png",format="png")
                return True
        except Exception as e:
            print(f"处理图像时发生错误: {str(e)}")
            return False

class BotRunTimeError(Exception):
    """bot runtime error"""
    
#崩溃返回图片化
async def crash_oops(err_values:Exception = None):
    if err_values == None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        data = traceback.format_exc()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)[-1]
        error_values = error.split(":",1)[-1]
        data = data.replace('\n','<br>')
    else:
        error_values=err_values
        newline_char = '<br>'
        data = f'{newline_char.join(err_values.args)}'
    template_path = str(Path(__file__).parent / "error_report") #同文件夹下面的
    htmlimage = await template_to_pic(
                template_path=template_path,
                template_name="hx_error.html",
                templates={
                    "verision":hx_config.hx_version,
                    "error":error_values,
                    "data": data,
                })
    return htmlimage

@run_postprocessor
async def post_run(bot: Bot, event: MessageEvent, e: Exception) -> None:
    img = await crash_oops(e)
    try:
        id = event.group_id
        await bot.call_api("send_group_msg",group_id=id,message=MessageSegment.image(img))
    except:
        raise BotRunTimeError("遇到未知错误,请自行扒拉日志!")
    logger.info(f"[Hx]:报错处理：{e}")