# -- coding: utf-8 --**
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent ,MessageSegment
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.matcher import Matcher
from html import unescape
import os,httpx, json, datetime, time
from .config import Config
from nonebot import get_plugin_config, logger, require
from datetime import datetime
hx_config = get_plugin_config(Config)
from pathlib import Path
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

if hx_config.hx_path == None:
    logger.warning("找不到配置里的路径，将使用默认配置")
    history_dir = store.get_data_dir("Hx_YingYing")
    log_dir = Path(f"{history_dir}\yinying_chat").absolute()
    log_dir.mkdir(parents=True, exist_ok=True)
else:
    logger.success("找到配置里的路径，载入成功")
    history_dir = store.get_data_dir(f"{hx_config.hx_path}")
    log_dir = Path(f"{history_dir}\yinying_chat").absolute()
    log_dir.mkdir(parents=True, exist_ok=True)


#创建用户文件夹
def create_dir_usr(path):
    if not os.path.exists(path):
        os.mkdir(path)

#用户输入
def user_in(id, text):
    if os.path.exists(f"{log_dir}\chat\{id}\content.json"):
        with open(f"{log_dir}\chat\{id}\content.json",'a',encoding='utf-8') as file:
            file.write(',\n{"role": "user", "content": "' + text + '"}')
    else:
        create_dir_usr(f"{log_dir}\chat\{id}")
        with open(f"{log_dir}\chat\{id}\content.json",'w',encoding='utf-8') as file:
            file.write('{"role": "user", "content": "' + text + '"}')

#AI输出
def ai_out(id, text):
    if os.path.exists(f"{log_dir}\chat\{id}\content.json"):
        with open(f'{log_dir}\chat\{id}\content.json','a',encoding='utf-8') as file:
            file.write(',\n{"role": "assistant", "content": "' + text + '"}')
    else:
        create_dir_usr(f"{log_dir}\chat\{id}")
        with open(f'{log_dir}\chat\{id}\content.json','w',encoding='utf-8') as file:
            file.write('{"role": "assistant", "content": "' + text + '"}')

#存储对话次数
def chat_times(id):
    if os.path.exists(f'{log_dir}/chat/{id}/times.json'):
        with open(f"{log_dir}/chat/{id}/times.json",'a',encoding='utf-8') as file:
                with open(f'{log_dir}/chat/{id}/times.json','r',encoding='utf-8') as file:
                    data = json.load(file)
                    data["times"] = data["times"] + 1
                    data.update(file)
                with open(f'{log_dir}/chat/{id}/times.json','w',encoding='utf-8') as file:
                    json.dump(data, file)
    else:
        create_dir_usr(f"{log_dir}\chat\{id}")
        with open(f'{log_dir}/chat/{id}/times.json','w',encoding='utf-8') as file:
                with open(f'{log_dir}/chat/{id}/times.json','w',encoding='utf-8') as file:
                    old_data = {}
                    dt = time.time()
                    t = int(dt)
                    data = {"times":0,"time":t,"character":"是一只猫猫龙哦"}
                    old_data.update(data)
                with open(f'{log_dir}/chat/{id}/times.json','w',encoding='utf-8') as file:
                    json.dump(data, file)
                    return 0



#清楚对话id
def chat_clear(id):
    with open(f"{log_dir}/chat/{id}/times.json",'a',encoding='utf-8') as file:
        with open(f'{log_dir}/chat/{id}/times.json','r',encoding='utf-8') as file:
            data = json.load(file)
            dt = time.time()
            t = int(dt)
            data["times"] = 0
            data["time"] = t
            data.update(file)
        with open(f'{log_dir}/chat/{id}/times.json','w',encoding='utf-8') as file:
            json.dump(data, file)
            return True
     


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

async def get_nick(bot:Bot,event: MessageEvent) -> str:
    """获取昵称"""
    qq = event.user_id
    info = await bot.get_stranger_info(user_id=int(qq))
    nick = info["nickname"]
    if nick is None:
        nick = None
    else:
        nick = nick
    return nick



def data_in(id,text,nick) -> str:
    """构建data"""
    with open(f'{log_dir}/chat/{id}/times.json','r',encoding='utf-8') as user,\
         open(f'{log_dir}/global.json','w',encoding='utf-8') as globa:
        data = {}
        packages_data = json.loads(json.dumps(data))
        allvariables = {}
        u = json.load(user)
        time = u["time"]
        character = u["character"]
        packages_data['appId'] = f'{hx_config.yinying_appid}'
        try:
            if hx_config.yinying_model == None or hx_config.yinying_model == "yinyingllm-v2":
                logger.warning("找不到配置里的yinying_model或你设置的模型为yinyingllm-v2,将使用默认模型llm2")
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v2'
                packages_data['model'] = 'yinyingllm-v2'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif hx_config.yinying_model == "yinyingllm-v1":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v1'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif hx_config.yinying_model == "yinyingllm-v3":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v3'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif hx_config.yinying_model == "cyberfurry-001":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-cyberfurry-001'
                packages_data['model'] = 'cyberfurry-001'
                packages_data['systemPrompt'] = "你的名字叫Hx"
                packages_data['message'] = f'{text}'
            elif hx_config.yinying_model == "easycyberfurry-001":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-easycyberfurry-001'
                packages_data['model'] = 'easycyberfurry-001'
                characterSet = {}
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                new_package = {}
                new_package['cfNickname'] = '幻歆'
                new_package['cfSpecies'] = '龙狼'
                new_package['cfConAge'] = 'child'
                new_package['cfConStyle'] = 'social_anxiety'
                new_package['cfStory'] = '由幻歆创造'
                characterSet.update(new_package)
                packages_data['variables'] = allvariables
                packages_data['characterSet'] = characterSet
                packages_data['message'] = f'{text}'
            else:
                logger.warning("找不到该模型！将使用默认模型llm2")
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v2'
                package = {}
                package['nick'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
        except Exception as e:
                logger.error("严重错误，构建data失败！")
                json_data = False
        return packages_data

            




async def send_msg(matcher: Matcher, event: MessageEvent, content):
    if hx_config.hx_reply == True:
        await matcher.send(MessageSegment.reply(event.message_id) + content)
    else:
        await matcher.send(content, at_sender=hx_config.hx_reply_at)

async def yinying(id,text,nick):
    chat_times(id)
    with open(f'{log_dir}/chat/{id}/times.json','r',encoding='utf-8') as file:
        data = json.load(file)
        times_yinying = data["times"]
        headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {hx_config.yinying_token}'
    }
        osu = data_in(id,text,nick)
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
                back = await client.post(hx_config.hx_api_yinying, headers=headers, json=osu)
        try:
                back = back.json()
        except json.decoder.JSONDecodeError as e:
                back_msg = f"json解析报错！\n返回结果：{e}"
                return back_msg
        try:
            if times_yinying>=hx_config.yinying_limit:
                msg = back['choices'][0]['message']['content']
                back_msg = f"[对话次数达到上限，即将清空缓存.]\n{msg}"
                user_in(id,text)
                ai_out(id,msg)
                chat_clear(id)
            else:
                msg = back['choices'][0]['message']['content']
                back_msg = f"[{times_yinying}|{hx_config.yinying_limit}]\n{msg}"
                user_in(id,text)
                ai_out(id,msg)
        except Exception as e:
                back_msg = f"{back} \n\n\n{osu}"
        return back_msg
    


async def get_answer(matcher: Matcher, event: MessageEvent, bot: Bot):
    text = unescape(await gen_chat_text(event, bot))
    id = get_id(event)
    nick = await get_nick(bot,event)
    if  text == "" or text is None or text == "/hx" or text == "/chat":
        msg = "诶唔，你叫我是有什么事嘛？"
        await send_msg(matcher,event,msg)
    else:
        try:
            back_msg = str(await yinying(id,text,nick))
            msg = back_msg.replace("\\n","\n")
            await send_msg(matcher,event,msg)
        except httpx.HTTPError as e:
            back_msg = f"请求接口报错！\n返回结果：{e}"
            await send_msg(matcher, back_msg)
