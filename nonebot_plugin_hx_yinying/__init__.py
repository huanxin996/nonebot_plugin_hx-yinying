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
import json,datetime,os
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
model_list = on_command("模型列表", aliases={"modellist","chat模型列表"}, priority=0, block=True)
model_handoff = on_command("切换模型", aliases={"qhmodel","切换chat模型"}, priority=0, block=True)
rule_reply = on_command("对话回复", aliases={"chat回复"}, priority=0, block=True)
ces = on_command("ces", aliases={"ces"}, priority=0, block=True)

@msg_at.handle()
async def at(matcher: Matcher, event: MessageEvent, bot: Bot, events:Event):
    if isinstance(events, GroupMessageEvent):
        await get_answer_at(matcher, event, bot)
    else:
        await get_answer_at(matcher, event, bot)

@msg_ml.handle()
async def ml(matcher: Matcher, event: MessageEvent, bot: Bot, events:Event, msg: Message = CommandArg()):
    if isinstance(events, GroupMessageEvent):
        await get_answer_ml(matcher, event, bot ,msg)
    else:
        await get_answer_ml(matcher, event, bot ,msg)

@clear.handle()
async def clear(matcher: Matcher, event: MessageEvent):
    id = get_id(event)
    if clear_id(id):
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
    else:
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
async def handoff(matcher: Matcher, bot: Bot, event: MessageEvent,events: Event, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    if not text == "" or text == None:
        if text == "开启" or text == "on" or text == "开":
            if global_config["reply"] == True:
                msg = "请勿重复开启对话回复哦"
                await send_msg(matcher,event,msg)
            else:
                global_config = config_in_global()
                global_config["reply"] == True
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(global_config,file)
                    msg = "对话回复已开启"
                    await send_msg(matcher,event,msg)
        elif text == "关闭" or text == "off" or text == "关":
            if global_config["reply"] == False:
                msg = "请勿重复开启对话回复哦"
                await send_msg(matcher,event,msg)
            else:
                global_config = config_in_global()
                global_config["reply"] == False
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(global_config,file)
                    msg = "对话回复已关闭"
                    await send_msg(matcher,event,msg)
    else:
        msg = "请注意，正确的格式应该是\n对话回复开启"
        await send_msg(matcher,event,msg)

