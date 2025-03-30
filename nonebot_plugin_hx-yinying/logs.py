import time
from dataclasses import dataclass, field
from typing import List, Dict
from .globalvar import GlobalVars,logger

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
class ChatLogs:
    """聊天记录管理类"""
    logs: Dict[str, List[ChatLogItem]] = field(default_factory=dict)
    
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
                # 初始化默认记录
                instance.add_log("114514", "幻歆", "初始化log记录")
            return instance
        except Exception as e:
            logger.error(f"加载聊天记录失败: {e}")
            instance = cls()
            instance.add_log("114514", "幻歆", "初始化log记录")
            return instance

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

    def add_log(self, user_id: str, rule: str, msg: str) -> None:
        """添加一条聊天记录"""
        if user_id not in self.logs:
            self.logs[user_id] = []
        log_item = ChatLogItem(rule=rule, msg=msg)
        self.logs[user_id].append(log_item)
        self.save()

    def get_logs(self, user_id: str, limit: int = 10) -> List[ChatLogItem]:
        """获取指定用户的聊天记录"""
        return self.logs.get(user_id, [])[-limit:]

    def clear_logs(self, user_id: str) -> None:
        """清空指定用户的聊天记录"""
        if user_id in self.logs:
            self.logs[user_id] = []
            self.save()

    def prune_old_logs(self, days: int = 7) -> None:
        """清理指定天数前的聊天记录"""
        cutoff_time = int(time.time()) - (days * 24 * 60 * 60)
        
        for user_id in self.logs:
            self.logs[user_id] = [
                log for log in self.logs[user_id]
                if log.timestamp > cutoff_time
            ]
        self.save()
