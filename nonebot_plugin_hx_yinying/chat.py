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

#初始化log记录
def log_in()-> str:
    if os.path.exists(f"{log_dir}/chat/all_log.json"):
        with open(f'{log_dir}/chat/all_log.json','r',encoding='utf-8') as file:
            json_data = json.load(file)
            return json_data
    else:
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json_data = {}
            package = {}
            history_package = []
            package['rule'] = '幻歆'
            package['msg'] = '初始化log记录'
            history_package.append(package)
            json_data['114514'] = history_package
            json.dump(json_data,file)
            return json_data

#创建用户文件夹
def create_dir_usr(path):
    if not os.path.exists(path):
        os.mkdir(path)

#用户输入
def user_in(id, text):
    data = log_in()
    if f'{id}' in data: 
        id_log = data[f'{id}']['log']
        package = {}
        package['rule'] = 'user'
        package['msg'] = f'{text}'
        id_log.append(package)
        data[f'{id}']['log'] = id_log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
    else : 
        package = {}
        log = {}
        history_package = []
        package['rule'] = 'user'
        package['msg'] = f'{text}'
        history_package.append(package)
        log['log'] = history_package
        dt = time.time()
        t = int(dt)
        log['time'] = t
        data[f'{id}'] = log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)

#AI输出
def ai_out(id, text):
    data = log_in()
    if f'{id}' in data: 
        id_log = data[f'{id}']['log']
        package = {}
        package['rule'] = 'ai'
        package['msg'] = f'{text}'
        id_log.append(package)
        data[f'{id}']['log'] = id_log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
    else : 
        package = {}
        log = {}
        history_package = []
        package['rule'] = 'ai'
        package['msg'] = f'{text}'
        history_package.append(package)
        log['log'] = history_package
        dt = time.time()
        t = int(dt)
        log['time'] = t
        data[f'{id}'] = log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)

#检测对话次数
def chat_times(id) -> str:
    data = log_in()
    history = data[f"{id}"]['log']
    times = len(history)/2 +0.5
    if times >= hx_config.yinying_limit:
        dt = time.time()
        t = int(dt)
        data[f'{id}']['time'] = t
        data[f"{id}"]['log'] = []
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
            return 0
    else:
        return times

#获取纯文本
async def gen_chat_text(event, bot: Bot) -> str:
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

#手动刷新对话
def clear_id(id) -> str:
    data = log_in()
    dt = time.time()
    t = int(dt)
    data[f'{id}']['time'] = t
    data[f'{id}']['log'] = []
    try:
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
            zt = True
    except Exception as e:
            zt = False
    return zt

#获取用户id
def get_id(event) -> str:
    """获取会话id"""
    if isinstance(event, GroupMessageEvent):
            id = f"{event.user_id}"
    else:
        id = f"{event.user_id}"
    return id

#获取用户昵称
async def get_nick(bot,event) -> str:
    """获取昵称"""
    qq = event.user_id
    info = await bot.get_stranger_info(user_id=int(qq))
    nick = info["nickname"]
    if nick is None:
        nick = None
    else:
        nick = nick
    return nick

#初始化传参（整理data）
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

#全局发送消息函数，发送消息直接await就行
async def send_msg(matcher, event, content):
    if hx_config.hx_reply == True:
        await matcher.send(MessageSegment.reply(event.message_id) + content)
    else:
        await matcher.send(content, at_sender=hx_config.hx_reply_at)

#主要构建
async def yinying(id,text,nick):
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
        times = chat_times(id)
        if times >= hx_config.yinying_limit or times == 0:
            msg = back['choices'][0]['message']['content']
            text0 = msg.replace("\n","\\n")
            text1 = text0.replace("'","\\'")
            text = text1.replace('"','')
            ai_out(id,text)
            back_msg = f"{msg}\n[对话次数达到上限，即将清空缓存.]"
        else:
            msg = back['choices'][0]['message']['content']
            text0 = msg.replace("\n","\\n")
            text1 = text0.replace("'","\\'")
            text = text1.replace('"','')
            ai_out(id,text)
            back_msg = f"{msg}\n[{times}|{hx_config.yinying_limit}]"
    except Exception as e:
            back_msg = f"{back} \n\n\n{osu}\n\n\n未知错误，错误定位于#主要构建函数。"
    return back_msg

#获取回复（被艾特）
async def get_answer_at(matcher, event, bot):
    text = unescape(await gen_chat_text(event, bot))
    if  text == "" or text is None or text == "/hx" or text == "/chat":
        msg = "诶唔，你叫我是有什么事嘛？"
        await send_msg(matcher,event,msg)
    else:
        try:
            id = get_id(event)
            nick = await get_nick(bot,event)
            user_in(id,text)
            back_msg = str(await yinying(id,text,nick))
            msg = back_msg.replace("\\n","\n")
            await send_msg(matcher,event,msg)
        except httpx.HTTPError as e:
            back_msg = f"请求接口报错！\n返回结果：{e}"
            await send_msg(matcher, event, back_msg)

#获取回复（指令触发）
async def get_answer_ml(matcher, event ,bot ,msg):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        try:
            id = get_id(event)
            nick = await get_nick(bot,event)
            user_in(id,text)
            back_msg = str(await yinying(id,text,nick))
            msg = back_msg.replace("\\n","\n")
            await send_msg(matcher,event,msg)
        except httpx.HTTPError as e:
            back_msg = f"请求接口报错！\n返回结果：{e}"
            await send_msg(matcher, event, back_msg)
    else:
        msg = "诶唔，你叫我是有什么事嘛？"
        await send_msg(matcher,event,msg)

