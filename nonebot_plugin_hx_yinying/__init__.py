from nonebot.plugin import PluginMetadata
from .config import Config
from pip._internal import main
from nonebot import on_command, on_message ,on_startswith ,get_plugin_config
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    Message,
    PrivateMessageEvent,
    Event,
)
from nonebot.log import default_filter, logger, logger_id, sys
from nonebot.matcher import Matcher
from nonebot.rule import to_me
import json,datetime,os,sys
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent, GroupMessageEvent
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
)

hx_config = get_plugin_config(Config)
log_dir = path_in()
   
new_verision = update_hx()
if new_verision <= hx_config.hx_version:
    logger.success("你的Hx_YinYing已经是最新版本了！")
else:
    logger.success("检查到Hx_YinYing有新版本！")
    logger.warning("【Hx】正在自动更新中")
    os.system(f'pip install nonebot-plugin-hx-yinying=={new_verision}')
    logger.success(f"[Hx_YinYing]更新完成！当前版本为{new_verision}")

if hx_config.yinying_appid == None or hx_config.yinying_token == None:
    logger.opt(colors=True).effor("未设置核心配置？！,请检查你配置里的yinying_appid和yinying_token")
    sys.exit()
else:
    logger.opt(colors=True).success("【Hx】加载核心配置成功")

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

msg_at = on_message(rule=to_me(), priority=0, block=True)
msg_ml = on_command("hx", aliases={"chat"}, priority=0, block=True)
clear =  on_command("刷新对话", aliases={"clear"}, priority=0, block=True)
history_get = on_command("导出对话", aliases={"getchat"}, priority=0, block=True)
set_get_global = on_command("导出全局设置", aliases={"getset_global"}, priority=0, block=True)
model_list = on_command("模型列表", aliases={"modellist","chat模型列表"}, priority=0, block=True)
model_handoff = on_command("切换模型", aliases={"qhmodel","切换chat模型"}, priority=0, block=True)
rule_reply = on_command("对话回复", aliases={"chat回复"}, priority=0, block=True)
rule_reply_at = on_command("回复艾特", aliases={"chat回复艾特"}, priority=0, block=True)
private = on_command("私聊回复", aliases={"私聊chat"}, priority=0, block=True)
ces = on_command("ces", aliases={"ces"}, priority=0, block=True)

@msg_at.handle()
async def at(matcher: Matcher, event: MessageEvent, bot: Bot, events:Event):
    if isinstance(events, GroupMessageEvent):
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
            if user_config["use_model"] == model:
                msg =f"(当前模型已经是{model}了)不需要重复切换哦"
                await send_msg(matcher,event,msg)
            else:
                user_config['private_model'] = f"{model}"
                config_user[f"{id}"] = user_config
                with open(f'{log_dir}/config/config_group.json','w',encoding='utf-8') as file:
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
async def get_config(bot:Bot,events: Event):
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