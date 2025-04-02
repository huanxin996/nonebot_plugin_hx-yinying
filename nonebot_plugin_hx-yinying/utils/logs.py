import time
from dataclasses import dataclass, field
from typing import List, Dict
from ..configs.globalvar import GlobalVars,logger

@dataclass
class ChatLogItem:
    """单条聊天记录"""
    rule: str
    msg: str
    timestamp: int = field(default_factory=lambda: int(time.time()))

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'rule': self.rule,
            'msg': self.msg,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ChatLogItem":
        """从字典创建实例"""
        return cls(
            rule=data.get('rule', ''),
            msg=data.get('msg', ''),
            timestamp=data.get('timestamp', int(time.time()))
        )

@dataclass
class UserChatCache:
    """用户聊天缓存"""
    user_id: str
    logs: List[ChatLogItem] = field(default_factory=list)
    last_update: float = field(default_factory=time.time)
    max_size: int = 100

    def add_log(self, log: ChatLogItem) -> None:
        """添加日志到缓存"""
        self.logs.append(log)
        if len(self.logs) > self.max_size:
            self.logs = self.logs[-self.max_size:]
        self.last_update = time.time()

    def clear(self) -> None:
        """清空缓存"""
        self.logs.clear()
        self.last_update = time.time()

    def is_expired(self, expire_time: int = 3600) -> bool:
        """检查缓存是否过期"""
        return time.time() - self.last_update > expire_time

    def get_recent(self, limit: int = 10) -> List[ChatLogItem]:
        """获取最近的记录"""
        return self.logs[-limit:]

# 缓存管理器
_global_cache: Dict[str, UserChatCache] = {}
    
def get_user_cache(user_id: str) -> UserChatCache:
    """获取用户缓存实例"""
    if user_id not in _global_cache:
        _global_cache[user_id] = UserChatCache(user_id=user_id)
    return _global_cache[user_id]

def clear_user_cache(user_id: str) -> None:
    """清空指定用户的缓存"""
    if user_id in _global_cache:
        _global_cache[user_id].clear()

def remove_user_cache(user_id: str) -> None:
    """移除指定用户的缓存实例"""
    _global_cache.pop(user_id, None)

def get_global_cache_count(user_id: str) -> int:
    """获取全局缓存中指定用户的记录数量"""
    if user_id in _global_cache:
        return len(_global_cache[user_id].logs) // 2
    return 0

@dataclass
class ChatLogs:
    """聊天记录管理类"""
    logs: Dict[str, List[ChatLogItem]] = field(default_factory=dict)
    _cache_expire: int = 3600  # 缓存过期时间(秒)

    @classmethod
    def load(cls) -> "ChatLogs":
        """加载聊天记录"""
        try:
            log_data = GlobalVars.get("chat_logs", "all_log.json", {})
            instance = cls()
            for user_id, history in log_data.items():
                instance.logs[user_id] = [
                    ChatLogItem.from_dict(item) if isinstance(item, dict) else item
                    for item in history
                ]
            if not instance.logs:
                instance.add_log("114514", "幻歆", "初始化log记录")
            return instance
        except Exception as e:
            logger.error(f"加载聊天记录失败: {e}")
            instance = cls()
            instance.add_log("114514", "幻歆", "初始化log记录")
            return instance

    def _get_cache(self, user_id: str) -> UserChatCache:
        """获取用户缓存"""
        cache = get_user_cache(user_id)
        if cache.is_expired(self._cache_expire):
            cache.clear()
        return cache
    def save(self) -> None:
        """保存聊天记录"""
        try:
            log_data = {
                user_id: [log.to_dict() for log in logs]
                for user_id, logs in self.logs.items()
            }
            GlobalVars.set("chat_logs", log_data, "all_log.json")
        except Exception as e:
            logger.error(f"保存聊天记录失败: {e}")

    def add_log(self, user_id: str, rule: str, msg: str, update_cache: bool = True) -> None:
        """添加一条聊天记录并更新缓存"""
        log_item = ChatLogItem(rule=rule, msg=msg)
        if user_id not in self.logs:
            self.logs[user_id] = []
        self.logs[user_id].append(log_item)
        if update_cache:
            cache = get_user_cache(user_id)
            if cache.is_expired(self._cache_expire):
                cache.clear()
            cache.add_log(log_item)
        self.save()

    def get_logs(self, user_id: str, limit: int = 32, use_cache: bool = True) -> List[ChatLogItem]:
        """获取指定用户的聊天记录"""
        if use_cache:
            cache = get_user_cache(user_id)
            if cache.is_expired(self._cache_expire):
                cache.clear()
            return cache.get_recent(limit)
        if user_id in self.logs:
            return self.logs[user_id][-limit:]
        return []
    
    def get_cache_count(self, user_id: str) -> int:
        """获取用户缓存中的记录数量"""
        return get_global_cache_count(user_id)

    def clear_logs(self, user_id: str, storage_type: str = "cache") -> None:
        """清空指定用户的聊天记录"""
        if storage_type in ("both", "main") and user_id in self.logs:
            self.logs[user_id] = []
            self.save()
            
        if storage_type in ("both", "cache"):
            clear_user_cache(user_id)

    def prune_old_logs(self, days: int = 7) -> None:
        """清理指定天数前的聊天记录"""
        cutoff_time = int(time.time()) - (days * 24 * 60 * 60)
        
        for user_id in self.logs:
            self.logs[user_id] = [
                log for log in self.logs[user_id]
                if log.timestamp > cutoff_time
            ]
        self.save()
