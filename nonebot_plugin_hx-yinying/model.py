from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional
from .config import configs

class YinYingModelType(Enum):
    """模型类型枚举"""
    V1 = "yinyingllm-v1"
    V2 = "yinyingllm-v2"
    V3 = "yinyingllm-v3"
    CYBERFURRY = "cyberfurry-001"
    EASYCYBERFURRY = "easycyberfurry-001"

@dataclass
class CharacterSet:
    """角色卡设定"""
    cf_nickname: Optional[str] = None
    cf_species: Optional[str] = None
    cf_con_age: Optional[str] = None  # child, teen, adult, elder
    cf_con_style: Optional[str] = None  # normal, social_anxiety, etc
    cf_story: Optional[str] = None
    
    def to_dict(self) -> Optional[Dict[str, str]]:
        """转换为字典，忽略空值"""
        result = {}
        mapping = {
            'cf_nickname': 'cfNickname',
            'cf_species': 'cfSpecies',
            'cf_con_age': 'cfConAge',
            'cf_con_style': 'cfConStyle',
            'cf_story': 'cfStory'
        }
        
        for py_key, json_key in mapping.items():
            if value := getattr(self, py_key):
                result[json_key] = value
                
        return result if result else None

@dataclass
class YinYingMessage:
    """音音消息基础类"""
    app_id: str
    message: str
    model: YinYingModelType
    user_id: str
    nick_name: Optional[str] = None
    furry_character: Optional[str] = None
    prompt_patch: Optional[str] = None
    character_set: Optional[CharacterSet] = None
    chat_id: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.chat_id:
            self.chat_id = f"{self.app_id}-{self.user_id}"
            
    def to_dict(self) -> Dict:
        """转换为API请求字典，忽略空值"""
        data = {
            "appId": self.app_id,
            "chatId": self.chat_id,
            "model": self.model.value,
            "message": self.message,
        }
        
        variables = {}
        if self.nick_name:
            variables["nickName"] = self.nick_name
            
        if self.model == YinYingModelType.EASYCYBERFURRY:
            if self.furry_character:
                variables["furryCharacter"] = self.furry_character
                
        if self.model == YinYingModelType.V2 and self.prompt_patch:
            variables["promptPatch"] = self.prompt_patch
        elif self.model == YinYingModelType.CYBERFURRY and self.prompt_patch:
            variables["prompt"] = self.prompt_patch
            
        if variables:
            data["variables"] = variables
            
        if self.model == YinYingModelType.EASYCYBERFURRY and self.character_set:
            if char_data := self.character_set.to_dict():
                data["characterSet"] = char_data
                
        return data
    
    @classmethod
    def create(cls, 
               message: str,
               user_id: str,
               model: YinYingModelType = YinYingModelType.V3,
               app_id: str = configs.yinying_appid,
               nick_name: Optional[str] = None,
               furry_character: Optional[str] = None,
               prompt_patch: Optional[str] = None,
               character_set: Optional[CharacterSet] = None) -> "YinYingMessage":
        """创建消息实例的便捷方法"""
        return cls(
            app_id=app_id,
            message=message,
            model=model,
            user_id=user_id,
            nick_name=nick_name,
            furry_character=furry_character,
            prompt_patch=prompt_patch,
            character_set=character_set
        )

