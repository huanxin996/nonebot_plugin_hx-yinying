import aiohttp, asyncio, json, nonebot,time
from typing import Dict, Optional, Any, Union, Literal,Tuple
from nonebot.log import logger
from ..config import hxconfigs
from .model import YinYingMessage,YinYingModelType,CharacterSet
from ..configs.cyber import CyberManager,CyberCharacter,CyberContribution,CyberContributionManager
from ..configs.easycyber import EasyCyberManager,EasyCyberContributionManager
from ..configs.spconfig import GlobalConfig,GroupConfig,UserConfig
from ..utils.logs import ChatLogs,_global_cache

def json_replace(text:str) -> str:
    """
    移除',"导致的转义问题
    """
    text = text.replace("'","/'")
    text = text.replace('"','/"')
    text = text.replace(',','/,')
    return text

def _truncate_log(data: Any, max_length: int = 10) -> str:
    """截断日志内容"""
    text = str(data)
    if len(text) > max_length:
        return f"{text[:max_length]}..."
    return text


async def make_request(
    url: str,
    method: Literal["GET", "POST"] = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    timeout: int = 30,
    max_retries: int = 3,
    retry_delay: int = 1
) -> Optional[Dict[str, Any]]:
    """
    通用异步请求方法
    
    Args:
        url: 请求地址
        method: 请求方法，支持 "GET" 或 "POST"
        headers: 请求头
        data: POST请求数据
        timeout: 超时时间(秒)
        max_retries: 最大重试次数
        retry_delay: 重试延迟(秒)
    """
    default_headers = {'content-type': 'application/json'}
    if headers:
        default_headers.update(headers)
    
    retry_count = 0
    
    async with aiohttp.ClientSession() as session:
        while retry_count < max_retries:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=default_headers,
                    json=data if method == "POST" else None,
                    timeout=timeout
                ) as response:
                    try:
                        back = await response.json()
                    except json.decoder.JSONDecodeError as e:
                        back = f"json解析报错！\n返回结果：{e}"
                    return back
                        
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                retry_count += 1
                logger.warning(
                    f"网络请求失败 ({retry_count}/{max_retries}): {str(e)}\n"
                    f"URL: {url}"
                )
                if retry_count < max_retries:
                    await asyncio.sleep(retry_delay)
                continue
                
            except Exception as e:
                logger.error(f"请求异常: {str(e)}\nURL: {url}")
                break
                
    logger.error(f"请求失败: 已达到最大重试次数或发生致命错误\nURL: {url}")
    return None

async def check_update() -> Tuple[Optional[str], Optional[str]]:
    """异步检查插件最新版本"""
    url = "https://pypi.org/pypi/nonebot-plugin-hx-yinying/json"
    
    response = await make_request(
        url=url,
        method="GET",
        max_retries=10,
        timeout=50
    )
    
    if response:
        try:
            version = response["info"]["version"]
            time = response["releases"][version][0]["upload_time"]
            return version, time
        except (KeyError, IndexError) as e:
            logger.error(f"解析响应数据失败: {str(e)}")
    
    return None, None

def format_message(
    back_msg: str, 
    times: int, 
    limit: Optional[int] = None,
    world_times: Optional[int] = None,
    lifes: Optional[int] = None
) -> str:
    """格式化返回消息，添加时间线和对话次数信息"""
    TEMPLATES = {
        "WORLD_LINE": "[时..无限.环...overlines{world}-{times}]",
        "LIFE_LINE": "[时..无限.环...overlines{life}-0]",
        "ENDLESS": "[overlines0|{times}]",
        "RESTART": "[时间线..重启.]",
        "NORMAL": "[{times}|{limit}]"
    }
    if world_times is not None:
        suffix = TEMPLATES["WORLD_LINE"].format(
            world=world_times,
            times=times
        )
    elif lifes is not None:
        suffix = TEMPLATES["LIFE_LINE"].format(life=lifes)
    elif limit is None:
        suffix = TEMPLATES["ENDLESS"].format(times=times)
    elif times >= limit:
        suffix = TEMPLATES["RESTART"]
    else:
        suffix = TEMPLATES["NORMAL"].format(
            times=times,
            limit=limit
        )
    return f"{back_msg}{suffix}"

async def yinying_back(
    back: dict, 
    group_id: Optional[str], 
    user_id: str, 
    nickname: str, 
    text: str
) -> str:
    """处理 API 返回的消息内容"""
    try:
        if not back.get('status', True):
            return f"API 返回错误，请检查 API 是否正常！\n{back}"
        message = back.get('choices', [{}])[0].get('message', {})
        back_msg = message.get('content')
        back_role = message.get('role')
        
        # 获取全局配置
        config = GlobalConfig.load()
        user_config = UserConfig.load()
        logs = ChatLogs.load()
        user_settings = user_config.get_user(user_id, nickname)
        
        if group_id:
            group_config = GroupConfig.load()
            model = group_config.get_group(group_id).use_model
        else:
            model = user_settings.private_model
        if back_role != "assistant":
            if "刷新对话试试吧" in back_msg:
                logs.clear_logs(user_id)
                return "时间线出现错误，已重置。"
            admin_group = config.admin_group
            if admin_group:
                report_msg = (
                    f"触发监测！触发者[{user_id}]:{nickname}\n"
                    f"发送内容:{text}\n"
                    f"API 返回内容:{back_msg}"
                )
                await nonebot.get_bot().call_api(
                    "send_group_msg",
                    group_id=admin_group,
                    message=report_msg
                )
            else:
                logger.warning("无 bot 管理群聊，上报触发检测失败")
            return back_msg
        chat_logs = ChatLogs.load()
        user_config = UserConfig.load()
        user_settings = user_config.get_user(user_id, nickname)
        chat_logs.add_log(user_id, "user", json_replace(text))
        chat_logs.add_log(user_id, "assistant", json_replace(back_msg))
        history_count = chat_logs.get_cache_count(user_id) 
        if user_settings.model_endless and model in {"cyberfurry-001", "easycyberfurry-001"}:
            #TODO: 处理时间线
            if history_count >= 6:
                # 保存当前时间线记忆
                #memory = await get_worldline(group_id, user_id, nickname)
                #user_settings.world_lifes.append(memory)
                #user_settings.save()
                
                # 重置时间线
                #config, lifes = keep_timeline(user_id)
                #return format_message(back_msg, history_count, lifes=lifes)
                return format_message(back_msg, history_count, world_times=user_settings.world_times)
            else:
                return format_message(back_msg, history_count, world_times=user_settings.world_times)
        limit = config.limit
        if history_count >= limit:
            logs.clear_logs(user_id)
            times = time.time()
            user_config.update_user(user_id=user_id,time=times)
            return format_message(back_msg, history_count, limit=limit)
        else:
            return format_message(back_msg, history_count, limit=limit)
            
    except Exception as e:
        logger.error(f"处理返回消息失败: {e}", exc_info=True)
        return f"处理消息时出现错误: {e}"

def update_character_set(character_set: dict, prompt_data: Optional[dict]) -> None:
    """更新角色设定
    
    Args:
        character_set (dict): 要更新的角色设定字典
        prompt_data (Optional[dict]): 提示数据
    """
    # 创建角色配置
    char = CharacterSet(
        cf_nickname=prompt_data.get("cfNickname", "Hx") if prompt_data else "Hx",
        cf_species=prompt_data.get("cfSpecies", "龙狼") if prompt_data else "龙狼",
        cf_con_age=prompt_data.get("cfConAge", "child") if prompt_data else "child",
        cf_con_style=prompt_data.get("cfConStyle", "social_anxiety") if prompt_data else "social_anxiety",
        cf_story=prompt_data.get("cfStory", "你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。") if prompt_data else "你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。"
    )
    
    # 更新字典
    if char_dict := char.to_dict():
        character_set.update(char_dict)

def process_model(
    model: str,
    id_config: Optional[dict],
    group_config: Optional[dict],
    user_id: str,
    nickname: str,
    character: Optional[str],
    text: str,
    times: int
) -> dict:
    """处理模型请求"""
    try:
        # 创建消息实例
        message = YinYingMessage.create(
            message=text,
            user_id=user_id,
            model=YinYingModelType(model),
            nick_name=nickname,
            furry_character=character
        )
        model_key = (model.replace('-001', '') + "_in").replace('cyberfurry', 'character')
        prompt_model = group_config.get(model_key) if group_config else id_config.get(model_key)
        if model in {YinYingModelType.CYBERFURRY.value, YinYingModelType.EASYCYBERFURRY.value}:
            if model == YinYingModelType.CYBERFURRY.value:
                cyber_manager = CyberManager.load()
                prompt = cyber_manager.get_character(prompt_model)
                if prompt:
                    message.prompt_patch = prompt.system_prompt
            else:
                easy_manager = EasyCyberManager.load()
                prompt = easy_manager.get_character(prompt_model)
                if prompt:
                    message.character_set = CharacterSet(
                        cf_nickname=prompt.cf_nickname,
                        cf_species=prompt.cf_species,
                        cf_con_age=prompt.cf_con_age,
                        cf_con_style=prompt.cf_con_style,
                        cf_story=prompt.cf_story
                    )
        message.chat_id = f"{hxconfigs.yinying_appid}-{user_id}-{times}-{model}"
        logger.debug(f"[Hx]:处理模型请求: {message.to_dict()}")
        return message.to_dict()
        
    except Exception as e:
        logger.error(f"处理模型请求失败: {e}")
        # 返回默认模型请求
        return YinYingMessage.create(
            message=text,
            user_id=user_id,
            model=YinYingModelType.V3,
            nick_name=nickname,
            furry_character="一只可爱的毛毛龙",
            chat_id=f"{hxconfigs.yinying_appid}-{user_id}-{times}-v3"
        ).to_dict()


async def data_in(
    group_id: Optional[str], 
    user_id: str, 
    nickname: str, 
    text: str
) -> Optional[dict]:
    """构建API请求数据"""
    try:
        user_config = UserConfig.load()
        user_settings = user_config.get_user(user_id, nickname)
        if not user_settings:
            logger.error(f"用户 {user_id} 配置获取失败")
            return None
        if group_id:
            group_config = GroupConfig.load()
            group_settings = group_config.get_group(group_id)
            if not group_settings:
                logger.error(f"群组 {group_id} 配置获取失败")
                return None
            model = group_settings.use_model
            packages_data = process_model(
                model=model,
                group_config=group_settings.to_dict(),
                id_config=user_settings.to_dict(),
                user_id=user_id,
                nickname=nickname,
                character=user_settings.character,
                text=text,
                times=user_settings.time
            )
        else:
            model = user_settings.private_model
            packages_data = process_model(
                model=model,
                id_config=user_settings.to_dict(),
                group_config=None,
                user_id=user_id,
                nickname=nickname,
                character=user_settings.character,
                text=text,
                times=user_settings.time
            )
        logger.debug(f"[Hx]:构建API请求数据: {packages_data}")
        return packages_data
    except Exception as e:
        logger.error(f"构建API请求数据失败: {e}", exc_info=True)
        return None

async def get_chat_response(
    group_id: Optional[str],
    user_id: str,
    nickname: str,
    text: str
) -> Optional[Dict[str, Any]]:
    """获取API聊天响应"""
    try:
        request_data = await data_in(group_id, user_id, nickname, text)
        if not request_data:
            raise RuntimeError("[Hx]:初始化data失败，终止api调用进程！")
            
        if not request_data.get("chatId"):
            raise RuntimeError("[Hx]:未找到chatId，无效对话！")
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {hxconfigs.yinying_token}'
        }
        logger.info(f"[Hx]:正在请求API-header: {_truncate_log(headers)}")
        logger.info(f"[Hx]:正在请求API-data: {_truncate_log(request_data)}")
        response = await make_request(
            url="https://api-yinying-ng.wingmark.cn/v1/chatWithCyberFurry",
            method="POST",
            headers=headers,
            data=request_data,
            max_retries=1,
            timeout=50
        )
        if not response:
            logger.error("API请求失败")
            return None
        logger.debug(f"[Hx]:API返回数据: {_truncate_log(response,max_length=50)}")
        back_msg = await yinying_back(
            back=response,
            group_id=group_id,
            user_id=user_id,
            nickname=nickname,
            text=text
        )
        
        if back_msg:
            return back_msg
        return None
        
    except RuntimeError as e:
        logger.error(f"聊天请求错误: {e}")
        return {"status": False, "message": str(e)}
        
    except Exception as e:
        logger.error(f"处理聊天响应失败: {e}", exc_info=True)
        return None