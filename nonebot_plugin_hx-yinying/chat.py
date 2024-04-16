# -- coding: utf-8 --**
__author__ = "HuanXin"
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.matcher import Matcher
from html import unescape
import os,httpx, json, datetime
from .config import Config
from nonebot import get_plugin_config, logger
from datetime import datetime
hx_config = get_plugin_config(Config)
from pathlib import Path
import nonebot_plugin_localstore as store

logger.warning("找不到路径，将使用默认配置")
history_dir = store.get_data_dir("Hx_YingYing")
log_dir = Path(f"{history_dir}\yinying_chat\chat").absolute()
log_dir.mkdir(parents=True, exist_ok=True)

#创建用户文件夹
def create_dir_usr(path):
    if not os.path.exists(path):
        os.mkdir(path)

#用户输入
def user_in(id, text):
    if os.path.exists(f"{log_dir}\{id}\content.json"):
        with open(f"{log_dir}\{id}\content.json",'a',encoding='utf-8') as file:
            file.write(',\n{"role": "user", "content": "' + text + '"}')
    else:
        create_dir_usr(f"{log_dir}\{id}")
        with open(f"{log_dir}\{id}\content.json",'w',encoding='utf-8') as file:
            file.write('{"role": "user", "content": "' + text + '"}')

#AI输出
def ai_out(id, text):
    if os.path.exists(f"{log_dir}\{id}\content.json"):
        with open(f'{log_dir}\{id}\content.json','a',encoding='utf-8') as file:
            file.write(',\n{"role": "assistant", "content": "' + text + '"}')
    else:
        create_dir_usr(f"{log_dir}\{id}")
        with open(f'{log_dir}\{id}\content.json','w',encoding='utf-8') as file:
            file.write('{"role": "assistant", "content": "' + text + '"}')



async def gen_chat_text(event: MessageEvent, bot: Bot) -> str:
    msg = ""
    for seg in event.message:
        if seg.is_text():
            msg += seg.data.get("text", "")

        elif seg.type == "at":
            qq = seg.data.get("qq", None)

            if qq:
                if qq == "all":
                    msg += "@全体成员"
                else:
                    user_info = await bot.get_group_member_info(
                        group_id=event.group_id,
                        user_id=event.user_id,
                        no_cache=False,
                    )
                    user_name = user_info.get("card", None) or user_info.get(
                        "nickname", None
                    )
                    if user_name:
                        msg
    return msg


def get_id(event: MessageEvent) -> str:
    """获取会话id"""
    if isinstance(event, GroupMessageEvent):
            id = f"{event.user_id}"
    else:
        id = f"{event.user_id}"
    return id

async def send_with_at(matcher: Matcher, content):
    await matcher.send(content, at_sender=hx_config.hx_reply_at)


async def finish_with_at(matcher: Matcher, content):
    await matcher.finish(content, at_sender=hx_config.hx_reply_at)

async def furrbar(text):
    data = {"model": f"{hx_config.furbar_model}",
            "messages": [{"role": "system","content": "你是一只龙"},
                         {"role":"user","content":text}]
            }
    json_data = json.dumps(data)
    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
        res = await client.post(hx_config.hx_api_furbar, json=data)
        res = res.json()
    try:
        res_raw = res['choices'][0]['message']['content']
    except Exception as e:
        res_raw = res
    return res_raw


async def yinying(text,id):
    user_in(id,text)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {hx_config.yinying_token}'
    }
    data = {
                'appId':'huanxinbot',
                'chatId':'huanxinbot-3485462167-ces',
                'model':f'{hx_config.yinying_model}',
                'variables':{'nickName': '幻歆','furryCharacter': '一只猫猫龙'},
                'message':f'{text}'
                }
    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            back = await client.post(hx_config.hx_api_yinying, headers=headers, json=data)
    try:
            back = back.json()
    except json.decoder.JSONDecodeError as e:
            back_msg = f"请求接口报错！\n返回结果：{e}"
            return back_msg
    try:
        back_msg = back['choices'][0]['message']['content']
    except Exception as e:
        back_msg = back
    return back_msg
    


async def get_answer(matcher: Matcher, event: MessageEvent, bot: Bot):
    text = unescape(await gen_chat_text(event, bot))
    id = get_id(event)
    try:
        back_msg = str(await yinying(text,id))
        msg = back_msg.replace("\n","\\n")
        ai_out(id,msg)
        await send_with_at(matcher,msg)
    except httpx.HTTPError as e:
        back_msg = f"请求接口报错！\n返回结果：{e}"
        await finish_with_at(matcher, back_msg)





