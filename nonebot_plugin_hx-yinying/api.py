import aiohttp, asyncio, json
from typing import Dict, Optional, Any, Union, Literal,Tuple
from nonebot.log import logger
from .config import configs

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

async def get_chat_response(
    data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {configs.yinying_token}'
    }
    response = await make_request(
        url="https://api-yinying-ng.wingmark.cn/v1/chatWithCyberFurry",
        method="POST",
        headers=headers,
        data=data,
        max_retries=3,
        timeout=50
    )
    
    if response:
        return response
    
    return None