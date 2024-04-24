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
    json_get_text,
    easycyber_in_tg,
    place,
    config_list,
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
   
new_verision, time = update_hx()
if new_verision <= hx_config.hx_version:
    logger.success(f"[Hx_YinYing]:你的Hx_YinYing已经是最新版本了！当前版本为{hx_config.hx_version}")
else:
    logger.success("[Hx_YinYing]:检查到Hx_YinYing有新版本！")
    logger.warning("【Hx】正在自动更新中")
    os.system(f'pip install nonebot-plugin-hx-yinying=={new_verision} -i https://pypi.Python.org/simple/')
    logger.success(f"[Hx_YinYing]:更新完成！最新版本为{new_verision}|当前使用版本为{hx_config.hx_version}")
    logger.warning(f"[Hx_YinYing]:你可能需要重新启动nonebot来完成插件的重载")

if hx_config.yinying_appid == None or hx_config.yinying_token == None:
    logger.opt(colors=True).error("未设置核心配置？！,请检查你配置里的yinying_appid和yinying_token")
else:
    logger.opt(colors=True).success("【Hx】加载核心配置成功")



msg_at = on_message(rule=to_me(), priority=10, block=True)
msg_ml = on_command("hx", aliases={"chat"}, priority=10, block=True)
clear =  on_command("刷新对话", aliases={"clear"}, priority=0, block=True)
history_get = on_command("导出对话", aliases={"getchat"}, priority=0, block=True)
set_global_config = on_command("设置全局配置", aliases={"设置配置全局","globalset"}, priority=0, block=True)
set_get_global = on_command("导出全局设置", aliases={"getset_global"}, priority=0, block=True)
model_list = on_command("模型列表", aliases={"modellist","chat模型列表"}, priority=0, block=True)
model_handoff = on_command("切换模型", aliases={"qhmodel","切换chat模型"}, priority=0, block=True)
rule_reply = on_command("对话回复", aliases={"chat回复"}, priority=0, block=True)
rule_reply_at = on_command("回复艾特", aliases={"chat回复艾特"}, priority=0, block=True)
private = on_command("私聊回复", aliases={"私聊chat"}, priority=0, block=True)
at_reply = on_command("艾特回复", aliases={"bot艾特回复"}, priority=0, block=True)
easycyber_set = on_command("easycyber", aliases={"easycyber设置","hxworld"}, priority=0, block=True)
admin_set = on_command("控制台操作", aliases={"管理控制台","setstart"}, priority=0, block=True)
verision = on_command("确认版本", aliases={"旅行伙伴确认","版本确认"}, priority=0, block=True)
character = on_command("sd", aliases={"旅行伙伴加入","设定加入"}, priority=0, block=True)

@character.handle()
async def verision_get(matcher: Matcher,bot:Bot, event: MessageEvent, events:Event, msg: Message = CommandArg()):
    user = get_id(event)
    nick = await get_nick(bot,event)
    config = config_in_user(user,nick)
    config_get = json_get(config,user)
    text = msg.extract_plain_text()
    if text == "" or text == None:
        msg = "没有获取到要加入伙伴的设定哦"
        await send_msg(matcher, event, msg)
    else:
        try:
            msg = text.split(" ")
            if int(len(msg)) == 1:
                config_get["nick"] = nick
                config_get["character"] = text
                config[f"{user}"] = config_get
                with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                    json.dump(config,file)
                    msg = f"{nick}加入成功"
            elif int(len(msg)) == 2:
                config_get["nick"] = msg[1]
                config_get["character"] = msg[0]
                config[f"{user}"] = config_get
                with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                    json.dump(config,file)
                    msg = f"{msg[0]}加入成功！"
            else:
                msg = "没有获取到要加入伙伴的设定哦"
            await send_msg(matcher, event, msg)
        except Exception as e:
            msg = False
            logger.opt(colors=True).error(f"{e}")
        
@verision.handle()
async def verision_get(matcher: Matcher, event: MessageEvent, events:Event):
    new_verision, time = update_hx()
    if isinstance(events, GroupMessageEvent):
        config = json_get(config_in_group(get_groupid(event)),get_groupid(event))
        model = json_get(config,"use_model")
        if new_verision > hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in or not model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        else:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in or not model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:\n最后更新时间:====>\n{time}\n======================"
        await send_msg(matcher, event, msg)
    else:
        config = json_get(config_in_user(get_id(event),False),get_id(event))
        model = json_get(config,"private_model")
        if new_verision > hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in or not model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        else:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in or not model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:\n最后更新时间:====>\n{time}\n======================"
        await send_msg(matcher, event, msg)

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

@set_global_config.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n修改 #修改全局配置项\n查看 #查看全局配置项\n追加 #向全局配置里追加配置项，通常用于插件更新后配置不存在导致的出错\n查看所有配置 #列出所有全局配置\n发送非预期命令则退出",
)
async def set_global(matcher: Matcher, bot:Bot, event: MessageEvent,events: Event, s: T_State):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "查看":
            config = config_in_global()
            get_config = json_get_text(config,text)
            if get_config == 0:
                s["last"] = True
                msg = f"无法查找到该配置项！，请检查其是否为正确的配置名{text}"
                await send_msg(matcher,event,msg)
            else:
                s["last"] = True
                msg = f"{text}状态为:{get_config}"
                await send_msg(matcher,event,msg)

        if s["last"] == "修改":
            config = config_in_global()
            get_config = json_get_text(config,text)
            if get_config == 0:
                s["last"] = True
                msg = "无法查找到该配置项！，请检查其是否为正确的配置名"
                await send_msg(matcher,event,msg)
            else:
                TFkey, Wkey, Listkey, app_key = config_list(config)
                if text in TFkey:
                    s["last"] = "修改TF"
                    s["set"] = text
                    msg = "请发送开启或关闭【也可以是on或者off或者开和关】"
                    await send_msg_reject(matcher,event,msg)
                elif text in Wkey:
                    s["last"] = "修改w"
                    s["set"] = text
                    msg = "请发送id（群号或者QQ号，看你改哪个配置项）"
                    await send_msg_reject(matcher,event,msg)
                elif text in Listkey:
                    s["last"] = "updata_LK"
                    s["set"] = text
                    msg = "请发送添加或删除【也可以是增加或者移除】"
                    await send_msg_reject(matcher,event,msg)
                else:
                    return
        
        if s["last"] == "修改TF":
            config = config_in_global()
            config_name = s["set"]
            get_config = json_get_text(config,config_name)
            if text == "on" or text == "开" or text == True:
                text = True
            elif text == "off" or text == "关" or text == False:
                text = False
                if get_config and text:
                    msg = f"该配置项[{config_name}]已经开启了，不需要重复开启噢"
                elif not get_config and not text:
                    msg = f"该配置项[{config_name}]已经关闭了，不需要重复关闭噢"
                elif text:
                    config[f"{config_name}"] = True
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config,file)
                    msg = f"{config_name}的状态已更改为{text}"
                elif not text:
                    config[f"{config_name}"] = False
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config,file)
                    msg = f"{config_name}的状态已更改为{text}"
            s["last"] = True
            if text == "退出":
                msg = "已退出"
            await send_msg(matcher,event,msg)        
        
        if s["last"] == "修改w":
            config = config_in_global()
            config_name = s["set"]
            get_config = json_get_text(config,config_name)
            config[f"{config_name}"] = text
            with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                json.dump(config,file)
            msg = f"{config_name}的id已更改为{text}"
            s["last"] = True
            await send_msg(matcher,event,msg)

        if s["last"] == "updata_LK":
            s["type"] = text
            if text == "增加" or text == "添加":
                s["last"] = "修改LKt"
                msg = "请发送要添加的id(存在时会失败！)"
            elif text == "移除" or text == "删除":
                s["last"] = "修改LKt"
                msg = "请发送要删除的id(不存在时会失败！)"
            else:
                s["last"] = True
                msg = "未知方式"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "修改LKt":
            config_name = s["set"]
            config_set_type = s["type"]
            s["last"] = True
            config = config_in_global()
            config_get = json_get(config,config_name)
            if config_set_type == "增加" or config_set_type == "添加":
                if text in config_get:
                    msg = "该id已经在这个配置项里了，不可以重复添加哦"
                else:
                    config_get.append(text)
                    config["config_name"] = config_get
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config,file)
                        msg = "该id已添加在这个配置项里"
            elif config_set_type == "移除" or config_set_type == "删除":
                if text not in config_get:
                    msg = "该id不在这个配置项里，无法重复删除"
                else:
                    config_get.remove(text)
                    config["config_name"] = config_get
                    with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                        json.dump(config,file)
                        msg = "该id已在这个配置项里被移除"
            await send_msg(matcher,event,msg) 
        
        
    #查看
    if text == "查看" or text == "查看配置":
        s["last"] = "查看"
        msg = "请输入配置项(具体名称)\n【ps:如果不知道建议先查看所有配置一下,[]内为具体名称】"
        await send_msg_reject(matcher,event,msg)
    
    if text == "修改" or text == "修改配置":
        s["last"] = "修改"
        msg = "请输入配置项(具体名称)\n【ps:如果不知道建议先查看所有配置一下,[]内为具体名称】"
        await send_msg_reject(matcher,event,msg)

    if text == "追加" or text == "追加配置":
        s["last"] = True
        msg = "在写了在写了😭"
        await send_msg(matcher,event,msg)

    if text == "查看所有配置":
        msg_list = await get_config_global()
        s["last"] = True
        if isinstance(events, GroupMessageEvent):
            await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)
        else:
            await bot.send_private_forward_msg(user_id=id, messages=msg_list)

    # 退出
    if s["last"]:
        return
    else:
        msg = f"未知命令“{text}”，已退出"
        await send_msg(matcher,event,msg)

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
    prompt=f"发送以下选项执行相应功能\n投稿 #投稿自定义预设(不允许同名)\n载入 #载入自定义预设(不允许不存在)\n查看列表 #列出所有公开的自定义预设\n退出 #退出设置\n发送非预期命令则退出",
)
async def _(matcher: Matcher, bot:Bot, event: MessageEvent, s: T_State,events: Event):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    easycyber_package = {}
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "增加":
            if text == "Hx" or text == "HX" or text == "幻歆":
                s["last"] = True
                msg = "easycyber预设“Hx”不能删除或修改，如要改动请改源码"
                await send_msg(matcher,event,msg)
            else:
                s["cfnickname"] = text
                s["last"] = "cfSpecies"
                msg = "请输入角色物种"
                await send_msg_reject(matcher,event,msg)
        if s["last"] == "cfSpecies":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            else:
                s["cfSpecies"] = text
                s["last"] = "cfconage"
                msg = "请输入角色表现:(比如\n child--[幼年]\n young--[青年]\n adult--[成年]\nps:只输入--前面的英文即可"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfconage":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            key = ['child','young','adult']
            if not text in key:
                s["last"] = True
                msg = "未找到该类型的角色表现！已自动退出"
                await send_msg(matcher,event,msg)
            else:
                s["cfconage"] = text
                s["last"] = "cfconstyle"
                msg = "请输入角色聊天风格:(比如\n vivid--[活泼]\n sentiment--[富有情感(共情大师？)]\n assistant--[助理]\n chilly--[冷酷无情]\n social_anxiety--[社恐]\nps:只输入--前面的英文即可"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfconstyle":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            key = ['vivid','sentiment','assistant','chilly','social_anxiety']
            if not text in key:
                s["last"] = True
                msg = "未找到该类型的角色聊天风格！已自动退出"
                await send_msg(matcher,event,msg)
            else:
                s["cfconstyle"] = json_replace(text)
                s["last"] = "cfstory"
                msg = "请输入角色的背景故事（这对他真的很重要\n[胡言乱语：我要给他完整的一生！！！]"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfstory":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            else:
                s["cfstory"] = text
                s["last"] = "public"
                msg = "该角色是否公开？(最后一步)完成将发送到bot管理站进行审核，审核通过后即可使用"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "public":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            else:
                name = s["cfnickname"]
                species = s["cfSpecies"]
                age = s["cfconage"]
                stytle = s["cfconstyle"]
                story = s["cfstory"]
                easycyber_package["cfNickname"] = s["cfnickname"]
                easycyber_package["cfSpecies"] = s["cfSpecies"]
                easycyber_package["cfConAge"] = s["cfconage"]
                easycyber_package["cfConStyle"] = s["cfconstyle"]
                easycyber_package["cfStory"] = s["cfstory"]
                easycyber_package["public"] = text
                easycyber_package["creator"] = id
                s["last"] = True
                cybernick = s["cfnickname"]
                g = json_get(config_in_global(),"admin_group")
                u = json_get(config_in_global(),"admin_pro")
                g_k = json_get(config_in_global(),"admin_group_switch")
                u_k = json_get(config_in_global(),"admin_user_switch")
                if not g and u:
                    logger.opt(colors=True).success(f"{g},{u}")
                    msg ="bot管理者未配置，超级管理员和bot控制台,审核失败！"
                elif u == None and g == None:
                    logger.opt(colors=True).success("false")
                    msg ="bot管理者未配置，超级管理员和bot控制台,审核失败！"
                elif u == None and g_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    groupid = json_get(config_in_global(),"admin_group")
                    msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\n物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                    await bot.call_api("send_group_msg",group_id=groupid, message=msg_tg)
                    msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                elif g == None and u_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    adminid = json_get(config_in_global(),"admin_pro")
                    msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                    await bot.call_api("send_private_msg",user_id=adminid, messages=msg_tg)
                    msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                elif u_k and g_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    groupid = json_get(config_in_global(),"admin_group")
                    adminid = json_get(config_in_global(),"admin_pro")
                    msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                    await bot.call_api("send_group_msg",group_id=groupid, message=msg_tg)
                    await bot.call_api("send_private_msg",user_id=adminid, messages=msg_tg)
                    msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                elif g_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    adminid = json_get(config_in_global(),"admin_pro")
                    msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                    await bot.call_api("send_private_msg",user_id=adminid, messages=msg_tg)
                else:
                    easycyber_in_tg(cybernick,easycyber_package)
                    groupid = json_get(config_in_global(),"admin_group")
                    msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\n物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                    await bot.call_api("send_group_msg",group_id=groupid, message=msg_tg)
                    msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                await send_msg(matcher,event,msg)


        if s["last"] == "载入":
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            else:
                s["last"] = True
                if isinstance(events, GroupMessageEvent):
                    groupid = get_groupid(event)
                    config = config_in_group(groupid)
                    config_group = json_get(config,groupid)
                    promte = json_get(easycyber_in(False,False),f"{text}")
                    public = json_get(promte,"public")
                    if not public:
                        msg = f"{text}模型拒绝被加载(可能是模型不存在或者模型非公开！)"      
                    else:
                        if config_group["character_in"] == text:
                            msg = f"{text}模型已加载，请勿重新加载"  
                        else:
                            config_group["character_in"] = f"{text}"
                            config[f"{groupid}"] = config_group
                            with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
                                json.dump(config,file)
                                msg = f"{text}加载成功！" 
                else:
                    config_user = config_in_user(id,False)
                    user = json_get(config_user,f"{id}")
                    promte = json_get(easycyber_in(False,False),f"{text}")
                    public = json_get(promte,"public")
                    creator = json_get(promte,"creator")
                    if creator == id:
                        if user["character_in"]== text:
                            msg = f"{text}模型已加载，请勿重新加载"  
                        else:
                            user["character_in"] = f"{text}"
                            config_user[f"{id}"] = user
                            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                                json.dump(config_user,file)
                                msg = f"{text}加载成功！"
                    elif not public:
                        msg = f"{text}模型拒绝被加载(可能是模型不存在或者模型非公开！)"      
                    else:
                        if user["character_in"] == text:
                            msg = f"{text}模型已加载，请勿重新加载"  
                        else:
                            user["character_in"] = f"{text}"
                            config_user[f"{id}"] = user
                            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                                json.dump(config_user,file)
                                msg = f"{text}加载成功！" 
                await send_msg(matcher,event,msg)
    # 增加预设
    if text == "投稿":
        s["last"] = "增加"
        msg = "请输入角色昵称"
        await send_msg_reject(matcher,event,msg)
    if text == "载入":
        s["last"] = "载入"
        msg = "请输入公开的角色昵称【非公开会载入失败！】"
        await send_msg_reject(matcher,event,msg)
    if text == "查看列表":
        s["last"] = True
        list_in = easycyber_in(False,False)
        try:
            list_got = []
            for key in list_in:
                if list_in[f"{key}"]["public"]:
                    list_got.append(format(key))
                else:
                    return
            msg = f"{list_got}"
        except Exception as e:
            msg = "当前没有公开的角色哦"
        await send_msg(matcher,event,msg)
    # 退出
    if s["last"]:
        return
    else:
        msg = f"未知命令“{text}”，已退出"
        await send_msg(matcher,event,msg)

@admin_set.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n通过 #通过投稿的自定义预设(不允许同名)\n拒绝 #拒绝投稿的自定义预设(不允许同名)\n查看 #查看投稿预设详情(不允许不存在)\n查看投稿列表 #列出所有投稿的自定义预设\n添加admin #添加bot管理者\n退出 #退出\n仅支持bot管理员使用！\n发送非预期命令则退出",
)
async def _(matcher: Matcher, bot:Bot, event: MessageEvent, s: T_State):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    place_user = place(id)
    if place_user >= 9:
        if "last" not in s:
            s["last"] = ""
        if s["last"]:
            if s["last"] == "通过1":
                json_1 = easycyber_in_tg(False,False)
                json_data = json_get(json_1,text)
                json_data["tg_admin"] = id
                user = json_data["creator"]
                in_ok = easycyber_in(text,json_data)
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/easycyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                    s["last"] = True
                    msg = f"已通过投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

            if s["last"] == "拒绝":
                s["last"] = True
                json_1 = easycyber_in_tg(False,False)
                json_data = json_get(json_1,text)
                user = json_data["creator"]
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/easycyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                    msg = f"已拒绝投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

        if text == "通过":
            s["last"] = "通过1"
            msg = "请输入要加入角色昵称"
            await send_msg_reject(matcher,event,msg)

        if text == "查看投稿列表":
            s["last"] = True
            list_in = easycyber_in_tg(False,False)
            msg_list = []
            for key in list_in:
                msg_list.append(format(key))
            await send_msg(matcher,event,f"{msg_list}")

        if text == "拒绝":
            s["last"] = "拒绝"
            msg = "请输入要离开角色昵称"
            await send_msg_reject(matcher,event,msg)

        if s["last"]:
            return
        else:
            msg = f"未知命令“{text}”，已退出"
            await send_msg(matcher,event,msg)

    else:
        msg = f"你的权限为{place_user},权限不足，无法操作"
        await send_msg(matcher, event, msg)