from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot import on_command, on_message ,on_startswith ,get_plugin_config
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.log import default_filter, logger, logger_id, sys
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent, GroupMessageEvent
from .chat import (
    gen_chat_text,
    get_id,
    send_with_at,
    finish_with_at,
    get_answer,
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
    homepage="https://github.com/huanxin996/Hx_bot",
    config=Config,
    supported_adapters=None,
)




msg = on_message(rule=to_me(), priority=0, block=True)
none = talk_keyword = on_startswith("h1x")

@none.handle()
@msg.handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot):
    await get_answer(matcher, event, bot)

