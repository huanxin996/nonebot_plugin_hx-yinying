from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot import on_command, on_message ,get_plugin_config
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    Message,
    Event,
)
from html import unescape
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.rule import to_me
import json,os
from .chat import (
    get_id,
    get_answer_at,
    get_answer_ml,
    get_nick,
    send_msg,
    clear_id,
    get_history,
    config_in_group,
    config_in_user,
    config_in_global,
    model_got,
    get_groupid,
    json_get,
    path_in,
    update_hx,
    get_config_global,
    send_msg_reject,
    easycyber_in,
    json_replace,
)

__plugin_meta__ = PluginMetadata(
    name="Hx_YinYing",
    description="快来和可爱的赛博狼狼聊天！",
    usage=(
        "通过QQ艾特机器人来进行对话"
    ),
    type="application",
    homepage="https://github.com/huanxin996/nonebot_plugin_hx-yinying",
    config=Config,
    supported_adapters={
        "~onebot.v11"
    },
)


hx_config = get_plugin_config(Config)
log_dir = path_in()
   
new_verision = update_hx()
if new_verision <= hx_config.hx_version:
    logger.success(f"你的Hx_YinYing已经是最新版本了！当前版本为{hx_config.hx_version}")
else:
    logger.success("检查到Hx_YinYing有新版本！")
    logger.warning("【Hx】正在自动更新中")
    os.system(f'pip install nonebot-plugin-hx-yinying=={new_verision} -i https://pypi.Python.org/simple/')
    logger.success(f"[Hx_YinYing]更新完成！最新版本为{new_verision}")
    logger.warning(f"[Hx_YinYing]:你可能需要重新启动nonebot来完成插件的重载")

if hx_config.yinying_appid == None or hx_config.yinying_token == None:
    logger.opt(colors=True).error("未设置核心配置？！,请检查你配置里的yinying_appid和yinying_token")
else:
    logger.opt(colors=True).success("【Hx】加载核心配置成功")



msg_at = on_message(rule=to_me(), priority=10, block=True)
msg_ml = on_command("hx", aliases={"chat"}, priority=10, block=True)
clear =  on_command("刷新对话", aliases={"clear"}, priority=0, block=True)
history_get = on_command("导出对话", aliases={"getchat"}, priority=0, block=True)
set_get_global = on_command("导出全局设置", aliases={"getset_global"}, priority=0, block=True)
model_list = on_command("模型列表", aliases={"modellist","chat模型列表"}, priority=0, block=True)
model_handoff = on_command("切换模型", aliases={"qhmodel","切换chat模型"}, priority=0, block=True)
rule_reply = on_command("对话回复", aliases={"chat回复"}, priority=0, block=True)
rule_reply_at = on_command("回复艾特", aliases={"chat回复艾特"}, priority=0, block=True)
private = on_command("私聊回复", aliases={"私聊chat"}, priority=0, block=True)
at_reply = on_command("艾特回复", aliases={"bot艾特回复"}, priority=0, block=True)
easycyber_set = on_command("easycyber", aliases={"easycyber设置"}, priority=0, block=True)

@msg_at.handle()
async def at(matcher: Matcher, event: MessageEvent, bot: Bot, events:Event):
    config_global = config_in_global()
    at_reply = json_get(config_global,"at_reply")
    if not at_reply:
        logger.opt(colors=True).warning("由于艾特回复被设置为false，此条消息忽略")
    elif isinstance(events, GroupMessageEvent):
        await get_answer_at(matcher, event, bot)
    elif json_get(config_in_global(),"private"):
        await get_answer_at(matcher, event, bot)

@msg_ml.handle()
async def ml(matcher: Matcher, event: MessageEvent, bot: Bot, events:Event, msg: Message = CommandArg()):
    if isinstance(events, GroupMessageEvent):
        await get_answer_ml(matcher, event, bot ,msg)
    elif json_get(config_in_global(),"private"):
        await get_answer_ml(matcher, event, bot ,msg)

@clear.handle()
async def clear(matcher: Matcher,bot:Bot, event: MessageEvent):
    id = get_id(event)
    nick = await get_nick(bot,event)
    if clear_id(id,nick):
        msg = "已刷新对话！"
        await send_msg(matcher, event, msg)
    else:
        msg = "刷新对话失败，请检查后台输出或联系开发者！"
        await send_msg(matcher, event, msg)

@history_get.handle()
async def history(bot: Bot, event: MessageEvent,events: Event):
    id = get_id(events)
    msg_list = await get_history(id,bot,event)
    if isinstance(events, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore
    elif json_get(config_in_global(),"private"):
        await bot.send_private_forward_msg(user_id=id, messages=msg_list)  # type: ignore

@model_list.handle()
async def list(matcher: Matcher, event: MessageEvent):
        msg = "1.yinyingllm-v1\n2.yinyingllm-v2\n3.yinyingllm-v3\n4.cyberfurry-001\n5.easycyberfurry-001\n切换模型请发送:模型切换(序号)"
        await send_msg(matcher, event, msg)

@model_handoff.handle()
async def handoff(matcher: Matcher, bot: Bot, event: MessageEvent,events: Event, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    model = model_got(text)
    if not text == "" or text == None:
        if isinstance(events, GroupMessageEvent):
            groupid = get_groupid(event)
            config_group = config_in_group(groupid)
            group_config = json_get(config_group,groupid)
            if group_config["use_model"] == model:
                msg =f"(当前模型已经是{model}了)不需要重复切换哦"
                await send_msg(matcher,event,msg)
            else:
                group_config["use_model"] = model
                config_group[f"{groupid}"] = group_config
                with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
                    json.dump(config_group,file)
                    msg =f"切换成功（当前模型已切换为{model})"
                    await send_msg(matcher,event,msg)
        else:
            id = get_id(event)
            nick = get_nick(bot,event)
            config_user = config_in_user(id,nick)
            user_config = json_get(config_user,id)
            if user_config["private_model"] == model:
                msg =f"(当前模型已经是{model}了)不需要重复切换哦"
                await send_msg(matcher,event,msg)
            else:
                user_config['private_model'] = f"{model}"
                config_user[f"{id}"] = user_config
                with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                    json.dump(config_user,file)
                    msg =f"切换成功（当前模型已切换为{model})"
                    await send_msg(matcher,event,msg)
    else:
        msg = "请注意，切换模型后不能为空哦"
        await send_msg(matcher,event,msg)

@rule_reply.handle()
async def reply(matcher: Matcher, bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        if text == "开启" or text == "on" or text == "开":
            config_global = config_in_global()
            zt_reply = json_get(config_global,"reply")
            if zt_reply == True:
                msg = "请勿重复开启对话回复哦"
                await send_msg(matcher,event,msg)
            else:
                config_global["reply"] = True
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file) 
                msg = "对话回复已开启"
                await send_msg(matcher,event,msg)
        elif text == "关闭" or text == "off" or text == "关":
            config_global = config_in_global()
            zt_reply = json_get(config_global,"reply")
            if zt_reply == False:
                msg = "请勿重复关闭对话回复哦"
                await send_msg(matcher,event,msg)
            else:
                config_global["reply"] = False
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file)
                msg = "对话回复已关闭"
                await send_msg(matcher,event,msg)
    else:
        msg = f"请注意，正确的格式应该是\n对话回复{text}"
        await send_msg(matcher,event,msg)

@rule_reply_at.handle()
async def reply_at(matcher: Matcher, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        if json_get(config_in_global(),"reply") == False:
            if text == "开启" or text == "on" or text == "开":
                config_global = config_in_global()
                zt_reply = json_get(config_global,"reply_at")
                if zt_reply == True:
                    msg = "请勿重复开启回复艾特哦"
                    await send_msg(matcher,event,msg)
                else:
                    config_global["reply_at"] = True
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config_global,file) 
                    msg = "回复艾特已开启"
                    await send_msg(matcher,event,msg)
            elif text == "关闭" or text == "off" or text == "关":
                config_global = config_in_global()
                zt_reply = json_get(config_global,"reply_at")
                if zt_reply == False:
                    msg = "请勿重复关闭对话回复哦"
                    await send_msg(matcher,event,msg)
                else:
                    config_global["reply_at"] = False
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config_global,file)
                    msg = "回复艾特已关闭"
                    await send_msg(matcher,event,msg)
        else:
            msg = "在对话回复开启的状况下（,回复艾特无效"
            await send_msg(matcher,event,msg)
    else:
        msg = f"请注意，正确的格式应该是\n回复艾特{text}"
        await send_msg(matcher,event,msg)

@set_get_global.handle()
async def get_config(bot:Bot, event: MessageEvent,events: Event):
    id = get_id(events)
    msg_list = await get_config_global()
    if isinstance(events, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore
    elif json_get(config_in_global(),"private"):
        await bot.send_private_forward_msg(user_id=id, messages=msg_list)  # type: ignore

@private.handle()
async def reply(matcher: Matcher, bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        if text == "开启" or text == "on" or text == "开":
            config_global = config_in_global()
            zt_reply = json_get(config_global,"private")
            if zt_reply == True:
                msg = "请勿重复开启私聊回复哦"
                await send_msg(matcher,event,msg)
            else:
                config_global["private"] = True
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file) 
                msg = "私聊回复已启用"
                await send_msg(matcher,event,msg)
        elif text == "关闭" or text == "off" or text == "关":
            config_global = config_in_global()
            zt_reply = json_get(config_global,"private")
            if zt_reply == False:
                msg = "请勿重复关闭私聊回复哦"
                await send_msg(matcher,event,msg)
            else:
                config_global["private"] = False
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file)
                msg = "私聊回复已停用"
                await send_msg(matcher,event,msg)
    else:
        msg = f"请注意，正确的格式应该是\n私聊回复{text}"
        await send_msg(matcher,event,msg)

@at_reply.handle()
async def reply(matcher: Matcher, bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        if text == "开启" or text == "on" or text == "开":
            config_global = config_in_global()
            at_reply = json_get(config_global,"at_reply")
            if not at_reply:
                config_global["at_reply"] = True
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file) 
                msg = "艾特回复已启用【bot被@将会回复】"
                await send_msg(matcher,event,msg)
            elif at_reply == True:
                msg = "请勿重复开启艾特回复哦【bot被@已经会回复了】"
                await send_msg(matcher,event,msg)
            else:
                config_global["at_reply"] = True
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file) 
                msg = "艾特回复已启用【bot被@将会回复】"
                await send_msg(matcher,event,msg)
        elif text == "关闭" or text == "off" or text == "关":
            config_global = config_in_global()
            at_reply = json_get(config_global,"at_reply")
            if not at_reply:
                config_global["at_reply"] = False
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file)
                msg = "艾特回复已停用【bot被@回复已停用】"
                await send_msg(matcher,event,msg)
            elif at_reply == False:
                msg = "请勿重复关闭艾特回复哦【bot被@已经不会回复了】"
                await send_msg(matcher,event,msg)
            else:
                config_global["at_reply"] = False
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(config_global,file) 
                msg = "艾特回复已停用【bot被@回复已停用】"
                await send_msg(matcher,event,msg)
    else:
        msg = f"请注意，正确的格式应该是\n私聊回复{text}"
        await send_msg(matcher,event,msg)

@easycyber_set.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n增加 #新增自定义预设(不允许同名)\n载入 #载入自定义预设(不允许不存在)\n查看列表 #列出所有公开的自定义预设\n发送非预期命令则退出",
)
async def _(matcher: Matcher,event: MessageEvent, s: T_State):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    easycyber_package = {}
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "增加":
            if text == "Hx" or text == "HX" or text == "幻歆":
                s["last"] = ""
                msg = "easycyber预设“Hx”不能删除或修改，如要改动请改源码"
                await send_msg_reject(matcher,event,msg)
            s["cfnickname"] = text
            s["last"] = "cfSpecies"
            msg = "请输入角色物种"
            await send_msg_reject(matcher,event,msg)
        if s["last"] == "cfSpecies":
            s["cfSpecies"] = text
            s["last"] = "cfconage"
            msg = "请输入角色表现:(比如\n child--[幼年]\n young--[青年]\n adult--[成年]\nps:只输入--前面的英文即可"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfconage":
            s["cfconage"] = text
            s["last"] = "cfconstyle"
            msg = "请输入角色聊天风格:(比如\n vivid--[活泼]\n sentiment--[富有情感(共情大师？)]\n assistant--[助理]\n chilly--[冷酷无情]\n social_anxiety--[社恐]\nps:只输入--前面的英文即可"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfconstyle":
            s["cfconstyle"] = json_replace(text)
            s["last"] = "cfstory"
            msg = "请输入角色的背景故事（这对他真的很重要\n[胡言乱语：我要给他完整的一生！！！]"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfstory":
            easycyber_package["cfNickname"] = s["cfnickname"]
            easycyber_package["cfSpecies"] = s["cfSpecies"]
            easycyber_package["cfConAge"] = s["cfconage"]
            easycyber_package["cfConStyle"] = s["cfconstyle"]
            easycyber_package["cfStory"] = f"{text}"
            s["last"] = ""
            cybernick = s["cfnickname"]
            easycyber_in(cybernick,easycyber_package)
            msg = "添加成功！，当前此预设仅能供自己私聊使用(问就是权限还没写好)]"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "载入":
            s["last"] = ""
            config_user = config_in_user(id,False)
            user = json_get(config_user,f"{id}")
            promte = json_get(easycyber_in(False,False),f"{text}")
            public = json_get(promte,"public")
            if not public:
               msg = f"{text}模型拒绝被加载"      
            else:
                if user["character_in"]== text:
                    msg = f"{text}模型已加载，请勿重新加载"  
                else:
                    user["character_in"] = f"{text}"
                    config_user[f"{id}"] = user
                    with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                        json.dump(config_user,file)
                        msg = f"{text}加载成功！" 
            await send_msg_reject(matcher,event,msg)
    # 增加预设
    if text == "增加":
        s["last"] = "增加"
        msg = "请输入角色昵称"
        await send_msg_reject(matcher,event,msg)
    
    if text == "载入":
        s["last"] = "载入"
        msg = "请输入公开的角色昵称【非公开会载入失败！】"
        await send_msg_reject(matcher,event,msg)

    if text == "查看列表":
        s["last"] = ""
        list_in = easycyber_in(False,False)
        list_got = []
        for key in list_in:
            if list_in[f"{key}"]["public"]:
                list_got.append(format(key))
            else:
                return
        msg = f"{list_got}"
        await send_msg_reject(matcher,event,msg)

    # 退出
    msg = f"未知命令“{text}”，已退出"
    await send_msg(matcher,event,msg)
