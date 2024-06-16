from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message ,get_plugin_config,require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
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
from nonebot.rule import to_me,Rule
import json,random
from .config import Config
from .chat import *
from .report import error_oops,get_file
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


#拉一坨大的😋
#awa--------味大，无需多盐！
logger.opt(colors=True).success( f"""
    <fg #60F5F5>                   ------------------<Y>幻歆v{hx_config.hx_version}</Y>----------------</fg #60F5F5>
<fg #60F5F5>,--,                                                                                                 </fg #60F5F5>                 
<r>      ,--.'|                                       ,--,     ,--,                                 ,---,.               ___   </r> 
<y>   ,--,  | :                                       |'. \   / .`|  ,--,                         ,'  .'  \            ,--.'|_   </y>
<g>,---.'|  : '         ,--,                    ,---, ; \ `\ /' / ;,--.'|         ,---,         ,---.' .' |   ,---.    |  | :,' </g> 
<c>|   | : _' |       ,'_ /|                ,-+-. /  |`. \  /  / .'|  |,      ,-+-. /  |        |   |  |: |  '   ,'\   :  : ' :  </c>
<e>:   : |.'  |  .--. |  | :    ,--.--.    ,--.'|'   | \  \/  / ./ `--'_     ,--.'|'   |        :   :  :  / /   /   |.;__,'  /   </e>
<m>|   ' '  ; :,'_ /| :  . |   /       \  |   |  ,"' |  \  \.'  /  ,' ,'|   |   |  ,"' |        :   |    ; .   ; ,. :|  |   |    </m>
<e>'   |  .'. ||  ' | |  . .  .--.  .-. | |   | /  | |   \  ;  ;   '  | |   |   | /  | |        |   :     \'   | |: ::__,'| :    </e>
<c>|   | :  | '|  | ' |  | |   \__\/: . . |   | |  | |  / \  \  \  |  | :   |   | |  | |        |   |   . |'   | .; :  '  : |__  </c>
<g>'   : |  : ;:  | : ;  ; |   ," .--.; | |   | |  |/  ;  /\  \  \ '  : |__ |   | |  |/         '   :  '; ||   :    |  |  | '.'| </g>
<y>|   | '  ,/ '  :  `--'   \ /  /  ,.  | |   | |--' ./__;  \  ;  \|  | '.'||   | |--'          |   |  | ;  \   \  /   ;  :    ; </y>
<r>;   : ;--'  :  ,      .-./;  :   .'   \|   |/     |   : / \  \  ;  :    ;|   |/              |   :   /    `----'    |  ,   /  </r>
<m>|   ,/       `--`----'    |  ,     .-./'---'      ;   |/   \  ' |  ,   / '---'               |   | ,'                ---`-'   </m>
<r>'---'                      `--`---'               `---'     `--` ---`-'                      `----'</r>
    <fg #60F5F5>                   ------------------<Y>幻歆v{hx_config.hx_version}</Y>----------------</fg #60F5F5>
""")


global_config = config_in_global()
dy_list = json_get(config_in_global(),"dy_list")
log_dir = path_in()

#检查关键配置，自动更新-0.2day
if not hx_config.yinying_appid or not hx_config.yinying_token:
    logger.error("未设置核心配置？！,请检查你配置里的yinying_appid和yinying_token")
else:
    scheduler.add_job(func=check_update,trigger='interval',hours=3,id="huanxin996")
    logger.opt(colors=True).success("【Hx】加载核心配置成功,定时检测更新启动。")

#检测更新
try:
    check_update()
except Exception as e:
    logger.opt(colors=True).error("【Hx】检测更新失败！！，联系开发者！错误捕获{e}")

#尝试检查错误模块
if os.path.exists(f"{log_dir}/file/error_report/hx_error.html"):
    logger.success("【Hx】已加载错误报告模块")
else:
    logger.error("未找到错误报告模块的文件，尝试下载。。。")
    get_file()

#根据订阅信息注册定时任务
try:
    extent = int(len(dy_list))
    for key in dy_list:
        config_1 = config_in_user(key,False)
        user_config = json_get(config_1,key)
        config_time = json_get_pro(user_config,"dy_time")
        config_minute = json_get_pro(user_config,"dy_minute")
        scheduler.add_job(func=get_chat,trigger='interval',args=[key] ,hours=config_time, minutes=config_minute, id=key)
    logger.opt(colors=True).success(f"【Hx】定时任务加载成功,当前共加载{extent}个订阅用户")
except Exception as e:
    logger.opt(colors=True).error(f"【Hx】定时任务加载失败！！，联系开发者！错误捕获{e}")

#加载自定义文件集
if hx_config.hx_chatcommand:
    logger.success(f"【Hx】命令列表加载成功,当前自定义命令列表为{hx_config.hx_chatcommand}")
    ml_st = hx_config.hx_chatcommand
else:
    logger.error(f"【Hx】命令列表加载失败，请检查配置文件")
    ml_st = {'hx','chat'}


#主要命令列表
help = on_command("yy帮助", aliases={"yinyinghelp","hx_help","hx_yinying_help"},rule=Rule(chek_rule_base),  priority=0, block=True)
msg_at = on_message(rule=Rule(chek_rule_base)&to_me(), priority=10,  block=True)
msg_ml = on_command("yinying_chat", aliases=ml_st,rule=Rule(chek_rule_base),  priority=15, block=True)
clear =  on_command("刷新对话", aliases={"clear"},rule=Rule(chek_rule_base),  priority=0, block=True)
history_get = on_command("导出对话", aliases={"getchat"},rule=Rule(chek_rule_base),  priority=0, block=True)
set_global_config = on_command("设置全局配置", aliases={"设置配置全局","globalset"},rule=Rule(chek_rule_admin),  priority=0, block=True)
model_list = on_command("模型列表", aliases={"modellist","chat模型列表"},rule=Rule(chek_rule_base),  priority=0, block=True)
model_handoff = on_command("切换模型", aliases={"qhmodel","切换chat模型","模型切换"},rule=Rule(chek_rule_base),  priority=0, block=True)
easycyber_set = on_command("easycyber", aliases={"easycyber设置","hxworld"},rule=Rule(chek_rule_base),  priority=10, block=True)
cyber_set = on_command("cyber", aliases={"cyber设置","Hxworld"},rule=Rule(chek_rule_base),  priority=10, block=True)
admin_set = on_command("控制台操作", aliases={"管理控制台","setstart"},rule=Rule(chek_rule_admin),  priority=1, block=True)
verision = on_command("确认版本", aliases={"旅行伙伴确认","版本确认"},rule=Rule(chek_rule_base),  priority=9, block=True)
character = on_command("sd", aliases={"旅行伙伴加入","设定加入"},rule=Rule(chek_rule_base),  priority=8, block=True)
chat_ne = on_command("加入订阅", aliases={"旅行伙伴觉醒","订阅加入"},rule=Rule(chek_rule_base),  priority=15, block=True)
time_noend = on_command("切换时间线", aliases={"切换模式"},rule=Rule(chek_rule_base),  priority=0, block=True)
gloubalblack_add = on_command("全局拉黑", aliases={"银影不要理"},rule=Rule(chek_rule_admin),  priority=0, block=True)
banword_add = on_command("添加违禁词", aliases={"banword","违禁词添加"},rule=Rule(chek_rule_admin),  priority=0, block=True)
ces = on_command("测试服务", aliases={"测试报错"},rule=Rule(chek_rule_base), priority=0, block=True)

@help.handle()
async def help(matcher: Matcher,event: MessageEvent):
    msg = "-----帮助列表-----\n刷新对话\n导出对话\n设置全局配置\n模型列表\n切换模型\neasycyber\ncyber\n控制台操作\n确认版本\n旅行伙伴加入\n切换时间线\n全局拉黑\n添加违禁词\n-----(点头)-----"
    await send_msg(matcher, event, msg)

#添加违禁词。
@banword_add.handle()
async def banword_add(matcher: Matcher,event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    config_1 = config_in_global()
    banword = json_get(config_1,"blacklist_world")
    if not text:
        msg= f"咱不知道要添加什么违禁词哦。"
    else:
        if text in banword:
            await send_msg(matcher, event, f"{text}已在违禁词列表里了！")
        banword.append(text)
        config_1["blacklist_world"] = banword
        with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
            json.dump(config_1,file)
            msg= f"{text}已添加到违禁词列表里"
    await send_msg(matcher, event, msg)

#生命模式-无限时间(仅供cyber和easycyber使用)
@time_noend.got(
    "msg",
    prompt=f"请输入时间线\n当前仅支持\n无限-overworld\n普通-nether\n请输入全称：无限-overworld",
)
async def time_noend(matcher: Matcher,bot:Bot, event: MessageEvent):
    text = unescape(event.get_plaintext().strip())
    config_1 = config_in_user(get_id(event),False)
    user_config = json_get(config_1,get_id(event))
    lines = user_config.get("model_endless",False)
    if text == "无限-overworld" and lines != True:
        user_config["model_endless"] = True
        with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
            json.dump(config_1,file)
        msg = ".载入成功"
    elif text == "普通-nether" and lines != False:
        user_config["model_endless"] = True
        with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
            json.dump(config_1,file)
        msg = "..载入成功"
    else:
        msg = "时间线重叠..."
    await send_msg(matcher,event,msg)

#拉黑用户、
@gloubalblack_add.handle()
async def gloubalblack_add(matcher: Matcher,bot:Bot,event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    groupid = event.group_id
    config_1 = config_in_global()
    user_config = json_get(config_1,"blacklist_user")
    if not text:
        id = await extract_member_at(groupid,msg,bot)
        for num in id:
            if num in user_config:
                logger.warning(f"{num}已在黑名单内")
            else:
                user_config.append(num)
        config_1["blacklist_user"] = user_config
        with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
            json.dump(config_1,file)
        msg= f"{id}\n拉黑成功"
    else:
        if text in user_config:
            await send_msg(matcher, event, "该用户已在黑名单内")
        user_config.append(text)
        config_1["blacklist_user"] = user_config
        with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
            json.dump(config_1,file)
            msg= f"{text}拉黑成功"
    await send_msg(matcher, event, msg)

#自定义自己的设定和昵称
@character.handle()
async def character(matcher: Matcher,bot:Bot, event: MessageEvent, msg: Message = CommandArg()):
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
                config_get["nick"] = msg[0]
                config_get["character"] = msg[1]
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

#版本确认
@verision.handle()
async def verision_get(matcher: Matcher, event: MessageEvent):
    new_verision, time = update_hx()
    if get_groupid(event):
        id = get_groupid(event)
        e_config = config_in_group(id)
        config = json_get(e_config,id)
        model = json_get(config,"use_model")
        if not new_verision and not hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前群聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前群聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前群聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        elif new_verision > hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if not model_in or model_in == None:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                else:
                    msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前群聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        else:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if  not model_in or model_in == None:
                    msg =f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                else:
                    msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前群聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        await send_msg(matcher, event, msg)
    else:
        config = json_get(config_in_user(get_id(event),False),get_id(event))
        model = json_get(config,"private_model")
        if not new_verision and not hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前私聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前私聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[？？？]\n你的插件版本可能已过时，当前无法获取最新版本\n当前私聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        elif new_verision > hx_config.hx_version:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in:
                    msg =f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(歪头)\n======================\n当前版本号:v{hx_config.hx_version}[已过时(]\n你的插件版本已过时，当前最新版本为v{new_verision}\n当前私聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        else:
            if model == "easycyberfurry-001":
                model_in = json_get(config,"easycharacter_in")
                if model_in:
                    msg =f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:{model}\n当前模型载入角色:Hx\n最后更新时间:====>\n{time}\n======================"
                msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:{model}\n当前模型载入角色:{model_in}\n最后更新时间:====>\n{time}\n======================"
            else:
                msg = f"(点头)\n======================\n当前版本号:v{hx_config.hx_version}[最新！]\n当前私聊使用模型:{model}\n最后更新时间:====>\n{time}\n======================"
        await send_msg(matcher, event, msg)

#@对话
@msg_at.handle()
async def at(matcher: Matcher, event: MessageEvent, bot: Bot):
    groupid = get_groupid(event)
    try:
        await get_answer_at(matcher, event, bot)
    except Exception as e:
        if groupid:
            img = await error_oops()
            await bot.call_api("send_group_msg",group_id=groupid,message=MessageSegment.image(img))
        else:
            img = await error_oops()
            await bot.call_api("send_private_msg",user_id=id,message=MessageSegment.image(img))

#指令对话
@msg_ml.handle()
async def ml(matcher: Matcher, event: MessageEvent, bot: Bot, msg: Message = CommandArg()):
    groupid = get_groupid(event)
    try:
        await get_answer_ml(matcher, event, bot ,msg)
    except Exception as e:
        if groupid:
            img = await error_oops()
            await bot.call_api("send_group_msg",group_id=groupid,message=MessageSegment.image(img))
        else:
            img = await error_oops()
            await bot.call_api("send_private_msg",user_id=id,message=MessageSegment.image(img))

#刷新对话
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

#设置全局配置
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
            get_config = await json_get_pro(config,text)
            if get_config == 2:
                s["last"] = True
                msg = f"无法查找到该配置项！，请检查其是否为正确的配置名{text}"
                await send_msg(matcher,event,msg)
            else:
                s["last"] = True
                msg = f"{text}状态为:{get_config}"
                await send_msg(matcher,event,msg)

        if s["last"] == "修改":
            config = config_in_global()
            if text == "退出":
                s["last"] = True
                msg = "已退出"
                await send_msg(matcher,event,msg)
            else:
                TFkey, Wkey, Listkey = await config_list(config)
                if text in TFkey:
                    s["last"] = "修改TF"
                    s["set"] = text
                    msg = "请发送开启或关闭【也可以是on或者off或者开和关】"
                    await send_msg_reject(matcher,event,msg)
                elif text in Wkey:
                    s["last"] = "修改w"
                    s["set"] = text
                    msg = "请发送id（群号或者QQ号或者是对话限制次数，看你改哪个配置项）"
                    await send_msg_reject(matcher,event,msg)
                elif text in Listkey:
                    s["last"] = "updata_LK"
                    s["set"] = text
                    msg = "请发送添加或删除【也可以是增加或者移除】"
                    await send_msg_reject(matcher,event,msg)
                else:
                    s["last"] = "修改"
                    msg = "无法查找到该配置项！，请检查其是否为正确的配置名,请重新输入！\n如需退出请发送退出"
                    await send_msg_reject(matcher,event,msg)
                    return
        
        if s["last"] == "修改TF":
            config = config_in_global()
            config_name = s["set"]
            get_config = await json_get_pro(config,config_name)
            logger.debug(f"{get_config}")
            key = {"on":False,"off":False,"开":True,"关":False,"开启":True,"关闭":False}
            if text in key:
                s["last"] = True
                text = key[f"{text}"]
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
            else:
                msg = "未知"
            await send_msg(matcher,event,msg) 
                
     
        
        if s["last"] == "修改w":
            config = config_in_global()
            config_name = s["set"]
            get_config = await json_get_pro(config,config_name)
            config[f"{config_name}"] = int(text)
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

#导出历史记录（私人消息转发,,还有我写的lj文件发送
@history_get.handle()
async def history(bot: Bot, event: MessageEvent,events: Event):
    id = get_id(event)
    msg_list = await get_history(id,bot,event)
    if isinstance(events, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore
    else:
        await bot.send_private_forward_msg(user_id=id, messages=msg_list)  # type: ignore

#获取模型列表
@model_list.handle()
async def list(matcher: Matcher, event: MessageEvent):
        msg = "1.yinyingllm-v1\n2.yinyingllm-v3\n3.yinyingllm-v4\n4.cyberfurry-001\n5.easycyberfurry-001\n切换模型请发送:切换模型(序号)"
        await send_msg(matcher, event, msg)

#模型切换方面
@model_handoff.handle()
async def handoff(matcher: Matcher, bot: Bot, event: MessageEvent,events: Event, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    nick = await get_nick(bot,event)
    id = get_id(event)
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
                clear_id(id,nick)
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
                user_config['private_model'] = model
                config_user[f"{id}"] = user_config
                with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                    json.dump(config_user,file)
                clear_id(id,nick)
                msg =f"切换成功（当前模型已切换为{model})"
                await send_msg(matcher,event,msg)
    else:
        msg = "请注意，切换模型后不能为空哦"
        await send_msg(matcher,event,msg)

#easycyber操作（投稿和载入和查看）
@easycyber_set.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n投稿 #投稿自定义预设(不允许同名)\n载入 #载入自定义预设(不允许不存在)\n查看列表 #列出所有公开的自定义预设\n退出 #退出设置\n发送非预期命令则退出",
)
async def _(matcher: Matcher, bot:Bot, event: MessageEvent, s: T_State,events: Event):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    easycyber_package = {}
    if text == "退出":
        s["last"] = True
        msg = "已退出"
        await send_msg(matcher,event,msg) 
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "增加":
            if text == "" or not text:
                s["last"] = "增加"
                msg = "无效昵称"
                await send_msg_reject(matcher,event,msg)
            if text == "Hx" or text == "HX" or text == "幻歆":
                s["last"] = True
                msg = "easycyber预设“Hx”不能删除或修改，如要改动请改源码"
                await send_msg(matcher,event,msg)
            elif text in easycyber_in_tg() or text in easycyber_in():
                s["last"] = "增加"
                msg = "该预设角色名称已经存在，请不要重复使用该昵称，请重新输入，如需退出请发送退出"
                await send_msg_reject(matcher,event,msg)
            else:
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
            key = ['child','young','adult']
            if not text in key:
                s["last"] = "cfconage"
                msg = "未找到该类型的角色聊天年龄!请重新输入，如需退出请发送：退出"
                await send_msg_reject(matcher,event,msg)
            else:
                s["cfconage"] = text
                s["last"] = "cfconstyle"
                msg = "请输入角色聊天风格:(比如\n vivid--[活泼]\n sentiment--[富有情感(共情大师？)]\n assistant--[助理]\n chilly--[冷酷无情]\n social_anxiety--[社恐]\nps:只输入--前面的英文即可"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfconstyle":
            key = ['vivid','sentiment','assistant','chilly','social_anxiety']
            if not text in key:
                s["last"] = "cfconstyle"
                msg = "未找到该类型的角色聊天风格！请重新输入，如需退出请发送：退出"
                await send_msg_reject(matcher,event,msg)
            else:
                s["cfconstyle"] = json_replace(text)
                s["last"] = "cfstory"
                msg = "请输入角色的背景故事（这对他真的很重要\n[胡言乱语：我要给他完整的一生！！！]"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "cfstory":
            s["cfstory"] = text
            s["last"] = "public"
            msg = "该角色是否公开？(最后一步)完成将发送到bot管理站进行审核，审核通过后即可使用,请发送是或否或者公开或不公开"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "public":
            key = {"是":True,"否":False,"公开":True,"不公开":False}
            if not text in key:
                s["last"] = "public"
                msg = "非正确格式！请重新输入，如需退出请发送：退出"
                await send_msg_reject(matcher,event,msg)
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
                easycyber_package["public"] = key[f"{text}"]
                easycyber_package["creator"] = int(id)
                s["last"] = True
                cybernick = s["cfnickname"]
                g = json_get(config_in_global(),"admin_group")
                u = json_get(config_in_global(),"admin_pro")
                g_k = json_get(config_in_global(),"admin_group_switch")
                u_k = json_get(config_in_global(),"admin_user_switch")
                msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\n物种:{species}\n年龄:{age}\n回复风格:{stytle}\n角色故事:{story}\n==========="
                msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                if not g and not u:
                    msg ="bot管理者未配置，超级管理员和bot控制台,审核失败！"
                elif not u and g:
                    easycyber_in_tg(cybernick,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                elif not g and u:
                    easycyber_in_tg(cybernick,easycyber_package)
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                elif u_k and g_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                elif u_k:
                    easycyber_in_tg(cybernick,easycyber_package)
                    adminid = json_get(config_in_global(),"admin_pro")
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                else:
                    easycyber_in_tg(cybernick,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                await send_msg(matcher,event,msg)


        if s["last"] == "载入":
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
                    if config_group["easycharacter_in"] == text:
                        msg = f"{text}模型已加载，请勿重新加载"  
                    else:
                        config_group["easycharacter_in"] = f"{text}"
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
                    if user["easycharacter_in"]== text:
                        msg = f"{text}模型已加载，请勿重新加载"  
                    else:
                        user["easycharacter_in"] = f"{text}"
                        config_user[f"{id}"] = user
                        with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                            json.dump(config_user,file)
                            msg = f"{text}加载成功！"
                elif not public:
                    msg = f"{text}模型拒绝被加载(可能是模型不存在或者模型非公开！)"      
                else:
                    if user["easycharacter_in"] == text:
                        msg = f"{text}模型已加载，请勿重新加载"  
                    else:
                        user["easycharacter_in"] = f"{text}"
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
            msg = f"[easycyber]可用角色(公开)\n"
            msg += "\n".join(list_got)
        except Exception as e:
            logger.opt(colors=True).error(f"【Hx】:错误捕获:{e}")
            msg = "当前没有公开的角色哦"
        await send_msg(matcher,event,msg)
    # 退出
    if s["last"]:
        return
    else:
        msg = f"未知命令“{text}”，已退出"
        await send_msg(matcher,event,msg)

#cyber操作（投稿和载入和查看）
@cyber_set.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n投稿 #投稿自定义预设(不允许同名)\n载入 #载入自定义预设(不允许不存在)\n查看列表 #列出所有公开的自定义预设\n退出 #退出设置\n发送非预期命令则退出",
)
async def _(matcher: Matcher, bot:Bot, event: MessageEvent, s: T_State,events: Event):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    easycyber_package = {}
    if text == "退出":
        s["last"] = True
        msg = "已退出"
        await send_msg(matcher,event,msg)  
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "增加":
            if text == "Hx" or text == "HX" or text == "幻歆":
                s["last"] = True
                msg = "cyber预设“Hx”不能删除或修改，如要改动请改源码"
                await send_msg(matcher,event,msg)
            elif text in cyber_in_tg() or text in cyber_in():
                s["last"] = True
                msg = "该预设角色名称已经存在，请不要重复使用该昵称."
                await send_msg(matcher,event,msg)
            else:
                s["name"] = text
                s["last"] = "system"
                msg = "该角色的systempromote是？"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "system":
            s["systempromote"] = text
            s["last"] = "public"
            msg = "该角色是否公开u\n请发送公开或不公开（也可以是是或否或者True或False）"
            await send_msg_reject(matcher,event,msg)

        if s["last"] == "public":
            key = {"是":True,"否":False,"公开":True,"不公开":False}
            if not text in key:
                s["last"] = "public"
                msg = "非正确格式！请重新输入，如需退出请发送：退出"
                await send_msg_reject(matcher,event,msg)
            else:
                name = s["name"]
                systempromote = s["systempromote"]
                easycyber_package["system"] = s["systempromote"]
                easycyber_package["public"] = key[f"{text}"]
                easycyber_package["creator"] = int(id)
                s["last"] = True
                g = json_get(config_in_global(),"admin_group")
                u = json_get(config_in_global(),"admin_pro")
                g_k = json_get(config_in_global(),"admin_group_switch")
                u_k = json_get(config_in_global(),"admin_user_switch")
                msg_tg = f"新投稿！\n来源于QQ[{id}]\n以下为设定内容\n===========\n昵称:{name}\nsystem:{systempromote}\n\n==========="
                msg = "投稿成功！，等待审核(问就是权限还没写好)]"
                if not g and not u:
                    logger.opt(colors=True).success(f"{g},{u}")
                    msg ="bot管理者未配置，超级管理员和bot控制台,审核失败！"
                elif not u and g:
                    cyber_in_tg(name,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                elif not g and u:
                    cyber_in_tg(name,easycyber_package)
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                elif u_k and g_k:
                    cyber_in_tg(name,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                elif u_k:
                    cyber_in_tg(name,easycyber_package)
                    await bot.call_api("send_private_msg",user_id=u, message=msg_tg)
                else:
                    cyber_in_tg(name,easycyber_package)
                    await bot.call_api("send_group_msg",group_id=g, message=msg_tg)
                await send_msg(matcher,event,msg)

        if s["last"] == "载入":
            s["last"] = True
            if isinstance(events, GroupMessageEvent):
                groupid = get_groupid(event)
                config = config_in_group(groupid)
                config_group = json_get(config,groupid)
                promte = json_get(cyber_in(False,False),f"{text}")
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
                promte = json_get(cyber_in(False,False),f"{text}")
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
                        with open(f'{log_dir}\config\config_user.json','w',encoding='utf-8') as file:
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
        list_in = cyber_in(False,False)
        try:
            list_got = []
            for key in list_in:
                if list_in[f"{key}"]["public"]:
                    list_got.append(format(key))
                else:
                    return
            msg = f"[cyber]可用角色(公开)\n"
            msg += "\n".join(list_got)
        except Exception as e:
            msg = "当前没有公开的角色哦"
        await send_msg(matcher,event,msg)
    # 退出
    if s["last"]:
        return
    else:
        msg = f"未知命令“{text}”，已退出"
        await send_msg(matcher,event,msg)

#所有投稿管理处理
@admin_set.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n通过 #通过投稿的预设(不允许同名)\n拒绝 #拒绝投稿的自定义预设(不允许同名)\n查看 #查看投稿预设详情(不允许不存在)\n查看投稿列表 #列出所有投稿的自定义预设\n添加admin #添加bot管理者\n退出 #退出\n仅支持bot管理员使用！\n发送非预期命令则退出",
)
async def _(matcher: Matcher, bot:Bot, event: MessageEvent, s: T_State):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    place_user = place(id)
    if place_user >= 9:
        if "last" not in s:
            s["last"] = ""
        if s["last"]:
            if s["last"] == "通过":
                msg = "请输入要通过的预设名称，如果不知道建议先get下列表"
                if text == "easycyber":
                    s["last"] = "easyber"
                    await send_msg_reject(matcher,event,msg)
                elif text == "cyber":
                    s["last"] = "cyber"
                    await send_msg_reject(matcher,event,msg)

            if s["last"] == "easyber":
                s["last"] = True
                json_1 = easycyber_in_tg()
                json_data = json_get(json_1,text)
                json_data["tg_admin"] = id
                user = json_data["creator"]
                in_ok = easycyber_in(text,json_data)
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/easycyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                    msg = f"[easycyber]已通过投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

            if s["last"] == "cyber":
                s["last"] = True
                json_1 = cyber_in_tg()
                json_data = json_get(json_1,text)
                logger.debug(json_data)
                json_data["tg_admin"] = id
                user = json_data["creator"]
                in_ok = cyber_in(text,json_data)
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/cyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                msg = f"[cyber]已通过投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

            if s["last"] == "拒绝":
                msg = "请输入要拒绝的预设名称，如果不知道建议先get下列表"
                if text == "easycyber":
                    s["last"] = "badeasyber"
                    await send_msg_reject(matcher,event,msg)
                elif text == "cyber":
                    s["last"] = "badcyber"
                    await send_msg_reject(matcher,event,msg)
            
            if s["last"] == "badeasyber":
                s["last"] = True
                json_1 = easycyber_in_tg()
                json_data = json_get(json_1,text)
                user = json_data["creator"]
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/easycyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                    msg = f"已拒绝投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

            if s["last"] == "badcyber":
                s["last"] = True
                json_1 = cyber_in_tg()
                json_data = json_get(json_1,text)
                user = json_data["creator"]
                end_json = json_1.pop(f"{text}")
                with open(f'{log_dir}/file/cyber_tg.json','w',encoding='utf-8') as file:
                    json.dump(json_1,file)
                    msg = f"已拒绝投稿用户为{user}关于角色{text}的投稿"
                await send_msg(matcher,event,msg)

        if text == "通过":
            s["last"] = "通过"
            msg = "请输入要通过的预设类型\n例如：cyber或者easycyber"
            await send_msg_reject(matcher,event,msg)


        if text == "查看投稿列表":
            s["last"] = True
            list_in = easycyber_in_tg(False,False)
            msg_list = []
            for key in list_in:
                msg_list.append(format(key))
            msg = f"[easycyber]投稿角色列表：\n"
            msg += "\n".join(msg_list)
            list_in = cyber_in_tg(False,False)
            msg_list = []
            for key in list_in:
                msg_list.append(format(key))
            msg += f"\n\n[cyber]投稿角色列表：\n"
            msg += "\n".join(msg_list)
            await send_msg(matcher,event,f"{msg}")

        if text == "拒绝":
            s["last"] = "拒绝"
            msg = "请输入要的预设类型\n例如：cyber或者easycyber"
            await send_msg_reject(matcher,event,msg)

        if s["last"]:
            return
        else:
            msg = f"未知命令“{text}”，已退出"
            await send_msg(matcher,event,msg)

    else:
        msg = f"你的权限为{place_user},权限不足，无法操作"
        await send_msg(matcher, event, msg)

#订阅系统
@chat_ne.got(
    "msg",
    prompt=f"发送以下选项执行相应功能\n加入 #银影将会主动来找你聊天》？\n退出 #呜呜呜，真的要赶银影走吗\n查看加入列表 #字如其意(仅限管理员使用)\n发送非预期命令则退出",
)
async def _(matcher: Matcher,event: MessageEvent, s: T_State):
    id = get_id(event)
    text = unescape(event.get_plaintext().strip())
    config_1 = config_in_user(id,False)
    user_config = json_get(config_1,id)
    global_config = config_in_global()
    dy_list = json_get(global_config,"dy_list")
    if "last" not in s:
        s["last"] = ""
    if s["last"]:
        if s["last"] == "加入":
            if text == "惊喜":
                s["last"] = True
                hour = random.randint(1,2)
                minute = random.randint(1,59)
                user_config["dy_time"] = hour
                user_config["dy_minute"] = minute
                dy_list.append(id)
                config_1[f"{id}"] = user_config
                global_config["dy_list"] = dy_list
                msg = "好哦，银影会不定时来找你聊天的！"
                scheduler.add_job(func=get_chat,trigger='interval',args=[id] ,hours=hour, minutes=minute, id=id)
                with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                    json.dump(global_config,file)
                with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                    json.dump(config_1,file)
                await send_msg(matcher,event,msg)
            elif text == "稳定":
                s["last"] = "hour"
                msg = "接下来你发送的数字将决定chat角色每过去几小时*分钟来找你一次"
                await send_msg_reject(matcher,event,msg)

        if s["last"] == "hour":
            s["last"] = "minutes"
            s["hour"] = text
            msg = f"接下来你发送的数字将决定chat角色每过去{text}小时;几分钟来找你一次"
            await send_msg_reject(matcher,event,msg)
        
        if s["last"] == "minutes":
            s["last"] = True
            hour = s["hour"]
            minute = text
            user_config["dy_time"] = int(hour)
            user_config["dy_minute"] = int(minute)
            dy_list.append(id)
            config_1[f"{id}"] = user_config
            global_config["dy_list"] = dy_list
            msg = "好哦，银影会不定时来找你聊天的！"
            with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                json.dump(global_config,file)
            with open(f'{log_dir}/config/config_user.json','w',encoding='utf-8') as file:
                json.dump(config_1,file)
            await send_msg(matcher,event,msg)


    if text == "加入":
        s["last"] = "加入"
        global_config = config_in_global()
        dy_list = json_get(global_config,"dy_list")
        if id in dy_list:
            msg = "你已经在银影的特关列表了），请不要重复添加"
        else:
            msg = "请选择惊喜or稳定\n发送：惊喜或者稳定即可"
        await send_msg_reject(matcher,event,msg)

    if text == "退出":
        s["last"] = True
        global_config = config_in_global()
        dy_list = json_get(global_config,"dy_list")
        if not id in dy_list:
            msg = "你不在银影的特关列表哦（"
        else:
            msg = "那再见咯，银影会想你的"
            end_json = dy_list.remove(id)
            global_config["dy_list"] = dy_list
            scheduler.remove_job(id)
            with open(f'{log_dir}/config/config_global.json','w',encoding='utf-8') as file:
                json.dump(global_config,file)
        await send_msg_reject(matcher,event,msg)

    if text == "查看加入列表":
        s["last"] = True
        msg = "在写了在写了，呜呜呜呜呜呜呜😭"
        await send_msg(matcher,event,msg)

    # 退出
    if s["last"]:
        return
    else:
        msg = f"未知命令“{text}”，已退出"
        await send_msg(matcher,event,msg)

#测试函数
@ces.handle()
async def _(event: MessageEvent,bot:Bot):
    try:
        await get_id()
    except Exception as e:
       img = await error_oops()
       id = event.group_id
       await bot.call_api("send_group_msg",group_id=id,message=MessageSegment.image(img))