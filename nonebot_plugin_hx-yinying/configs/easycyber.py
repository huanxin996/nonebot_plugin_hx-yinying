from dataclasses import dataclass, field
from typing import Optional, List, Dict
from .globalvar import GlobalVars,logger,time

@dataclass
class EasyCyberCharacter:
    """easycyber角色定义"""
    cf_nickname: str
    cf_species: str 
    cf_con_age: str
    cf_con_style: str
    cf_story: str
    public: bool = True
    creator: int = 3485462167
    create_time: int = field(default_factory=lambda: int(time.time()))
    last_update: int = field(default_factory=lambda: int(time.time()))
    id: int = 0

    def to_dict(self) -> dict:
        """转换为接口格式的字典"""
        return {
            "cfNickname": self.cf_nickname,
            "cfSpecies": self.cf_species,
            "cfConAge": self.cf_con_age,
            "cfConStyle": self.cf_con_style,
            "cfStory": self.cf_story,
            "public": self.public,
            "creator": self.creator,
            "create_time": self.create_time,
            "last_update": self.last_update,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EasyCyberCharacter":
        """从字典创建实例"""
        return cls(
            cf_nickname=data.get("cfNickname", ""),
            cf_species=data.get("cfSpecies", ""),
            cf_con_age=data.get("cfConAge", "child"),
            cf_con_style=data.get("cfConStyle", "social_anxiety"),
            cf_story=data.get("cfStory", ""),
            public=data.get("public", True),
            creator=data.get("creator", 3485462167),
            create_time=data.get("create_time", int(time.time())),
            last_update=data.get("last_update", int(time.time())),
            id=data.get("id", 0)
        )

@dataclass
class EasyCyberManager:
    """easycyber角色管理器"""
    characters: Dict[str, EasyCyberCharacter] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "EasyCyberManager":
        """加载配置"""
        try:
            data = GlobalVars.get("easycyber", "easycyber.json", {})
            instance = cls()
            if not data:
                default_char = EasyCyberCharacter(
                    cf_nickname="Hx",
                    cf_species="龙狼",
                    cf_con_age="child",
                    cf_con_style="sentiment",
                    cf_story="相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。"
                )
                instance.add_character("Hx", default_char)
                return instance
            for nick, char_data in data.items():
                try:
                    instance.characters[nick] = EasyCyberCharacter.from_dict(char_data)
                except Exception as e:
                    logger.error(f"加载角色 {nick} 失败: {e}")
            return instance
        except Exception as e:
            logger.error(f"加载赛博角色配置失败: {e}")
            return cls()

    def save(self) -> None:
        """保存配置"""
        try:
            data = {
                nick: char.to_dict()
                for nick, char in self.characters.items()
            }
            GlobalVars.set("easycyber", data, "easycyber.json")
        except Exception as e:
            logger.error(f"保存赛博角色配置失败: {e}")

    def get_character(self, nickname: str) -> Optional[EasyCyberCharacter]:
        """获取指定角色"""
        return self.characters.get(nickname)

    def add_character(self, nickname: str, character: EasyCyberCharacter) -> bool:
        """添加新角色"""
        if nickname not in self.characters:
            character.id = len(self.characters)
            self.characters[nickname] = character
            self.save()
            return True
        return False

    def update_character(self, nickname: str, **kwargs) -> bool:
        """更新角色信息"""
        if char := self.get_character(nickname):
            for key, value in kwargs.items():
                if hasattr(char, key):
                    setattr(char, key, value)
            char.last_update = int(time.time())
            self.save()
            return True
        return False

    def create_character(self, nickname: str, **kwargs) -> Optional[EasyCyberCharacter]:
        """创建新角色"""
        if nickname in self.characters:
            return None
            
        char = EasyCyberCharacter(
            cf_nickname=nickname,
            cf_species=kwargs.get("species", "未知"),
            cf_con_age=kwargs.get("con_age", "child"),
            cf_con_style=kwargs.get("con_style", "social_anxiety"),
            cf_story=kwargs.get("story", ""),
            creator=kwargs.get("creator", 3485462167)
        )
        
        if self.add_character(nickname, char):
            return char
        return None

@dataclass
class EasyCyberContribution(EasyCyberCharacter):
    """投稿角色定义"""
    check_status: bool = False  # 审核状态
    contributor: Optional[int] = None  # 投稿者ID
    check_time: Optional[int] = None  # 审核时间
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        data = super().to_dict()
        data.update({
            "check_status": self.check_status,
            "contributor": self.contributor,
            "check_time": self.check_time
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "EasyCyberContribution":
        """从字典创建实例"""
        return cls(
            cf_nickname=data.get("cfNickname", ""),
            cf_species=data.get("cfSpecies", ""),
            cf_con_age=data.get("cfConAge", "child"),
            cf_con_style=data.get("cfConStyle", "social_anxiety"),
            cf_story=data.get("cfStory", ""),
            public=data.get("public", True),
            creator=data.get("creator", 3485462167),
            create_time=data.get("create_time", int(time.time())),
            last_update=data.get("last_update", int(time.time())),
            id=data.get("id", 0),
            check_status=data.get("check_status", False),
            contributor=data.get("contributor"),
            check_time=data.get("check_time")
        )

@dataclass
class EasyCyberContributionManager:
    """easycyber投稿角色管理器"""
    contributions: Dict[str, EasyCyberContribution] = field(default_factory=dict)
    
    @classmethod
    def load(cls) -> "EasyCyberContributionManager":
        """加载投稿配置"""
        try:
            data = GlobalVars.get("easycyber_tg", "easycyber_tg.json", {})
            instance = cls()
            
            # 如果数据为空，创建默认角色
            if not data:
                default_char = EasyCyberContribution(
                    cf_nickname="保留查询",
                    cf_species="狼龙",
                    cf_con_age="child",
                    cf_con_style="social_anxiety",
                    cf_story="你的名字叫Hx,相传Hx诞生于幻歆的幻梦破碎之歆中，是终结和新生的象征。",
                    check_status=True
                )
                instance.add_contribution("保留查询", default_char)
                return instance
            
            # 加载现有角色
            for nick, char_data in data.items():
                try:
                    instance.contributions[nick] = EasyCyberContribution.from_dict(char_data)
                except Exception as e:
                    logger.error(f"加载投稿角色 {nick} 失败: {e}")
                    
            return instance
            
        except Exception as e:
            logger.error(f"加载投稿角色配置失败: {e}")
            return cls()
    
    def save(self) -> None:
        """保存配置"""
        try:
            data = {
                nick: char.to_dict()
                for nick, char in self.contributions.items()
            }
            GlobalVars.set("easycyber_tg", data, "easycyber_tg.json")
        except Exception as e:
            logger.error(f"保存投稿角色配置失败: {e}")
    
    def get_contribution(self, nickname: str) -> Optional[EasyCyberContribution]:
        """获取指定投稿角色"""
        return self.contributions.get(nickname)
    
    def add_contribution(self, nickname: str, character: EasyCyberContribution) -> bool:
        """添加新投稿角色"""
        if nickname not in self.contributions:
            character.id = len(self.contributions)
            self.contributions[nickname] = character
            self.save()
            return True
        return False
    
    def submit_contribution(self, nickname: str, contributor_id: int, **kwargs) -> Optional[EasyCyberContribution]:
        """提交新投稿"""
        if nickname in self.contributions:
            return None
            
        char = EasyCyberContribution(
            cf_nickname=nickname,
            cf_species=kwargs.get("species", "未知"),
            cf_con_age=kwargs.get("con_age", "child"),
            cf_con_style=kwargs.get("con_style", "social_anxiety"),
            cf_story=kwargs.get("story", ""),
            creator=kwargs.get("creator", contributor_id),
            contributor=contributor_id,
            check_status=False
        )
        
        if self.add_contribution(nickname, char):
            return char
        return None
    
    def check_contribution(self, nickname: str, status: bool = True) -> bool:
        """审核投稿"""
        if char := self.get_contribution(nickname):
            char.check_status = status
            char.check_time = int(time.time())
            self.save()
            return True
        return False
    
    def get_pending_contributions(self) -> List[EasyCyberContribution]:
        """获取待审核的投稿"""
        return [
            char for char in self.contributions.values()
            if not char.check_status
        ]
    
    def get_checked_contributions(self) -> List[EasyCyberContribution]:
        """获取已审核的投稿"""
        return [
            char for char in self.contributions.values()
            if char.check_status
        ]




