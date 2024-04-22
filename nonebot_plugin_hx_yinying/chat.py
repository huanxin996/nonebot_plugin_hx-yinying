# -- coding: utf-8 --**
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent ,MessageSegment ,Message
from html import unescape
from typing import List
import os,httpx, json, time, requests
from .config import Config
from nonebot import get_plugin_config, logger, require
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

#判断模型
def model_got(msg) -> str:
    try:
        if msg == "1" or msg == "yinyingllm-v1" or msg == "yinyingllmv1":
            back = "yinyingllm-v1"
        elif msg == "2" or msg == "yinyingllm-v2" or msg == "yinyingllmv2":
            back = "yinyingllm-v2"
        elif msg == "3" or msg == "yinyingllm-v3" or msg == "yinyingllmv3":
            back = "yinyingllm-v3"
        elif msg == "4" or msg == "cyberfurry-001" or msg == "cyberfurry001" or msg == "cyberfurry1":
            back = "cyberfurry-001"
        elif msg == "5" or msg == "easycyberfurry-001" or msg == "easycyberfurry001" or msg == "easycyberfurry1":
            back = "easycyberfurry-001"
    except Exception as e:
        return f"{e}"
    return back

#path---in
def path_in() -> str:
    if hx_config.hx_path == None:
        history_dir = store.get_data_dir("Hx_YingYing")
        log_dir = Path(f"{history_dir}\yinying_chat").absolute()
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    else:
        history_dir = store.get_data_dir(f"{hx_config.hx_path}")
        log_dir = Path(f"{history_dir}\yinying_chat").absolute()
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir


#update-----Hx
def update_hx() -> str:
    fails = 0
    while True:
        try:
            if fails >= 20:
                break
            headers = {'content-type': 'application/json'}
            ret = requests.get(url="https://pypi.org/pypi/nonebot-plugin-hx-yinying/json", headers=headers ,timeout=10)
            if ret.status_code == 200:
                json = ret.json()
                verision = json["info"]["version"]
            else:
                continue
        except:
            fails += 1
            logger.warning("网络状况不佳，检查最新版本失败，正在重新尝试")
        else:
            break
    return verision

#获取用户id
def get_id(event) -> int:
    """获取会话id"""
    if isinstance(event, GroupMessageEvent):
            id = f"{event.user_id}"
    else:
        id = f"{event.user_id}"
    return id

#获取群聊id
def get_groupid(event) -> int:
    """获取群聊id"""
    if isinstance(event, GroupMessageEvent):
            groupid = f"{event.group_id}"
    else:
        groupid = None
    return groupid

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


#结果消息函数，发送消息直接await就行
async def send_msg_reject(matcher, event, content):
    config_global = config_in_global()
    reply_config = json_get(config_global,"reply")
    if reply_config == True:
        await matcher.reject(MessageSegment.reply(event.message_id) + content)
    else:
        reply_at = json_get(config_global,"reply_at")
        await matcher.reject(content, at_sender=reply_at)


#创建用户文件夹
def create_dir_usr(path):
    if not os.path.exists(path):
        os.mkdir(path)

#json转义防止爆炸（）
def json_replace(text) -> str:
    text = text.replace('\n','\\n')
    text = text.replace('\t','\\t')
    text = text.replace("'","\\'")
    text = text.replace('"','\\"')
    return text

#初始化log记录
def log_in()-> str:
    try:
        if os.path.exists(f"{log_dir}/chat/all_log.json"):
            with open(f'{log_dir}/chat/all_log.json','r',encoding='utf-8') as file:
                json_data = json.load(file)
                back = json_data
        else:
            create_dir_usr(f'{log_dir}/chat')
            with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
                json_data = {}
                package = {}
                history_package = []
                package['rule'] = '幻歆'
                package['msg'] = '初始化log记录'
                history_package.append(package)
                json_data['114514'] = history_package
                json.dump(json_data,file)
                back = json_data
    except Exception as e:
                create_dir_usr(f'{log_dir}/chat')
                logger.warning("加载全局log记录时失败！，请不要随意修改bot插件本地文件")
                with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
                    json_data = {}
                    package = {}
                    history_package = []
                    package['rule'] = '幻歆'
                    package['msg'] = '初始化log记录'
                    history_package.append(package)
                    json_data['114514'] = history_package
                    json.dump(json_data,file)
                    back = json_data
    return back

#用户输入
def user_in(id, text):
    data = log_in()
    if f'{id}' in data: 
        id_log = data[f'{id}']['log']
        package = {}
        package['rule'] = 'user'
        text_r = json_replace(text)
        package['msg'] = f'{text_r}'
        id_log.append(package)
        data[f'{id}']['log'] = id_log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
    else : 
        package = {}
        log = {}
        history_package = []
        package['rule'] = 'user'
        text_r = json_replace(text)
        package['msg'] = f'{text_r}'
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
        text_r = json_replace(text)
        package['msg'] = f'{text_r}'
        id_log.append(package)
        data[f'{id}']['log'] = id_log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
    else : 
        package = {}
        log = {}
        history_package = []
        package['rule'] = 'ai'
        text_r = json_replace(text)
        package['msg'] = f'{text_r}'
        history_package.append(package)
        log['log'] = history_package
        dt = time.time()
        t = int(dt)
        log['time'] = t
        data[f'{id}'] = log
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)

#载入本地保存的easycyber预设(一些情况下失败时不会清空，请找到专业人员修复)
def easycyber_in(cybernick,json_1) -> str:
    try:
        if os.path.exists(f"{log_dir}/config/easycyber.json"):
            with open(f'{log_dir}/config/easycyber.json','r',encoding='utf-8') as file:
                json_data = json.load(file)
                if cybernick in json_data or not json_1 or not cybernick:
                    back = json_data
                else:
                    dt = time.time()
                    t = int(dt)
                    dw = int(len(json_data) + 1)
                    package_easycyberfurry = json_1
                    package_easycyberfurry["create_time"] = t
                    package_easycyberfurry["last_update"] = t
                    package_easycyberfurry["public"] = False
                    package_easycyberfurry["id"] = dw
                    json_data[f"{cybernick}"] = package_easycyberfurry
                    with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                        json.dump(json_data,file)
                    back = json_data
        else:
            create_dir_usr(f"{log_dir}/config")
            with open(f'{log_dir}/config/easycyber.json','w',encoding='utf-8') as file:
                dt = time.time()
                t = int(dt)
                global_easycyberfurry = {}
                package_easycyberfurry = {}
                package_easycyberfurry["cfNickname"] = "Hx"
                package_easycyberfurry["cfSpecies"] = "龙狼"
                package_easycyberfurry["cfConAge"] = "child"
                package_easycyberfurry["cfConStyle"] = "sentiment"
                package_easycyberfurry["cfStory"] = "相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。"
                package_easycyberfurry["create_by"] = 3485462167
                package_easycyberfurry["create_time"] = t
                package_easycyberfurry["last_update"] = t
                package_easycyberfurry["public"] = True
                package_easycyberfurry["id"] = 0
                global_easycyberfurry["Hx"] = package_easycyberfurry
                packages_easycyberfurry = json_1
                packages_easycyberfurry["create_time"] = t
                packages_easycyberfurry["last_update"] = t
                packages_easycyberfurry["public"] = True
                packages_easycyberfurry["id"] = 1
                global_easycyberfurry[f"{cybernick}"] = packages_easycyberfurry
                json.dump(global_easycyberfurry,file)
                back = global_easycyberfurry
    except Exception as e:
            logger.error(f"加载本地cyberfurry预设时失败！，请不要随意修改bot插件本地文件。。。。！")
            logger.warning("你要为你的行为负责，来自不知名开发者")
            logger.warning(f"报错捕获{e}")
            back = False
    return back

#载入全局本地配置
def config_in_global() -> str:
    try:
        if os.path.exists(f"{log_dir}/config/config_global.json"):
            with open(f'{log_dir}/config/config_global.json','r',encoding='utf-8') as file:
                json_data = json.load(file)
                back = json_data
        else:
            create_dir_usr(f"{log_dir}/config")
            with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                json_data = {}
                global_cyberfurry = {}
                global_easycyberfurry = {}
                black_user = []
                black_group = []
                black_world = []
                package_cyberfurry = {}
                package_easycyberfurry = {}
                Xml = []
                package_cyberfurry["systemPrompt"] = "你的名字叫Hx,与幻歆的幻梦破碎之歆中诞生"
                package_cyberfurry["xml"] = Xml
                package_cyberfurry["create_by"] = 3485462167
                package_cyberfurry["create_time"] = 1713710000
                package_cyberfurry["last_update"] = 1713710923
                package_cyberfurry["public"] = True
                package_cyberfurry["id"] = 0
                global_cyberfurry["Hx"] = package_cyberfurry
                package_easycyberfurry["cfNickname"] = "Hx"
                package_easycyberfurry["cfSpecies"] = "龙狼"
                package_easycyberfurry["cfConAge"] = "child"
                package_easycyberfurry["cfConStyle"] = "sentiment"
                package_easycyberfurry["cfNickname"] = "相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。"
                package_easycyberfurry["create_by"] = 3485462167
                package_easycyberfurry["create_time"] = 1713710000
                package_easycyberfurry["last_update"] = 1713710923
                package_easycyberfurry["public"] = True
                package_easycyberfurry["id"] = 0
                global_easycyberfurry["Hx"] = package_easycyberfurry
                json_data['global_switch'] = True
                json_data['limit'] = 12
                json_data['at_reply'] = True
                json_data['reply'] = False
                json_data['reply_at'] = False
                json_data['private'] = True
                json_data['blacklist_user'] = black_user
                json_data['blacklist_group'] = black_group
                json_data['blacklist_world'] = black_world
                json_data['cyberfurry'] = global_cyberfurry
                json_data['easycyberfurry'] = global_easycyberfurry
                json.dump(json_data,file)
                back = json_data
    except Exception as e:
            create_dir_usr(f"{log_dir}/config")
            logger.error(f"加载全局配置时失败！，请不要随意修改bot插件本地文件,现已重置所有群聊配置")
            logger.warning("你要为你的行为负责，来自不知名开发者")
            logger.warning(f"报错捕获{e}")
            with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                json_data = {}
                global_cyberfurry = {}
                global_easycyberfurry = {}
                black_user = []
                black_group = []
                black_world = []
                package_cyberfurry = {}
                package_easycyberfurry = {}
                Xml = []
                package_cyberfurry["systemPrompt"] = "你的名字叫Hx,与幻歆的幻梦破碎之歆中诞生"
                package_cyberfurry["xml"] = Xml
                package_cyberfurry["create_by"] = 3485462167
                package_cyberfurry["create_time"] = 1713710000
                package_cyberfurry["last_update"] = 1713710923
                package_cyberfurry["public"] = True
                package_cyberfurry["id"] = 0
                global_cyberfurry["Hx"] = package_cyberfurry
                package_easycyberfurry["cfNickname"] = "Hx"
                package_easycyberfurry["cfSpecies"] = "龙狼"
                package_easycyberfurry["cfConAge"] = "child"
                package_easycyberfurry["cfConStyle"] = "sentiment"
                package_easycyberfurry["cfNickname"] = "相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。"
                package_easycyberfurry["create_by"] = 3485462167
                package_easycyberfurry["create_time"] = 1713710000
                package_easycyberfurry["last_update"] = 1713710923
                package_easycyberfurry["public"] = True
                package_easycyberfurry["id"] = 0
                global_easycyberfurry["Hx"] = package_easycyberfurry
                json_data['global_switch'] = True
                json_data['limit'] = 12
                json_data['reply'] = False
                json_data['reply_at'] = False
                json_data['private'] = True
                json_data['blacklist_user'] = black_user
                json_data['blacklist_group'] = black_group
                json_data['blacklist_world'] = black_world
                json_data['cyberfurry'] = global_cyberfurry
                json_data['easycyberfurry'] = global_easycyberfurry
                json.dump(json_data,file)
                back = json_data
    return back

#载入群聊本地配置
def config_in_group(groupid) -> str:
    try:
        if os.path.exists(f"{log_dir}/config/config_group.json"):
            with open(f'{log_dir}/config/config_group.json','r',encoding='utf-8') as file:
                json_data = json.load(file)
                if groupid in json_data:
                    back = json_data
                else:
                    dt = time.time()
                    t = int(dt)
                    id_package = {}
                    id_package['use_model'] = "yinyingllm-v2"
                    id_package['chat_alltimes'] = 0
                    id_package['first_chattime'] = t
                    id_package['last_chattime'] = t
                    json_data[f"{groupid}"] = id_package
                    with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
                        json.dump(json_data,file)
                        back = json_data
        else:
            create_dir_usr(f"{log_dir}/config")
            with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
                dt = time.time()
                t = int(dt)
                json_data = {}
                id_package = {}
                id_package['use_model'] = "yinyingllm-v2"
                id_package['chat_alltimes'] = 0
                id_package['first_chattime'] = t
                id_package['last_chattime'] = t
                json_data[f"{groupid}"] = id_package
                json.dump(json_data,file)
                back = json_data
    except Exception as e:
            logger.error(f"加载群聊{groupid}配置时失败！，请不要随意修改bot插件本地文件,现已重置所有群聊配置")
            logger.warning("你要为你的行为负责，来自不知名开发者")
            logger.warning(f"报错捕获{e}")
            with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
                dt = time.time()
                t = int(dt)
                json_data = {}
                id_package = {}
                id_package['use_model'] = "yinyingllm-v2"
                id_package['chat_alltimes'] = 0
                id_package['first_chattime'] = t
                id_package['last_chattime'] = t
                json_data[f"{groupid}"] = id_package
                json.dump(json_data,file)
                back = json_data
    return back

#载入个人本地配置
def config_in_user(id,nick) -> str:
    try:
        if os.path.exists(f"{log_dir}/config/config_user.json"):
            with open(f'{log_dir}/config/config_user.json','r',encoding='utf-8') as file:
                json_data = json.load(file)
                if id in json_data or not nick:
                    back = json_data
                else:
                    dt = time.time()
                    t = int(dt)
                    id_package = {}
                    id_package['character'] = f"我是{nick}，是一只可爱的毛毛龙嗷呜"
                    id_package['character_in'] = True
                    id_package['private_model'] = "yinyingllm-v2"
                    id_package['chat_alltimes'] = 0
                    id_package['times'] = 1
                    id_package['time'] = 1713710000
                    id_package['first_chattime'] = t
                    id_package['last_chattime'] = t
                    json_data[f"{id}"] = id_package
                    with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                        json.dump(json_data,file)
                        back = json_data
        else:
            create_dir_usr(f"{log_dir}/config")
            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                dt = time.time()
                t = int(dt)
                json_data = {}
                id_package = {}
                id_package['character'] = f"我是{nick}，是一只可爱的毛毛龙嗷呜"
                id_package['character_in'] = True
                id_package['private_model'] = "yinyingllm-v2"
                id_package['chat_alltimes'] = 0
                id_package['times'] = 1
                id_package['time'] = 1713710000
                id_package['first_chattime'] = t
                id_package['last_chattime'] = t
                json_data[f"{id}"] = id_package
                json.dump(json_data,file)
                back = json_data
    except Exception as e:
            logger.error(f"加载用户{id}配置时失败！，请不要随意修改bot插件本地文件,现已重置所有用户配置")
            logger.warning("你要为你的行为负责，来自不知名开发者")
            logger.warning(f"报错捕获{e}")
            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                dt = time.time()
                t = int(dt)
                json_data = {}
                id_package = {}
                id_package['character'] = f"我是{nick}，是一只可爱的毛毛龙嗷呜"
                id_package['character_in'] = True
                id_package['private_model'] = "yinyingllm-v2"
                id_package['chat_alltimes'] = 0
                id_package['times'] = 1
                id_package['time'] = 1713710000
                id_package['first_chattime'] = t
                id_package['last_chattime'] = t
                json_data[f"{id}"] = id_package
                json.dump(json_data,file)
                back = json_data
    return back

#尝试获取bot本地文件夹文件
def file_get(file) -> str:
    try:
        if os.path.exists(f"{log_dir}/file/{file}"):
            back = True
        else:
            back = False
    except Exception as e:
        back = False
    return back

#历史消息卡片构建
async def get_history(id,bot,event) -> List[MessageSegment]:
    date = log_in()
    log_list = date[f"{id}"]["log"]
    t = len(log_list)/2
    nick = await get_nick(bot,event)
    msg_list = []
    try:
        for item in log_list:
            text = item["msg"]
            if item["rule"]=="user":
                msg_list.append(
                MessageSegment.node_custom(
                user_id=id,
                nickname="呜呜一号",
                content=Message(f"(来源)[user]\n{text}"),
                ))
            else:
                msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"(来源)[bot]\n{text}"),                    
                ))
        msg_list.insert(
            0,
                MessageSegment.node_custom(
                    user_id=3485462167,
                    nickname="AAA星佑批发（幻歆限定）",
                    content=Message(f"(来源)[{nick}*hx限定][{id}]\n\n共查找到{t}条历史对话记录"),
                ),)
    except Exception as e:
        msg_list = [
            MessageSegment.node_custom(
                user_id=3485462167,
                nickname="AAA星佑批发（幻歆限定）",
                content=Message("合并消息时出错！"),
            )
        ]
    return msg_list

#全局配置卡片构建
async def get_config_global() -> List[MessageSegment]:
    config = config_in_global()
    msg_list = []
    try:
        reply = config["reply"]
        reply_at = config["reply_at"]
        global_switch = config["global_switch"]
        private = config["private"]
        limit = config["limit"]
        at_reply = config["at_reply"]
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"全局开启状态:{global_switch}"),                    
                ))
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"bot被艾特或回复是否回应:{at_reply}"),                    
                ))
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"对话回复开启状态:{reply}"),                    
                ))
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"回复艾特开启状态:{reply_at}\n请注意：该配置项和对话回复冲突，当对话回复开启时，该配置项无效！"),                    
                ))
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"是否启用私聊？:{private}"),                    
                ))
        msg_list.append(
                MessageSegment.node_custom(
                user_id=3202123263,
                nickname="AAA星佑批发（Hx限定）",
                content=Message(f"对话次数上限:{limit}"),                    
                ))
        msg_list.insert(
            0,
                MessageSegment.node_custom(
                    user_id=3485462167,
                    nickname="AAA星佑批发（幻歆限定）",
                    content=Message("【重要】以下为bot全局配置"),
                ),)
    except Exception as e:
        msg_list = [
            MessageSegment.node_custom(
                user_id=3485462167,
                nickname="AAA星佑批发（幻歆限定）",
                content=Message("获取全局配置合并消息时出错！"),
            )
        ]
    return msg_list

#检测对话次数
def chat_times(id,nick) -> int:
    data = log_in()
    history = data[f"{id}"]['log']
    times = int(len(history)/2 + 0.5)
    limit = json_get(config_in_global(),"limit")
    config = config_in_user(id,nick)
    if times >= limit:
        dt = time.time()
        t = int(dt)
        data[f'{id}']['time'] = t
        data[f"{id}"]['log'] = []
        config[f"{id}"]["time"] = t
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as user:
                json.dump(config,user)
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

#获取json函数
def json_get(json,key) -> str:
    try:
        back = json[f"{key}"]
    except Exception as e:
        back = False
    return back

#手动刷新对话
def clear_id(id,nick) -> str:
    data = log_in()
    dt = time.time()
    t = int(dt)
    data[f'{id}']['time'] = t
    data[f'{id}']['log'] = []
    config = config_in_user(id,nick)
    config[f"{id}"]["time"] = t
    try:
        with open(f'{log_dir}/chat/all_log.json','w',encoding='utf-8') as file:
            json.dump(data,file)
            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as user:
                json.dump(config,user)
                zt = True
    except Exception as e:
            zt = False
    return zt

#初始化传参（整理data）
def data_in(groupid,id,text,nick) -> str:
    """构建data"""
    data = {}
    packages_data = json.loads(json.dumps(data))
    allvariables = {}
    packages_data['appId'] = f'{hx_config.yinying_appid}'
    user_config = config_in_user(id,nick)
    group_config = config_in_group(groupid)
    id_config = json_get(user_config,id)
    group_config = json_get(group_config,groupid)
    character = json_get(id_config,"character")
    time = json_get(id_config,"time")
    model_group = json_get(group_config,"use_model")
    try:
        if not model_group or groupid == None:
            model = json_get(id_config,"private_model")
            if model == None or model == "yinyingllm-v2":
                logger.warning("找不到配置里的yinying_model或你设置的模型为yinyingllm-v2,将使用默认模型llm2")
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v2'
                packages_data['model'] = 'yinyingllm-v2'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif model == "yinyingllm-v1":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v1'
                packages_data['message'] = f'{text}'
            elif model == "yinyingllm-v3":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v3'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif model == "cyberfurry-001":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-cyberfurry-001'
                packages_data['model'] = 'cyberfurry-001'
                packages_data['systemPrompt'] = "你的名字叫Hx"
                packages_data['message'] = f'{text}'
            elif model == "easycyberfurry-001":
                if json_get(id_config,"character_in") == True or not json_get(id_config,"character_in"):
                    logger.warning("okokok1")
                    packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-easycyberfurry-001'
                    packages_data['model'] = 'easycyberfurry-001'
                    characterSet = {}
                    package = {}
                    package['nickName'] = f'{nick}'
                    package['furryCharacter'] = f'{character}'
                    allvariables.update(package)
                    new_package = {}
                    new_package['cfNickname'] = 'Hx'
                    new_package['cfSpecies'] = '龙狼'
                    new_package['cfConAge'] = 'child'
                    new_package['cfConStyle'] = 'social_anxiety'
                    new_package['cfStory'] = '你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。'
                    characterSet.update(new_package)
                    packages_data['variables'] = allvariables
                    packages_data['characterSet'] = characterSet
                    packages_data['message'] = f'{text}'
                else:
                    logger.warning("okokok2")
                    promte_model = json_get(id_config,"character_in")
                    promte = json_get(easycyber_in(promte_model,False),f"{promte_model}")
                    if not promte:
                        packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-easycyberfurry-001'
                        packages_data['model'] = 'easycyberfurry-001'
                        characterSet = {}
                        package = {}
                        package['nickName'] = f'{nick}'
                        package['furryCharacter'] = f'{character}'
                        allvariables.update(package)
                        new_package = {}
                        new_package['cfNickname'] = 'Hx'
                        new_package['cfSpecies'] = '龙狼'
                        new_package['cfConAge'] = 'child'
                        new_package['cfConStyle'] = 'social_anxiety'
                        new_package['cfStory'] = '你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。'
                        characterSet.update(new_package)
                        packages_data['variables'] = allvariables
                        packages_data['characterSet'] = characterSet
                        packages_data['message'] = f'{text}'
                    else:
                        logger.warning("okokok3")
                        packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-easycyberfurry-001'
                        packages_data['model'] = 'easycyberfurry-001'
                        package = {}
                        package['nickName'] = f'{nick}'
                        package['furryCharacter'] = f'{character}'
                        allvariables.update(package)
                        new_package = {}
                        new_package['cfNickname'] = f"{promte['cfNickname']}"
                        new_package['cfSpecies'] = f"{promte['cfSpecies']}"
                        new_package['cfConAge'] = f"{promte['cfConAge']}"
                        new_package['cfConStyle'] = f"{promte['cfConStyle']}"
                        new_package['cfStory'] = f"{promte['cfStory']}"
                        characterSet.update(new_package)
                        packages_data['variables'] = allvariables
                        packages_data['characterSet'] = characterSet
                        packages_data['message'] = f'{text}'
            else:
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v2'
                package = {}
                package['nick'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
        else:
            logger.warning(f"{model_group}")
            model = model_group
            if model == None or model == "yinyingllm-v2":
                logger.warning("找不到配置里的yinying_model或你设置的模型为yinyingllm-v2,将使用默认模型llm2")
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v2'
                packages_data['model'] = 'yinyingllm-v2'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif model == "yinyingllm-v1":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v1'
                packages_data['message'] = f'{text}'
            elif model == "yinyingllm-v3":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-yinyingllm-v3'
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                packages_data['variables'] = allvariables
                packages_data['message'] = f'{text}'
            elif model == "cyberfurry-001":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-cyberfurry-001'
                packages_data['model'] = 'cyberfurry-001'
                packages_data['systemPrompt'] = "你的名字叫Hx"
                packages_data['message'] = f'{text}'
            elif model == "easycyberfurry-001":
                packages_data['chatId'] = f'{hx_config.yinying_appid}-{id}-{time}-easycyberfurry-001'
                packages_data['model'] = 'easycyberfurry-001'
                characterSet = {}
                package = {}
                package['nickName'] = f'{nick}'
                package['furryCharacter'] = f'{character}'
                allvariables.update(package)
                new_package = {}
                new_package['cfNickname'] = 'Hx'
                new_package['cfSpecies'] = '龙狼'
                new_package['cfConAge'] = 'child'
                new_package['cfConStyle'] = 'social_anxiety'
                new_package['cfStory'] = '你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。'
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
    config_global = config_in_global()
    reply_config = json_get(config_global,"reply")
    if reply_config == True:
        await matcher.send(MessageSegment.reply(event.message_id) + content)
    else:
        reply_at = json_get(config_global,"reply_at")
        await matcher.send(content, at_sender=reply_at)

#主要构建
async def yinying(groupid,id,text,nick):
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {hx_config.yinying_token}'
    }
    osu = data_in(groupid,id,text,nick)
    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            back = await client.post("https://api-yinying-ng.wingmark.cn/v1/chatWithCyberFurry", headers=headers, json=osu)
    try:
            back = back.json()
    except json.decoder.JSONDecodeError as e:
            back_msg = f"json解析报错！\n返回结果：{e}"
            return back_msg
    try:
        times = chat_times(id,nick)
        limit = json_get(config_in_global(),"limit")
        if times >= limit or times == 0:
            msg = back['choices'][0]['message']['content']
            ai_out(id,json_replace(text))
            back_msg = f"{msg}\n[对话次数达到上限，即将清空缓存.]"
        else:
            msg = back['choices'][0]['message']['content']
            ai_out(id,json_replace(text))
            back_msg = f"{msg}\n[{times}|{limit}]"
    except Exception as e:
        back_msg = f"{back}\n\n{osu}\n\n未知错误，错误定位于#主要构建函数。"
    return back_msg

#获取回复（被艾特）
async def get_answer_at(matcher, event, bot):
    text = unescape(await gen_chat_text(event, bot))
    if  text == "" or text is None or text == "！d" or text == "/！d":
        msg = "诶唔，你叫我是有什么事嘛？"
        await send_msg(matcher,event,msg)
    else:
        try:
            groupid = get_groupid(event)
            id = get_id(event)
            nick = await get_nick(bot,event)
            user_in(id,json_replace(text))
            back_msg = str(await yinying(groupid,id,text,nick))
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
            groupid = get_groupid(event)
            id = get_id(event)
            nick = await get_nick(bot,event)
            user_in(id,json_replace(text))
            back_msg = str(await yinying(groupid,id,text,nick))
            msg = back_msg.replace("\\n","\n")
            await send_msg(matcher,event,msg)
        except httpx.HTTPError as e:
            back_msg = f"请求接口报错！\n返回结果：{e}"
            await send_msg(matcher, event, back_msg)
    else:
        msg = "诶唔，你叫我是有什么事嘛？"
        await send_msg(matcher,event,msg)

