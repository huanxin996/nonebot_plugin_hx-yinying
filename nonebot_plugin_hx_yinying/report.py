from io import BytesIO
import traceback,requests,zipfile,sys,os
from PIL import Image,ImageFilter
from .chat import(
    file_get,
    path_in,
    create_dir_usr,
)
from nonebot import get_plugin_config,require
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic
from loguru import logger
from tqdm import tqdm
from nonebot.message import run_postprocessor
from nonebot.adapters.onebot.v11 import (
   Bot,  MessageEvent ,MessageSegment
)
from .config import Config
file = path_in()
def get_file():
    url = "https://skin.huanxinbot.com/api/lzy.php?url=https://wwp.lanzoup.com/i1TJF1wvd6aj&type=down"
    file_get = requests.get(url=url,stream=True)
    total = int(file_get.headers.get('Content-Length',0))
    with open(f"{file}/error.zip","wb") as f,tqdm(desc="error.zip",total=total,unit="iB",unit_scale=True,unit_divisor=1024,) as bar: 
        for data in file_get.iter_content(chunk_size=1024): 
            size = f.write(data)
            bar.update(len(data))
    if os.path.exists(f"{file}/error.zip"):
        logger.success("[Hx]尝试下载补全文件成功")
        with zipfile.ZipFile(f"{file}/error.zip", 'r') as zip_ref:
            zip_ref.extractall(f"{file}/file")
            logger.success("[Hx]尝试补全成功")
            logger.success("已加载错误报告模块")
        os.remove(f"{file}/error.zip")
    else:
        logger.error("尝试下载失败！")

if os.path.exists(f"{file}/file/error_report/hx_error.html"):
    logger.success("已加载错误报告模块")
else:
    logger.error("未找到错误报告模块的文件，尝试下载。。。")
    get_file()

##由星佑的oops修改而来
image_dir = str(f"{file}/error_report")
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
async def crash_oops(err_values:Exception):
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
    template_path = str(f"{file}/file/error_report")
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