import asyncio
from nonebot.log import logger
from nonebot import require
from nonebot.plugin import PluginMetadata,inherit_supported_adapters
require("nonebot_plugin_userinfo")
require("nonebot_plugin_alconna")
from .config import Config,configs
from .api import check_update

__plugin_meta__ = PluginMetadata(
    name="Hx_YinYing",
    description="和赛博小狼聊天！\n由CyberFurry®️强力驱动",
    usage=(
        "通过QQ艾特机器人来进行对话",
        "使用方法：\n"
        "1. @机器人 对话内容\n"
        "2. yinying help\n"
    ),
    type="application",
    homepage="https://github.com/huanxin996/nonebot_plugin_hx-yinying",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna","nonebot_plugin_userinfo"),
)

if not configs.localstore_use_cwd:
    logger.warning("由于localstore_use_cwd为False,本地数据插件使用默认路径存储数据，但是本人十分不建议这样做，所以本插件拒绝被加载，请在配置文件中修改localstore_use_cwd为True后重启nonebot")
    raise Exception("Hx_YinYing插件被拒绝被加载")

version, time = asyncio.run(check_update())

logger.opt(colors=True).success( f"""
    <fg #60F5F5>                   ------------------<Y>Hx-v.{version},最后更新于:{time}</Y>----------------</fg #60F5F5>
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
    <fg #60F5F5>                   ------------------<Y>Hx-v.{version},最后更新于:{time}</Y>----------------</fg #60F5F5>
""")


from .commands import *