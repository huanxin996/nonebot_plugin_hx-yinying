from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot import on_command, on_message ,on_startswith ,get_plugin_config
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.log import default_filter, logger, logger_id, sys
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent, GroupMessageEvent
from .chat import (
    gen_chat_text,
    get_id,
    get_answer_at,
    get_answer_ml,
    send_msg,
    clear_id,
    user_in,
)
import json,datetime
hx_config = get_plugin_config(Config)

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

@msg_at.handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot):
    await get_answer_at(matcher, event, bot)

@msg_ml.handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot, msg: Message = CommandArg()):
    await get_answer_ml(matcher, event, bot ,msg)

@clear.handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot):
    id = get_id(event)
    if clear_id(id):
        msg = "已刷新对话！"
        await send_msg(matcher, event, msg)
    else:
        msg = "刷新对话失败，请检查后台输出或联系开发者！"
        await send_msg(matcher, event, msg)
