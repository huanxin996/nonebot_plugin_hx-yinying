import json,os,time
from pathlib import Path
from typing import Dict, Any, Optional
from nonebot.log import logger
from .config import configs

current_dir = configs.plugin_cache_dir if configs.localstore_use_cwd else Path.cwd()
plugin_config_dir = current_dir / "data"
if not os.path.exists(plugin_config_dir):
    os.makedirs(plugin_config_dir)
logger.debug(f"当前插件存储路径为：{plugin_config_dir}")

class GlobalVars:
    """全局变量存储类，使用单例模式管理配置文件"""
    _instances: Dict[str, "GlobalVars"] = {}

    def __init__(self, filename: str = "global_vars.json"):
        """初始化实例属性"""
        self.data: Dict[str, Any] = {}
        self._is_loaded: bool = False
        self._storage_path: Path = plugin_config_dir / filename
        self._last_update: Dict[str, float] = {}

    def __new__(cls, filename: str = "global_vars.json"):
        """创建或获取实例"""
        if filename not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[filename] = instance
        return cls._instances[filename]

    @classmethod
    def get_instance(cls, filename: str = "global_vars.json") -> "GlobalVars":
        """获取指定文件的实例"""
        return cls(filename)

    def ensure_loaded(self) -> None:
        """确保数据已加载"""
        if not self._is_loaded:
            self._load_data()
            self._is_loaded = True

    def _load_data(self) -> None:
        """从文件加载数据"""
        try:
            if self._storage_path.exists():
                with open(self._storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
        except Exception as e:
            logger.error(f"加载数据失败 {self._storage_path}: {e}")

    def _save_data(self) -> None:
        """保存数据到文件"""
        try:
            self._storage_path.parent.mkdir(exist_ok=True)
            with open(self._storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存数据失败 {self._storage_path}: {e}")

    @classmethod
    def get(cls, key: str, filename: str = "global_vars.json", default: Any = None) -> Any:
        """获取配置值"""
        instance = cls.get_instance(filename)
        instance.ensure_loaded()
        
        expire_time = instance.data.get(f"{key}_expire")
        if expire_time and time.time() > expire_time:
            instance.delete(key)
            return default
            
        return instance.data.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any, filename: str = "global_vars.json", 
            expire: Optional[int] = None) -> None:
        """设置配置值"""
        instance = cls.get_instance(filename)
        instance.ensure_loaded()
        
        instance.data[key] = value
        instance._last_update[key] = time.time()
        
        if expire:
            instance.data[f"{key}_expire"] = time.time() + expire
            
        instance._save_data()

    @classmethod
    def delete(cls, key: str, filename: str = "global_vars.json") -> None:
        """删除配置值"""
        instance = cls.get_instance(filename)
        instance.ensure_loaded()
        
        instance.data.pop(key, None)
        instance.data.pop(f"{key}_expire", None)
        instance._last_update.pop(key, None)
        
        instance._save_data()

    @classmethod
    def clear_expired(cls, filename: str = "global_vars.json") -> None:
        """清理过期数据"""
        instance = cls.get_instance(filename)
        instance.ensure_loaded()
        
        current_time = time.time()
        expired_keys = [
            key[:-7] for key, expire_time in instance.data.items()
            if key.endswith('_expire') and current_time > expire_time
        ]
        
        for key in expired_keys:
            instance.delete(key)