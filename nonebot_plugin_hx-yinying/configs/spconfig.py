from dataclasses import dataclass, field
from typing import Optional, List, Dict
from .globalvar import GlobalVars,logger,time

@dataclass
class GlobalConfig:
    """全局配置模型"""
    # 开关配置
    global_switch: bool = True
    admin_group_switch: bool = True
    admin_user_switch: bool = False
    at_reply: bool = True
    reply: bool = False
    reply_at: bool = False
    private: bool = True
    
    # 权限配置
    admin_pro: Optional[str] = None
    admin_group: Optional[str] = None
    admin_user: List[str] = field(default_factory=list)
    white_user: List[str] = field(default_factory=list)
    white_group: List[str] = field(default_factory=list)
    
    # 黑名单配置
    rule_model: str = "black"
    blacklist_user: List[str] = field(default_factory=list)
    blacklist_group: List[str] = field(default_factory=list)
    blacklist_world: List[str] = field(default_factory=list)
    
    # 其他配置
    limit: int = 12
    dy_list: List[str] = field(default_factory=list)

    @classmethod
    def load(cls) -> "GlobalConfig":
        """从 GlobalVars 加载配置"""
        try:
            config_data = GlobalVars.get("config", "config_global.json", {})
            if not config_data:
                config = cls()
                config.save()
                return config
            return cls(**config_data)
        except Exception as e:
            logger.error(f"加载全局配置失败: {e}")
            return cls()
    
    def save(self) -> None:
        """保存配置到 GlobalVars"""
        try:
            config_data = {
                'global_switch': self.global_switch,
                'admin_pro': self.admin_pro,
                'admin_group': self.admin_group,
                'admin_group_switch': self.admin_group_switch,
                'admin_user_switch': self.admin_user_switch,
                'limit': self.limit,
                'at_reply': self.at_reply,
                'reply': self.reply,
                'reply_at': self.reply_at,
                'private': self.private,
                'dy_list': self.dy_list,
                'rule_model': self.rule_model,
                'white_user': self.white_user,
                'white_group': self.white_group,
                'admin_user': self.admin_user,
                'blacklist_user': self.blacklist_user,
                'blacklist_group': self.blacklist_group,
                'blacklist_world': self.blacklist_world
            }
            GlobalVars.set("config", config_data, "config_global.json")
        except Exception as e:
            logger.error(f"保存全局配置失败: {e}")
            
    def update(self, **kwargs) -> None:
        """更新配置项"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        
    def add_to_list(self, list_name: str, value: str) -> bool:
        """添加值到列表"""
        if hasattr(self, list_name) and isinstance(getattr(self, list_name), list):
            target_list = getattr(self, list_name)
            if value not in target_list:
                target_list.append(value)
                self.save()
                return True
        return False
        
    def remove_from_list(self, list_name: str, value: str) -> bool:
        """从列表移除值"""
        if hasattr(self, list_name) and isinstance(getattr(self, list_name), list):
            target_list = getattr(self, list_name)
            if value in target_list:
                target_list.remove(value)
                self.save()
                return True
        return False

@dataclass
class GroupConfigItem:
    """单个群组的配置项"""
    use_model: str = "yinyingllm-v2"
    character_in: bool = True
    easycharacter_in: bool = True
    chat_alltimes: int = 0
    first_chattime: int = field(default_factory=lambda: int(time.time()))
    last_chattime: int = field(default_factory=lambda: int(time.time()))
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'use_model': self.use_model,
            'character_in': self.character_in,
            'easycharacter_in': self.easycharacter_in,
            'chat_alltimes': self.chat_alltimes,
            'first_chattime': self.first_chattime,
            'last_chattime': self.last_chattime
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GroupConfigItem":
        """从字典创建实例"""
        return cls(**data)

@dataclass
class GroupConfig:
    """群组配置管理"""
    groups: Dict[str, GroupConfigItem] = field(default_factory=dict)
    
    @classmethod
    def load(cls) -> "GroupConfig":
        """从 GlobalVars 加载配置"""
        try:
            config_data = GlobalVars.get("group_config", "config_group.json", {})
            instance = cls()
            for group_id, group_data in config_data.items():
                instance.groups[group_id] = GroupConfigItem.from_dict(group_data)
            return instance
        except Exception as e:
            logger.error(f"加载群组配置失败: {e}")
            return cls()
    
    def save(self) -> None:
        """保存配置到 GlobalVars"""
        try:
            config_data = {
                group_id: group_config.to_dict()
                for group_id, group_config in self.groups.items()
            }
            GlobalVars.set("group_config", config_data, "config_group.json")
        except Exception as e:
            logger.error(f"保存群组配置失败: {e}")
    
    def get_group(self, group_id: str) -> GroupConfigItem:
        """获取群组配置，如果不存在则创建新的"""
        if group_id not in self.groups:
            self.groups[group_id] = GroupConfigItem()
            self.save()
        return self.groups[group_id]
    
    def update_group(self, group_id: str, **kwargs) -> None:
        """更新群组配置"""
        group_config = self.get_group(group_id)
        for key, value in kwargs.items():
            if hasattr(group_config, key):
                setattr(group_config, key, value)
        self.save()
    
    def record_chat(self, group_id: str) -> None:
        """记录聊天"""
        group_config = self.get_group(group_id)
        group_config.chat_alltimes += 1
        group_config.last_chattime = int(time.time())
        self.save()

@dataclass
class UserConfigItem:
    """单个用户的配置项"""
    character: str = "一只可爱的毛毛龙"
    character_in: bool = True
    easycharacter_in: bool = True
    private_model: str = "yinyingllm-v2"
    chat_alltimes: int = 0
    times: int = 1
    all_times: int = 1
    world_timeline: Optional[str] = None
    model_endless: bool = False
    world_times: int = 0
    world_lifes: List[str] = field(default_factory=list)
    dy_time: int = 3
    dy_minute: int = 3
    time: int = 1713710000
    first_chattime: int = field(default_factory=lambda: int(time.time()))
    last_chattime: int = field(default_factory=lambda: int(time.time()))
    nick: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'character': self.character,
            'character_in': self.character_in,
            'easycharacter_in': self.easycharacter_in,
            'private_model': self.private_model,
            'chat_alltimes': self.chat_alltimes,
            'times': self.times,
            'all_times': self.all_times,
            'world_timeline': self.world_timeline,
            'model_endless': self.model_endless,
            'world_times': self.world_times,
            'world_lifes': self.world_lifes,
            'dy_time': self.dy_time,
            'dy_minute': self.dy_minute,
            'time': self.time,
            'first_chattime': self.first_chattime,
            'last_chattime': self.last_chattime,
            'nick': self.nick
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserConfigItem":
        """从字典创建实例"""
        return cls(**data)

@dataclass
class UserConfig:
    """用户配置管理"""
    users: Dict[str, UserConfigItem] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "UserConfig":
        """从 GlobalVars 加载配置"""
        try:
            config_data = GlobalVars.get("user_config", "config_user.json", {})
            instance = cls()
            for user_id, user_data in config_data.items():
                instance.users[user_id] = UserConfigItem.from_dict(user_data)
            return instance
        except Exception as e:
            logger.error(f"加载用户配置失败: {e}")
            return cls()

    def save(self) -> None:
        """保存配置到 GlobalVars"""
        try:
            config_data = {
                user_id: user_config.to_dict()
                for user_id, user_config in self.users.items()
            }
            GlobalVars.set("user_config", config_data, "config_user.json")
        except Exception as e:
            logger.error(f"保存用户配置失败: {e}")

    def get_user(self, user_id: str, nick: Optional[str] = None) -> UserConfigItem:
        """获取用户配置，如果不存在则创建新的"""
        if user_id not in self.users:
            self.users[user_id] = UserConfigItem(nick=nick)
            self.save()
        elif nick and self.users[user_id].nick != nick:
            self.users[user_id].nick = nick
            self.save()
        return self.users[user_id]

    def update_user(self, user_id: str, **kwargs) -> None:
        """更新用户配置"""
        user_config = self.get_user(user_id)
        for key, value in kwargs.items():
            if hasattr(user_config, key):
                setattr(user_config, key, value)
        self.save()

    def record_chat(self, user_id: str) -> None:
        """记录聊天"""
        user_config = self.get_user(user_id)
        user_config.chat_alltimes += 1
        user_config.last_chattime = int(time.time())
        user_config.times = min(user_config.times + 1, user_config.all_times)
        self.save()

    def add_world_life(self, user_id: str, life: str) -> None:
        """添加世界线记录"""
        user_config = self.get_user(user_id)
        if life not in user_config.world_lifes:
            user_config.world_lifes.append(life)
            user_config.world_times += 1
            self.save()