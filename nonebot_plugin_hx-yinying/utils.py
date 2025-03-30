from nonebot_plugin_userinfo import EventUserInfo, UserInfo
from nonebot_plugin_alconna.uniseg import UniMessage,MsgTarget
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from .globalvar import GlobalConfig,GroupConfig,UserConfig

def json_replace(text:str) -> str:
    """
    移除',"导致的转义问题
    """
    text = text.replace("'","/'")
    text = text.replace('"','/"')
    text = text.replace(',','/,')
    return text

def ban_word(text:str) -> str:
    """违禁词剔除函数"""
    config = GlobalConfig.load()
    ban_word_list = config.blacklist_world
    if ban_word_list:
        for word in ban_word_list:
            if word and word in text:
                text = text.replace(word, "w" * len(word))
                
    return text

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

async def check_base_permission(user_info: UserInfo = EventUserInfo()) -> bool:
    """检查基础权限"""
    config = GlobalConfig.load()
    user_id = str(user_info.user_id)
    
    if config.rule_model == "white":
        return user_id in config.white_user
        
    return user_id not in config.blacklist_user

async def check_admin_permission(user_info: UserInfo = EventUserInfo()) -> bool:
    """
    检查管理员权限
    
    Args:
        user_info: 用户信息对象
        
    Returns:
        bool: 是否有管理员权限
    """
    config = GlobalConfig.load()
    logger.debug(f"{config.admin_user} {config.admin_group}")
    user_id = str(user_info.user_id)
    
    if user_id in config.admin_user:
        return True
        
    try:
        from nonebot.adapters.onebot.v11 import Event
        event = Event()  # 创建一个空事件对象
        event.user_id = int(user_id)
        return await SUPERUSER(event)
    except Exception as e:
        logger.warning(f"超级用户权限检查失败: {e}")
        return True

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
