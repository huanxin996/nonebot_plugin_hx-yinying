import random
from nonebot import get_driver
from nonebot_plugin_userinfo import EventUserInfo, UserInfo
from nonebot_plugin_alconna.uniseg import UniMessage,MsgTarget
from nonebot.adapters import Event
from nonebot.log import logger
from typing import Optional
from ..configs.spconfig import GlobalConfig,UserConfig
from .logs import ChatLogs
from ..api.methods import get_chat_response



def number_suiji():
    """
    随机数生成
    """
    digits = "0123456789"
    str_list =[random.choice(digits) for i in range(3)]
    random_str =''.join(str_list)
    return random_str

def ban_word(text:str) -> str:
    """违禁词剔除函数"""
    config = GlobalConfig.load()
    ban_word_list = config.blacklist_world
    if ban_word_list:
        for word in ban_word_list:
            if word and word in text:
                text = text.replace(word, "w" * len(word))
                
    return text

def get_superuser() -> list:
    """
    获取nonebot超级管理组
    """
    list_superuser = get_driver().config.superusers
    try:
        if list_superuser == None or not list_superuser:
            superuser = ["3485462167"]
        else:
            superuser = get_driver().config.superusers
    except Exception as e:
            logger.warning(f"报错捕获{e}")
            superuser = ["3485462167"]
    return superuser

def get_group_id(event: Event) -> tuple[bool, Optional[str]]:
    """获取群组ID"""
    session_parts = event.get_session_id().split("_")
    if len(session_parts) >= 2:
        if session_parts[0] == "group":
            return True, session_parts[1]
    return False, None


async def send_message(target: MsgTarget, message: str, is_finish: bool = False) -> bool:
    """发送消息"""
    if is_finish:
        await UniMessage.text(message).finish(target)
        return True
    else:
        await UniMessage.text(message).send(target)
        return False

async def show_config_help(target: MsgTarget):
    """显示配置帮助"""
    help_text = """配置管理指令:
    基础配置:
    - yinying.config --global <key> <value>: 设置全局配置
    - yinying.config --cyber <mode>: 设置赛博模式
    - yinying.config --timeline <line>: 切换时间线
    
    管理员功能:
    - yinying.config admin --blacklist <add/remove> <用户ID>
    - yinying.config admin --banword <add/remove> <违禁词>
    - yinying.config admin --test: 测试功能"""
    await send_message(target, help_text)

async def check_permission(event:Event,user_info: UserInfo = EventUserInfo()) -> bool:
    """检查权限"""
    if await check_admin_permission(user_info):
        return True
    else:
        if await check_base_permission(event,user_info):
            return True
        else:
            return False    

async def check_base_permission(event:Event,user_info: UserInfo = EventUserInfo()) -> bool:
    """检查基础权限"""
    config = GlobalConfig.load()
    user_id = str(user_info.user_id)
    is_group,group_id = get_group_id(event)

    # 白名单模式
    if config.rule_model == "white":
        is_white_user = user_id in config.white_user
        is_white_group = group_id and group_id in config.white_group
        return is_white_user or is_white_group
    
    # 黑名单模式
    is_black_user = user_id in config.blacklist_user
    is_black_group = group_id and group_id in config.blacklist_group
    
    # 私聊默认允许,群聊需要检查群权限
    if is_group:
        if not config.private:  # 群聊关闭时拒绝
            return False
        return not (is_black_user or is_black_group)
    else:
        if not config.private:  # 私聊关闭时拒绝
            return False
        return not is_black_user

async def check_admin_permission(user_info: UserInfo = EventUserInfo()) -> bool:
    """检查管理员权限"""
    config = GlobalConfig.load()
    superusers = get_superuser()
    user_id = str(user_info.user_id)
    if user_id in config.admin_user or user_info.user_id in superusers or user_id is config.admin_pro:
        return True
    else:
        return False
    

async def handle_blacklist(target: MsgTarget, action: str, user_id: str):
    """处理黑名单"""
    config = GlobalConfig.load()
    
    if action == "add":
        if config.add_to_list("blacklist_user", user_id):
            await send_message(target, f"[黑名单] 已添加用户: {user_id}")
        else:
            await send_message(target, f"[黑名单] 用户 {user_id} 已在列表中")
            
    elif action == "remove":
        if config.remove_from_list("blacklist_user", user_id):
            await send_message(target, f"[黑名单] 已移除用户: {user_id}")
        else:
            await send_message(target, f"[黑名单] 用户 {user_id} 不在列表中")
            
    elif action == "list":
        users = config.blacklist_user
        if users:
            user_list = "\n".join(f"- {uid}" for uid in users)
            await send_message(target, f"[黑名单] 当前黑名单:\n{user_list}")
        else:
            await send_message(target, "[黑名单] 当前黑名单为空")
            
    else:
        await send_message(target, "[错误] 未知操作,请使用 add/remove/list")

async def handle_banword(target: MsgTarget, action: str, word: str):
    """处理违禁词"""
    config = GlobalConfig.load()
    
    if action == "add":
        if config.add_to_list("blacklist_world", word):
            await send_message(target, f"[违禁词] 已添加: {word}")
        else:
            await send_message(target, f"[违禁词] {word} 已在列表中")
            
    elif action == "remove":
        if config.remove_from_list("blacklist_world", word):
            await send_message(target, f"[违禁词] 已移除: {word}")
        else:
            await send_message(target, f"[违禁词] {word} 不在列表中")
            
    elif action == "list":
        words = config.blacklist_world
        if words:
            word_list = "\n".join(f"- {w}" for w in words)
            await send_message(target, f"[违禁词] 当前违禁词:\n{word_list}")
        else:
            await send_message(target, "[违禁词] 当前无违禁词")
            
    else:
        await send_message(target, "[错误] 未知操作,请使用 add/remove/list")

async def show_help(target: MsgTarget):
    """显示帮助信息"""
    help_text = """小狼聊天助手
    基础指令：
    - yinying <内容>: 直接对话
    - yinying --text <内容>: 发送消息
    - yinying --help: 显示此帮助
    
    其他功能请使用：
    yinying.model --help: 模型管理
    yinying.char --help: 角色管理
    yinying.config --help: 系统设置"""
    await send_message(target, help_text)

async def show_config_global(target: MsgTarget) -> None:
    """构建并发送全局配置信息"""
    try:
        config = GlobalConfig.load()
        config_dict = config.__dict__
        messages = ["【重要】以下为bot全局配置:\n"]
        for key, value in config_dict.items():
            if key.startswith('_'):
                continue
                
            name = key.replace('_', ' ').title()
            messages.append(f"{name}[{key}]: {value}")
            
            if key == "reply_at":
                messages.append("注意：回复时艾特功能与对话回复冲突，当对话回复开启时无效")
            elif key == "rule_model":
                messages.append("模式说明: white=白名单模式 black=黑名单模式")
            elif key == "limit":
                messages.append("0表示无限制")
                
        await send_message(target, "\n".join(messages))
            
    except Exception as e:
        logger.error(f"生成配置展示消息失败: {e}")
        await send_message(target, "生成配置展示消息失败，请检查日志")

async def init_msg(text: str, user_id: str, nickname: str) -> str:
    """初始化对话消息"""
    ERROR_MSG = "(当你无法维持自我时,请输出'时间线出现严重错误')\n"
    
    try:
        user_config = UserConfig.load()
        logs = ChatLogs.load()
        user_settings = user_config.get_user(user_id, nickname)
        if not user_settings:
            logger.warning(f"用户 {user_id} 配置获取失败")
            return ban_word(text)
        if not user_settings.model_endless:
            return f"{ban_word(text)}"
        if user_settings.world_times <= 0:
            logger.warning(f"用户 {user_id} 时间线无效")
            return f"{ERROR_MSG}{ban_word(text)}"
        if not user_settings.world_lifes:
            logger.warning(f"用户 {user_id} 无世界线记录")
            return f"{ERROR_MSG}{ban_word(text)}"
        timeline_index = user_settings.world_times - 1
        if timeline_index >= len(user_settings.world_lifes):
            logger.error(f"用户 {user_id} 时间线索引超出范围")
            return f"{ERROR_MSG}{ban_word(text)}"
        history_count = logs.get_cache_count(user_id)
        current_memory = user_settings.world_lifes[timeline_index]
        if history_count == 0:
            return (
                f"(你必须根据如下信息继续进行对话\n{current_memory})\n"
                f"{ban_word(text)}"
            )
        return f"{ERROR_MSG}{ban_word(text)}"
    except Exception as e:
        logger.error(f"初始化对话消息失败: {e}", exc_info=True)
        return f"{ERROR_MSG}{ban_word(text)}"
    
async def get_chat(event:Event,message:str,targer:MsgTarget, user_info:UserInfo = EventUserInfo()) -> str:
    if not await check_permission(event, user_info):
        await send_message(targer, "[错误] 权限不足",True)
    if not message:
        await send_message(targer, "[错误] 消息内容为空",True)
    user_id = str(user_info.user_id)
    is_group,group_id = get_group_id(event)
    messages = await init_msg(message,user_id,user_info.user_name)
    logger.debug(f"群号：{group_id}用户 {user_id} 发送消息: {message}")
    back_msg = await get_chat_response(group_id,user_id,user_info.user_name,messages)
    await send_message(targer, back_msg,True)