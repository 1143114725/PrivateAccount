import configparser
import json
import os
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union

# 尝试导入可选依赖
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import toml
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False


class ConfigManager:
    """配置管理工具类，支持多种配置文件格式"""

    def __init__(self,
                 config_path: Union[str, List[str]] = None,
                 env_override: bool = False,
                 default_env: str = 'dev'):
        """
        初始化配置管理器

        :param config_path: 配置文件路径或路径列表
        :param env_override: 是否允许环境变量覆盖配置
        :param default_env: 默认环境
        """
        self.config_data: Dict[str, Any] = {}
        self.env_override = env_override
        self.default_env = default_env
        self.loaded_files: List[str] = []

        if config_path:
            if isinstance(config_path, str):
                self.load(config_path)
            elif isinstance(config_path, list):
                for path in config_path:
                    self.load(path)

    def load(self, config_path: str) -> 'ConfigManager':
        """
        加载配置文件

        :param config_path: 配置文件路径
        :return: 配置管理器实例（支持链式调用）
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        # 根据文件扩展名选择解析器
        ext = os.path.splitext(config_path)[1].lower()
        config_data = {}

        if ext == '.ini':
            config_data = self._parse_ini(config_path)
        elif ext == '.json':
            config_data = self._parse_json(config_path)
        elif ext == '.yaml' or ext == '.yml':
            if YAML_AVAILABLE:
                config_data = self._parse_yaml(config_path)
            else:
                raise ImportError("PyYAML库未安装，无法解析YAML文件")
        elif ext == '.toml':
            if TOML_AVAILABLE:
                config_data = self._parse_toml(config_path)
            else:
                raise ImportError("toml库未安装，无法解析TOML文件")
        elif ext == '.xml':
            config_data = self._parse_xml(config_path)
        else:
            raise ValueError(f"不支持的配置文件格式: {ext}")

        # 合并配置数据
        self._merge_config(self.config_data, config_data)
        self.loaded_files.append(config_path)

        # 应用环境变量覆盖
        if self.env_override:
            self._apply_env_override()

        return self

    def load_directory(self, dir_path: str, recursive: bool = False) -> 'ConfigManager':
        """
        加载目录下的所有配置文件

        :param dir_path: 目录路径
        :param recursive: 是否递归加载子目录
        :return: 配置管理器实例（支持链式调用）
        """
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"目录不存在: {dir_path}")

        supported_extensions = ['.ini', '.json', '.yaml', '.yml', '.toml', '.xml']

        for root, _, files in os.walk(dir_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    self.load(file_path)
            if not recursive:
                break

        return self

    def get(self, section: Optional[str] = None, key: Optional[str] = None, default: Any = None) -> Any:
        """
        获取配置值

        :param section: 配置节名
        :param key: 配置项名
        :param default: 默认值
        :return: 配置值
        """
        try:
            if section is None:
                return self.config_data
            
            if key is None:
                return self.config_data.get(section, default)

            return self.config_data[section][key]
        except (KeyError, TypeError):
            return default

    def getint(self, section: str, key: str, default: int = 0) -> int:
        """
        获取整数类型的配置值

        :param section: 配置节名
        :param key: 配置项名
        :param default: 默认值
        :return: 整数配置值
        """
        value = self.get(section, key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def getfloat(self, section: str, key: str, default: float = 0.0) -> float:
        """
        获取浮点数类型的配置值

        :param section: 配置节名
        :param key: 配置项名
        :param default: 默认值
        :return: 浮点数配置值
        """
        value = self.get(section, key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def getboolean(self, section: str, key: str, default: bool = False) -> bool:
        """
        获取布尔类型的配置值

        :param section: 配置节名
        :param key: 配置项名
        :param default: 默认值
        :return: 布尔配置值
        """
        value = self.get(section, key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        try:
            return bool(int(value))
        except (ValueError, TypeError):
            return default

    def set(self, section: str, key: str, value: Any) -> 'ConfigManager':
        """
        设置配置值

        :param section: 配置节名
        :param key: 配置项名
        :param value: 配置值
        :return: 配置管理器实例（支持链式调用）
        """
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value
        return self

    def has_section(self, section: str) -> bool:
        """
        检查是否存在指定配置节

        :param section: 配置节名
        :return: 是否存在
        """
        return section in self.config_data

    def add_section(self, section: str) -> 'ConfigManager':
        """
        添加配置节

        :param section: 配置节名
        :return: 配置管理器实例（支持链式调用）
        """
        if not self.has_section(section):
            self.config_data[section] = {}
        return self

    def remove_section(self, section: str) -> 'ConfigManager':
        """
        删除配置节

        :param section: 配置节名
        :return: 配置管理器实例（支持链式调用）
        """
        if self.has_section(section):
            del self.config_data[section]
        return self

    def validate(self, required_sections: List[str] = None, required_keys: Dict[str, List[str]] = None) -> bool:
        """
        验证配置

        :param required_sections: 必需的配置节列表
        :param required_keys: 必需的配置项字典，格式为{section: [key1, key2, ...]}
        :return: 是否验证通过
        """
        if required_sections:
            for section in required_sections:
                if not self.has_section(section):
                    raise ValueError(f"缺少必需的配置节: {section}")

        if required_keys:
            for section, keys in required_keys.items():
                if not self.has_section(section):
                    raise ValueError(f"缺少必需的配置节: {section}")
                for key in keys:
                    if key not in self.config_data[section]:
                        raise ValueError(f"配置节 {section} 缺少必需的配置项: {key}")

        return True

    def _parse_ini(self, file_path: str) -> Dict[str, Any]:
        """解析INI格式配置文件"""
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        return {section: dict(config[section]) for section in config.sections()}

    def _parse_json(self, file_path: str) -> Dict[str, Any]:
        """解析JSON格式配置文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _parse_yaml(self, file_path: str) -> Dict[str, Any]:
        """解析YAML格式配置文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def _parse_toml(self, file_path: str) -> Dict[str, Any]:
        """解析TOML格式配置文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

    def _parse_xml(self, file_path: str) -> Dict[str, Any]:
        """解析XML格式配置文件"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        result = {}

        def _parse_element(element: ET.Element, parent_dict: Dict[str, Any]):
            if len(element) == 0:
                parent_dict[element.tag] = element.text
            else:
                section = {}
                parent_dict[element.tag] = section
                for child in element:
                    _parse_element(child, section)

        _parse_element(root, result)
        return result

    def _merge_config(self, target: Dict[str, Any], source: Dict[str, Any]):
        """合并配置数据"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_config(target[key], value)
            else:
                target[key] = value

    def _apply_env_override(self):
        """应用环境变量覆盖"""
        for section, items in self.config_data.items():
            for key in items:
                env_key = f"{section.upper()}_{key.upper()}"
                if env_key in os.environ:
                    self.config_data[section][key] = os.environ[env_key]

    def __str__(self) -> str:
        """返回配置数据的字符串表示"""
        return str(self.config_data)

    def __repr__(self) -> str:
        """返回配置管理器的表示"""
        return f"ConfigManager(config_data={self.config_data}, env_override={self.env_override})"
