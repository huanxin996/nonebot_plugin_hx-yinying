from nonebot import on_message
from nonebot.rule import to_me,Rule
from nonebot.adapters import Event
from nonebot_plugin_userinfo import EventUserInfo, UserInfo
from nonebot_plugin_alconna import on_alconna,Alconna, Args, Option,Arparma,Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage,MsgTarget
from .utils.methods import *
from .utils.logs import ChatLogs


chat = on_message(rule=to_me()&Rule(check_permission),priority=15, block=True)

# 基础命令
chat_cmd = on_alconna(
    Alconna(
        "yinying",
        Args["content?", str],
        Option("help", help_text="显示帮助信息", alias=["帮助", "指令"]),
        Option("text", Args["content", str], help_text="直接对话内容"),
        Option("refresh", help_text="刷新对话" ,alias=["重置","刷新对话","重置对话","刷新"])
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
            Args.key[str] + Args.value[str],
            help_text="全局配置设置"
        ),
        Option("list", help_text="设置项列表"),
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
            Subcommand(
                "cache",
                Option("add", Args["content", str], help_text="添加测试缓存"),
                Option("clear", help_text="清空缓存"),
                Option("list", Args["type?", str], help_text="显示缓存"),
                help_text="缓存管理"  
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
        Option("switch", Args["name", str], help_text="切换模型"),
        Option("subscribe",  Args["name", str],help_text="当处于easycyber或cyber模型下时，选择使用的角色"),
        Option("info", help_text="显示当前模型信息")
    ),
    block=True
)

# 处理cyberfurry角色命令
cyber_cmd = on_alconna(
    Alconna(
        "yinying.cyber",
        Option("help", help_text="显示角色帮助"),
        Option("submitting", Args["name?", str] + Args["prompt?", str] + Args["public?", bool],help_text="投稿cyber角色设定"),
        Option("add", Args["name", str] + Args["prompt?", str] + Args["public?", bool], help_text="添加cyber角色设定"),
        Option("list", help_text="查看角色列表"),
        Option("info", Args["name", str], help_text="查看角色信息")
    ),
    block=True
)

# 处理easycyberfurry角色命令
easycyber_cmd = on_alconna(
    Alconna(
        "yinying.easycyber",
        Option("help", help_text="显示角色帮助"),
        Option("add", 
            Args["name", str] + 
            Args["species?", str] + 
            Args["age?", str] +
            Args["style?", str] +
            Args["story?", str] +
            Args["public?", bool],
            help_text="添加角色设定"
        ),
        Option("submitting",
            Args["name", str] + 
            Args["species?", str] + 
            Args["age?", str] +
            Args["style?", str] +
            Args["story?", str] +
            Args["public?", bool],
            help_text="投稿角色"
        ),
        Option("list", help_text="查看角色列表"),
        Option("info", Args["name", str], help_text="查看角色信息")
    ),
    block=True
)

@chat.handle()
async def handle_chat_message(event:Event,target: MsgTarget,user_info: UserInfo = EventUserInfo()):
    if not await check_permission(event, user_info):
        await send_message(target, "[错误] 权限不足")
        return
    message = event.get_plaintext()
    await get_chat(event, message, target, user_info)

@chat_cmd.handle()
async def handle_chat(event:Event,arp: Arparma, target: MsgTarget, 
                     user_info: UserInfo = EventUserInfo()):
    """处理基础对话"""
    if not await check_permission(event, user_info):
        await send_message(target, "[错误] 权限不足")
        return
    # 处理帮助指令
    if arp.find("help"):
        await show_help(target)
        return
        
    # 处理直接对话内容
    if content := arp.main_args.get("content"):
        await get_chat(event, content, target, user_info)
        return
            
    # 处理 text 
    if text_opt := arp.options.get("text"):
        if content := text_opt.args.get("content"):
            await get_chat(event, content, target, user_info)
            return

@config_cmd.handle()
async def handle_config(arp: Arparma, target: MsgTarget,
                       user_info: UserInfo = EventUserInfo()):
    """处理配置命令"""
    if not await check_admin_permission(user_info):
        await UniMessage.text("[错误] 需要管理员权限").send(target)
        return
    # 显示帮助
    if arp.find("help"):
        await show_config_help(target)
        return
    if arp.find("list"):
        await show_config_global(target)
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
        
        # 缓存管理
        elif cache := admin.subcommands.get("cache"):
            user_id = str(user_info.user_id)
            
            if add_opt := cache.options.get("add"):
                content = add_opt.args.get("content")
                chat_logs = ChatLogs.load() 
                chat_logs.add_log(user_id, "test", content)
                await UniMessage.text(f"已添加测试缓存: {content}").send(target)
                
            elif clear_opt := cache.options.get("clear"):
                chat_logs = ChatLogs.load()
                chat_logs.clear_logs(user_id, "cache")
                await UniMessage.text("已清空缓存").send(target)
                
            elif list_opt := cache.options.get("list"):
                storage_type = list_opt.args.get("type", "cache")
                chat_logs = ChatLogs.load()
                if storage_type == "cache":
                    logs = chat_logs.get_logs(user_id, use_cache=True)
                    count = chat_logs.get_cache_count(user_id)
                    await UniMessage.text(f"缓存记录({count}条):\n" + 
                        "\n".join(f"{log.rule}: {log.msg}" for log in logs)
                    ).send(target)
                else:
                    logs = chat_logs.get_logs(user_id, use_cache=False)
                    await UniMessage.text("主存储记录:\n" + 
                        "\n".join(f"{log.rule}: {log.msg}" for log in logs)
                    ).send(target)
            return

@model_cmd.handle()
async def handle_model(event:Event,arp: Arparma, target: MsgTarget,
                     user_info: UserInfo = EventUserInfo()):
    """处理角色命令"""
    if not await check_permission(event, user_info):
        await send_message(target, "[错误] 权限不足")
        return
    # 显示帮助
    if arp.find("help"):
        await send_message(target, "[模型] 帮助:\n"
            "1. yinying.model list\n"
            "2. yinying.model switch <模型名称>\n"
            "3. yinying.model subscribe <角色名称>\n",
            True)
    elif arp.find("list"):
        model_list = "\n".join(
                f"{i}. {m}" for i, m in enumerate(m.value for m in YinYingModelType)
            )
        await send_message(target, f"模型列表：\n{model_list}",True)
    elif models := arp.options.get("switch"):
        model = models.args.get("name")
        if model:
            msg = await switch_model(event,model,user_info)
            await send_message(target, msg,True)
        else:
            await send_message(target, "[错误] 请指定模型名称")
    elif subscribe := arp.options.get("subscribe"):
        name = subscribe.args.get("name")
        if not name:
            await send_message(target, "[错误] 请指定角色名称")
            return
        
        msg = await handle_model_subscribe(target,event, name, user_info)
        await send_message(target, msg)

@cyber_cmd.handle()
async def handle_cyber(
    event: Event,
    arp: Arparma,
    target: MsgTarget,
    user_info: UserInfo = EventUserInfo()
):
    """处理cyber命令"""
    async def handle_character_create(name: str, prompt: str, is_public: bool, cmd_type: str = "add"):
        """检查参数完整性"""
        missing_args = []
        if not name:
            name = "角色名称"
            missing_args.append("角色名称")
        if not prompt:
            missing_args.append("系统提示词语")
        if is_public is None:
            missing_args.append("是否公开")
            
        if missing_args:
            msg = (
                f"[提示] {cmd_type}角色 {name} 缺少以下信息:\n"
                f"- {' 和 '.join(missing_args)}\n"
                f"请按以下格式补充:\n"
                f"完整格式: yinying.cyber {cmd_type} {name} <系统提示词语> <是否公开>\n"
            )
            await send_message(target, msg)
            return False
        return True

    # 显示帮助
    if arp.find("help"):
        help_text = (
            "[角色] 帮助:\n"
            "1. 添加角色: yinying.cyber add <角色名称> <系统提示词语> <是否公开>\n" 
            "2. 投稿角色: yinying.cyber submitting <角色名称> <系统提示词语> <是否公开>\n"
            "3. 订阅角色: yinying.cyber subscribe\n"
            "4. 查看列表: yinying.cyber list\n"
            "5. 角色信息: yinying.cyber info <角色名称>\n"
        )
        await send_message(target, help_text)
        return
    
    # 处理添加角色
    for cmd in ["add", "submitting"]:
        if opts := arp.options.get(cmd):
            name = opts.args.get("name")
            prompt = opts.args.get("prompt")  
            is_public = opts.args.get("public")

            # 检查角色名
            if name.lower() in ["hx", "幻歆"]:
                await send_message(target, "[错误] 该名称为保留名称,无法使用")
                return
                
            # 检查是否已存在
            cyber_manager = CyberManager.load()
            contrib_manager = CyberContributionManager.load()
            total_chars = len(cyber_manager.characters) + len(contrib_manager.contributions)
            char_id = total_chars + 1
            
            if cyber_manager.get_character(name) or contrib_manager.get_contribution(name):
                await send_message(target, f"[错误] 角色 {name} 已存在")
                return
                
            # 验证参数完整性
            if not await handle_character_create(name, prompt, is_public, cmd):
                return
                
            try:
                user_id = int(user_info.user_id)
                
                if cmd == "submitting":
                    # 投稿模式 - 使用 CyberContributionManager
                    char = contrib_manager.submit_contribution(
                        id=char_id,
                        nickname=name,
                        contributor_id=user_id,
                        system_prompt=prompt.strip(),
                        public=is_public
                    )
                    
                    if not char:
                        await send_message(target, "[错误] 投稿失败")
                        return
                        
                    # 获取管理员配置
                    global_config = GlobalConfig.load()
                    admin_group = global_config.admin_group
                    admin_user = global_config.admin_pro
                    group_switch = global_config.admin_group_switch
                    user_switch = global_config.admin_user_switch
                    
                    # 构建审核通知
                    msg_tg = (
                        f"新投稿!\n"
                        f"来源于QQ[{user_info.user_id}]\n"
                        f"以下为设定内容\n"
                        f"===========\n"
                        f"昵称:{name}\n"
                        f"system:{prompt}\n\n"
                        f"==========="
                    )
                    
                    # 发送审核通知
                    if admin_group and group_switch:
                        logger.debug(f"发送审核通知: {msg_tg}")
                        #await bot.call_api("send_group_msg", group_id=admin_group, message=msg_tg)
                    if admin_user and user_switch:
                        logger.debug(f"发送审核通知: {msg_tg}")
                        #await bot.call_api("send_private_msg", user_id=admin_user, message=msg_tg)
                        
                    await send_message(target, f"[成功] 角色 {name} 已提交审核")
                    
                else:
                    # 权限检查
                    if not await check_permission(event, user_info):
                        await send_message(target, "[错误] 权限不足")
                        return
                    # 添加模式 - 使用 CyberManager
                    char = CyberCharacter(
                        id=char_id,
                        system_prompt=prompt.strip(),
                        creator=user_id,
                        public=is_public,
                        create_time=int(time.time())
                    )
                    cyber_manager.characters[name] = char
                    cyber_manager.save()
                    await send_message(target, f"[成功] 角色 {name} 添加完成!")
                    
            except Exception as e:
                logger.error(f"处理角色失败: {e}")
                await send_message(target, f"[错误] 处理失败: {e}")
            return


@cyber_cmd.handle()
async def handle_cyber(
    event: Event,
    arp: Arparma, 
    target: MsgTarget,
    user_info: UserInfo = EventUserInfo()
):
    """处理cyber命令"""
    # 显示帮助
    if arp.find("help"):
        help_text = (
            "[角色] 帮助:\n"
            "1. 添加角色: yinying.cyber add <角色名称> <设定> <是否公开>\n" 
            "2. 投稿角色: yinying.cyber submitting <角色名称> <设定> <是否公开>\n"
            "3. 查看列表: yinying.cyber list\n"
        )
        await send_message(target, help_text)
        return

    # 查看列表
    if arp.find("list"):
        try:
            cyber_manager = EasyCyberManager.load()
            contrib_manager = EasyCyberContributionManager.load()
            
            # 获取所有公开角色
            public_chars = [
                name for name, char in cyber_manager.characters.items()
                if char.public
            ]
            # 获取已审核的公开投稿
            public_contribs = [
                char.cf_nickname for char in contrib_manager.get_checked_contributions()
                if char.public
            ]
            
            all_chars = public_chars + public_contribs
            if all_chars:
                msg = "[cyber]可用角色(公开):\n" + "\n".join(all_chars)
            else:
                msg = "当前没有公开的角色"
            await send_message(target, msg)
        except Exception as e:
            logger.error(f"获取角色列表失败: {e}")
            await send_message(target, "获取角色列表失败")
        return

    # 处理添加/投稿角色
    for cmd in ["add", "submitting"]:
        if opts := arp.options.get(cmd):
            name = opts.args.get("name")
            story = opts.args.get("prompt")
            is_public = opts.args.get("public")

            # 基础检查
            if not all([name, story]):
                msg = f"[错误] 添加角色需要提供名称和设定"
                await send_message(target, msg)
                return

            if name.lower() in ["hx", "幻歆"]:
                await send_message(target, "[错误] 该名称为保留名称,无法使用")
                return
                
            try:
                cyber_manager = EasyCyberManager.load()
                contrib_manager = EasyCyberContributionManager.load()
                
                # 检查是否已存在
                if cyber_manager.get_character(name) or contrib_manager.get_contribution(name):
                    await send_message(target, f"[错误] 角色 {name} 已存在")
                    return
                
                if cmd == "submitting":
                    # 投稿模式
                    char = contrib_manager.submit_contribution(
                        nickname=name,
                        contributor_id=user_info.user_id,
                        story=story,
                        public=is_public
                    )
                    
                    if not char:
                        await send_message(target, "[错误] 投稿失败")
                        return
                        
                    # 获取管理员配置
                    global_config = GlobalConfig.load()
                    admin_group = global_config.admin_group
                    admin_user = global_config.admin_pro
                    group_switch = global_config.admin_group_switch
                    user_switch = global_config.admin_user_switch
                    
                    # 构建审核通知
                    msg_tg = (
                        f"新投稿!\n"
                        f"来源于QQ[{user_info.user_id}]\n"
                        f"以下为设定内容\n"
                        f"===========\n"
                        f"昵称:{name}\n"
                        f"故事:{story}\n\n"
                        f"==========="
                    )
                    
                    # 发送审核通知
                    if admin_group and group_switch:
                        logger.debug(f"发送审核通知: {msg_tg}")
                        #await bot.call_api("send_group_msg", group_id=admin_group, message=msg_tg)
                    if admin_user and user_switch:
                        logger.debug(f"发送审核通知: {msg_tg}")
                        #await bot.call_api("send_private_msg", user_id=admin_user, message=msg_tg)
                        
                    await send_message(target, f"[成功] 角色 {name} 已提交审核")
                    
                else:
                    # 权限检查
                    if not await check_permission(event, user_info):
                        await send_message(target, "[错误] 权限不足")
                        return
                        
                    # 添加模式
                    char = cyber_manager.create_character(
                        nickname=name,
                        story=story,
                        creator=user_info.user_id,
                        public=is_public
                    )
                    
                    if char:
                        await send_message(target, f"[成功] 角色 {name} 添加完成!")
                    else:
                        await send_message(target, "[错误] 添加角色失败")
            except Exception as e:
                logger.error(f"处理角色失败: {e}")
                await send_message(target, f"[错误] 处理失败: {e}")
            return


@easycyber_cmd.handle()
async def handle_easycyber(
    event: Event,
    arp: Arparma,
    target: MsgTarget,
    user_info: UserInfo = EventUserInfo()
):
    """处理 easycyber 命令"""
    # 显示帮助
    if arp.find("help"):
        help_text = (
            "[角色] 帮助:\n"
            "1. 添加角色: yinying.easycyber add <名称> [种族] [年龄] [风格] [故事] [是否公开]\n"
            "2. 投稿角色: yinying.easycyber submitting <名称> [种族] [年龄] [风格] [故事] [是否公开]\n"
            "3. 查看列表: yinying.easycyber list\n"
            "4. 角色信息: yinying.easycyber info <名称>\n"
        )
        await send_message(target, help_text)
        return

    # 查看列表
    if arp.find("list"):
        try:
            cyber_manager = EasyCyberManager.load()
            contrib_manager = EasyCyberContributionManager.load()
            
            # 获取所有公开角色
            public_chars = [
                name for name, char in cyber_manager.characters.items()
                if char.public
            ]
            # 获取已审核的公开投稿
            public_contribs = [
                char.cf_nickname for char in contrib_manager.get_checked_contributions()
                if char.public
            ]
            
            all_chars = public_chars + public_contribs
            if all_chars:
                msg = "[cyber]可用角色(公开):\n" + "\n".join(all_chars)
            else:
                msg = "当前没有公开的角色"
            await send_message(target, msg)
        except Exception as e:
            logger.error(f"获取角色列表失败: {e}")
            await send_message(target, "获取角色列表失败")
        return

    # 查看角色信息
    if info := arp.options.get("info"):
        name = info.args.get("name")
        if not name:
            await send_message(target, "[错误] 请指定角色名称")
            return
            
        cyber_manager = EasyCyberManager.load()
        contrib_manager = EasyCyberContributionManager.load()
        
        char = cyber_manager.get_character(name) or contrib_manager.get_contribution(name)
        if not char:
            await send_message(target, f"[错误] 角色 {name} 不存在")
            return
            
        msg = (
            f"[角色信息]\n"
            f"昵称: {char.cf_nickname}\n"
            f"种族: {char.cf_species}\n"
            f"年龄: {char.cf_con_age}\n"
            f"风格: {char.cf_con_style}\n"
            f"故事: {char.cf_story}\n"
            f"公开: {'是' if char.public else '否'}\n"
            f"创建者: {char.creator}\n"
            f"创建时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(char.create_time))}"
        )
        await send_message(target, msg)
        return

    # 处理添加/投稿角色
    for cmd in ["add", "submitting"]:
        if opts := arp.options.get(cmd):
            name = opts.args.get("name")
            species = opts.args.get("species", "未知")
            age = opts.args.get("age", "child")
            style = opts.args.get("style", "social_anxiety")
            story = opts.args.get("story", "")
            is_public = opts.args.get("public", True)

            # 基础检查
            if not name:
                await send_message(target, "[错误] 请指定角色名称")
                return

            if name.lower() in ["hx", "幻歆"]:
                await send_message(target, "[错误] 该名称为保留名称,无法使用")
                return
            
            # 检查年龄参数
            if age not in VALID_AGES:
                age_list = "/".join(f"{k}--[{v}]" for k,v in VALID_AGES.items())
                await send_message(target, f"[错误] 无效的年龄参数\n可用值: \n{age_list}")
                return

            # 检查风格参数    
            if style not in VALID_STYLES:
                style_list = "/".join(f"{k}--[{v}]" for k,v in VALID_STYLES.items())
                await send_message(target, f"[错误] 无效的聊天风格\n可用值: \n{style_list}")
                return
                
            try:
                cyber_manager = EasyCyberManager.load()
                contrib_manager = EasyCyberContributionManager.load()
                
                # 检查是否已存在
                if cyber_manager.get_character(name) or contrib_manager.get_contribution(name):
                    await send_message(target, f"[错误] 角色 {name} 已存在")
                    return
                
                if cmd == "submitting":
                    # 投稿模式
                    char = contrib_manager.submit_contribution(
                        nickname=name,
                        contributor_id=user_info.user_id,
                        species=species,
                        con_age=age,
                        con_style=style,
                        story=story,
                        public=is_public
                    )
                    
                    if not char:
                        await send_message(target, "[错误] 投稿失败")
                        return
                        
                    # 获取管理员配置并发送通知
                    global_config = GlobalConfig.load()
                    msg_tg = (
                        f"新投稿!\n"
                        f"来源于QQ[{user_info.user_id}]\n"
                        f"==========\n"
                        f"昵称: {name}\n"
                        f"种族: {species}\n"
                        f"年龄: {age}\n"
                        f"风格: {style}\n"
                        f"故事: {story}\n"
                        f"公开: {is_public}\n"
                        f"=========="
                    )
                    
                    if global_config.admin_group and global_config.admin_group_switch:
                        logger.info(f"新投稿通知: {msg_tg}")
                        #await bot.call_api("send_group_msg", group_id=global_config.admin_group, message=msg_tg)
                    if global_config.admin_pro and global_config.admin_user_switch:
                        logger.info(f"新投稿通知: {msg_tg}")
                        #await bot.call_api("send_private_msg", user_id=global_config.admin_pro, message=msg_tg)
                        
                    await send_message(target, f"[成功] 角色 {name} 已提交审核")
                    
                else:
                    # 权限检查
                    if not await check_permission(event, user_info):
                        await send_message(target, "[错误] 权限不足")
                        return
                        
                    # 添加模式
                    char = cyber_manager.create_character(
                        nickname=name,
                        species=species,
                        con_age=age,
                        con_style=style,
                        story=story,
                        creator=user_info.user_id,
                        public=is_public
                    )
                    
                    if char:
                        await send_message(target, f"[成功] 角色 {name} 添加完成!")
                    else:
                        await send_message(target, "[错误] 添加角色失败")
                        
            except Exception as e:
                logger.error(f"处理角色失败: {e}")
                await send_message(target, f"[错误] 处理失败: {e}")
            return