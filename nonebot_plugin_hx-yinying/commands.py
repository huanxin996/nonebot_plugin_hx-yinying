from nonebot.log import logger
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters import Event
from nonebot_plugin_userinfo import EventUserInfo, UserInfo
from nonebot_plugin_alconna import on_alconna,Alconna, Args, Option,Arparma,Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage,MsgTarget
from .utils import *

chat = on_message(rule=to_me(),priority=15, block=True)

# 基础命令
chat_cmd = on_alconna(
    Alconna(
        "yinying",
        Args["content?", str],
        Option("help", help_text="显示帮助信息", alias=["帮助", "指令"]),
        Option("text", Args["content", str], help_text="直接对话内容"),
    ),
    block=True
)

# 配置项指令
config_cmd = on_alconna(
    Alconna(
        "yinying.config",
        Option("help", help_text="显示设置帮助"),
        # 基础配置
        Option("global", 
            Args.key[str] + Args.value[str],  # 修改这里，使用加号连接两个参数
            help_text="全局配置设置"
        ),
        # 管理员功能
        Subcommand(
            "admin",
            Subcommand(
                "blacklist",
                Option("add", Args["user_id", str], help_text="添加用户到黑名单"),
                Option("remove", Args["user_id", str], help_text="从黑名单移除用户"),
                Option("list", help_text="查看黑名单列表"),
                help_text="黑名单管理"
            ),
            Subcommand(
                "banword",
                Option("add", Args["word", str], help_text="添加违禁词"),
                Option("remove", Args["word", str], help_text="移除违禁词"),
                Option("list", help_text="查看违禁词列表"),
                help_text="违禁词管理"
            ),
            help_text="管理员功能"
        )
    ),
    block=True
)

# 处理模型命令
model_cmd = on_alconna(
    Alconna(
        "yinying.model",
        Option("help", help_text="显示模型帮助"),
        Option("list", help_text="显示模型列表"),
        Option("switch", Args["name", str], help_text="切换模型")
    ),
    block=True
)

# 处理角色命令
char_cmd = on_alconna(
    Alconna(
        "yinying.char",
        Option("help", help_text="显示角色帮助"),
        Option("add", Args["name", str], help_text="添加角色设定"),
        Option("subscribe", help_text="订阅角色")
    ),
    block=True
)

@chat.handle()
async def handle_chat_message(event:Event,target: MsgTarget,user_info: UserInfo = EventUserInfo()):
    user_id = user_info.user_id
    session_id = event.get_session_id()
    message = event.get_plaintext()
    await send_message(target, f"正在处理...{message}")

@chat_cmd.handle()
async def handle_chat(arp: Arparma, target: MsgTarget, 
                     user_info: UserInfo = EventUserInfo()):
    """处理基础对话"""
    # 处理帮助指令
    if arp.find("help"):
        await show_help(target)
        return
        
    # 处理直接对话内容
    if content := arp.main_args.get("content"):
        await send_message(target, content)
        return
            
    # 处理 text 
    if text_opt := arp.options.get("text"):
        if content := text_opt.args.get("content"):
            await send_message(target, content)
            return

@config_cmd.handle()
async def handle_config(arp: Arparma, target: MsgTarget,
                       user_info: UserInfo = EventUserInfo()):
    """处理配置命令"""
    # 显示帮助
    if arp.find("help"):
        await show_config_help(target)
        return
    
    # 全局配置
    elif options := arp.options.get("global"):
        key = options.args.get("key")
        value = options.args.get("value")
        if key and value:
            # TODO: 实现配置保存逻辑
            await UniMessage.text(f"[配置] 已设置 {key} = {value}").send(target)
            return
        else:
            await UniMessage.text("[错误] 配置参数不完整").send(target)
            return
        
    # 赛博设置
    elif options := arp.options.get("cyber"):
        mode = options.args.get("mode")
        if mode:
            await UniMessage.text(f"[赛博] 已切换模式: {mode}").send(target)
            return
        await UniMessage.text("[错误] 请指定赛博模式").send(target)
        return
        
    # 管理员功能
    elif admin := arp.subcommands.get("admin"):
        # 权限检查
        if not await check_admin_permission(user_info):
            await UniMessage.text("[错误] 需要管理员权限").send(target)
            return

        # 黑名单管理
        if blacklist := admin.subcommands.get("blacklist"):
            if add_opt := blacklist.options.get("add"):
                user_id = add_opt.args.get("user_id")
                await handle_blacklist(target, "add", user_id)
            elif remove_opt := blacklist.options.get("remove"):
                user_id = remove_opt.args.get("user_id")
                await handle_blacklist(target, "remove", user_id)
            elif list_opt := blacklist.options.get("list"):
                await handle_blacklist(target, "list")
            return

        # 违禁词管理
        elif banword := admin.subcommands.get("banword"):
            if add_opt := banword.options.get("add"):
                word = add_opt.value["word"]
                await handle_banword(target, "add", word)
            elif remove_opt := banword.options.get("remove"):
                word = remove_opt.args.get["word"]
                await handle_banword(target, "remove", word)
            elif list_opt := banword.options.get("list"):
                await handle_banword(target, "list")
            return