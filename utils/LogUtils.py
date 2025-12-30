import logging
import os
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler, SocketHandler, DatagramHandler
from typing import Dict, Any, Optional, List, Callable
from utils.ConfigManager import ConfigManager


class ContentFilter(logging.Filter):
    """自定义内容过滤器"""
    
    def __init__(self, include_keywords: Optional[List[str]] = None, exclude_keywords: Optional[List[str]] = None):
        """
        初始化内容过滤器
        
        :param include_keywords: 只包含这些关键词的日志才会被记录
        :param exclude_keywords: 包含这些关键词的日志会被过滤掉
        """
        super().__init__()
        self.include_keywords = include_keywords or []
        self.exclude_keywords = exclude_keywords or []
    
    def filter(self, record):
        """
        过滤日志记录
        
        :param record: 日志记录对象
        :return: 是否保留该日志记录
        """
        message = str(record.getMessage())
        
        # 先检查是否需要排除
        for keyword in self.exclude_keywords:
            if keyword.lower() in message.lower():
                return False
        
        # 如果没有包含关键词要求，则保留所有不被排除的日志
        if not self.include_keywords:
            return True
        
        # 检查是否包含要求的关键词
        for keyword in self.include_keywords:
            if keyword.lower() in message.lower():
                return True
        
        return False


class ModuleFilter(logging.Filter):
    """模块过滤器"""
    
    def __init__(self, include_modules: Optional[List[str]] = None, exclude_modules: Optional[List[str]] = None):
        """
        初始化模块过滤器
        
        :param include_modules: 只包含这些模块的日志才会被记录
        :param exclude_modules: 包含这些模块的日志会被过滤掉
        """
        super().__init__()
        self.include_modules = include_modules or []
        self.exclude_modules = exclude_modules or []
    
    def filter(self, record):
        """
        过滤日志记录
        
        :param record: 日志记录对象
        :return: 是否保留该日志记录
        """
        module_name = record.module
        
        # 先检查是否需要排除
        for module in self.exclude_modules:
            if module in module_name:
                return False
        
        # 如果没有包含模块要求，则保留所有不被排除的日志
        if not self.include_modules:
            return True
        
        # 检查是否包含要求的模块
        for module in self.include_modules:
            if module in module_name:
                return True
        
        return False


class LogUtils:
    """日志工具类"""
    
    # 日志级别映射
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    # 日志格式
    LOG_FORMATS = {
        'simple': '%(levelname)s - %(message)s',
        'standard': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    }
    
    def __init__(self, name: str = __name__, config_file: str = 'config/LogConfig.ini'):
        """
        初始化日志工具
        
        :param name: 日志名称
        :param config_file: 配置文件路径
        """
        self.name = name
        self.config_file = config_file
        self.logger = logging.getLogger(name)
        self.config = None
        
        # 加载配置
        self._load_config()
        
        # 初始化日志器
        self._init_logger()
    
    def _load_config(self):
        """加载日志配置"""
        try:
            self.config = ConfigManager(self.config_file)
        except Exception as e:
            # 如果加载配置文件失败，使用默认配置
            print(f"加载配置文件失败: {e}")
            self.config = None
    
    def _init_logger(self):
        """初始化日志器"""
        # 获取日志级别
        log_level = self._get_config_value('logging', 'level', 'INFO')
        log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
        
        # 设置日志级别
        self.logger.setLevel(log_level)
        
        # 清除已有的处理器
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 配置控制台输出
        if self._get_config_value('logging', 'console_enabled', 'true').lower() == 'true':
            self._add_console_handler()
        
        # 配置文件输出
        if self._get_config_value('logging', 'file_enabled', 'true').lower() == 'true':
            self._add_file_handler()
        
        # 配置邮件通知
        if self._get_config_value('logging', 'email_enabled', 'false').lower() == 'true':
            self._add_email_handler()
        
        # 配置网络输出
        if self._get_config_value('logging', 'network_enabled', 'false').lower() == 'true':
            self._add_network_handler()
    
    def _add_console_handler(self):
        """添加控制台处理器"""
        handler = logging.StreamHandler(sys.stdout)
        
        # 设置日志格式
        log_format = self._get_config_value('logging', 'console_format', 'standard')
        formatter = logging.Formatter(self.LOG_FORMATS.get(log_format, self.LOG_FORMATS['standard']))
        handler.setFormatter(formatter)
        
        # 设置日志级别
        log_level = self._get_config_value('logging', 'console_level', 'INFO')
        log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
        handler.setLevel(log_level)
        
        # 添加过滤器
        self._add_filters(handler)
        
        self.logger.addHandler(handler)
    
    def _add_file_handler(self):
        """添加文件处理器"""
        # 获取日志文件路径
        log_dir = self._get_config_value('logging', 'file_dir', 'logs')
        log_filename = self._get_config_value('logging', 'file_name', 'app.log')
        log_path = os.path.join(log_dir, log_filename)
        
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 获取日志轮转配置
        rotate_type = self._get_config_value('logging', 'rotate_type', 'size')  # size或time
        
        if rotate_type == 'size':
            # 按大小轮转
            max_bytes = int(self._get_config_value('logging', 'max_bytes', '10485760'))  # 默认10MB
            backup_count = int(self._get_config_value('logging', 'backup_count', '5'))  # 默认保留5个文件
            handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
        else:
            # 按时间轮转
            when = self._get_config_value('logging', 'rotate_when', 'D')  # D=天, H=小时, M=分钟, S=秒
            interval = int(self._get_config_value('logging', 'rotate_interval', '1'))  # 默认每天轮转
            backup_count = int(self._get_config_value('logging', 'backup_count', '7'))  # 默认保留7天
            handler = TimedRotatingFileHandler(log_path, when=when, interval=interval, backupCount=backup_count, encoding='utf-8')
        
        # 设置日志格式
        log_format = self._get_config_value('logging', 'file_format', 'detailed')
        formatter = logging.Formatter(self.LOG_FORMATS.get(log_format, self.LOG_FORMATS['detailed']))
        handler.setFormatter(formatter)
        
        # 设置日志级别
        log_level = self._get_config_value('logging', 'file_level', 'INFO')
        log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
        handler.setLevel(log_level)
        
        # 添加过滤器
        self._add_filters(handler)
        
        self.logger.addHandler(handler)
    
    def _add_email_handler(self):
        """添加邮件处理器"""
        try:
            # 获取邮件配置
            mail_host = self._get_config_value('logging', 'email_host')
            mail_port = int(self._get_config_value('logging', 'email_port', '587'))
            mail_username = self._get_config_value('logging', 'email_username')
            mail_password = self._get_config_value('logging', 'email_password')
            mail_from = self._get_config_value('logging', 'email_from')
            mail_to = self._get_config_value('logging', 'email_to')
            mail_subject = self._get_config_value('logging', 'email_subject', '应用程序错误日志')
            
            if not all([mail_host, mail_username, mail_password, mail_from, mail_to]):
                print("邮件配置不完整，跳过邮件处理器配置")
                return
            
            # 创建邮件处理器
            handler = SMTPHandler(
                mailhost=(mail_host, mail_port),
                fromaddr=mail_from,
                toaddrs=mail_to.split(','),
                subject=mail_subject,
                credentials=(mail_username, mail_password),
                secure=()
            )
            
            # 设置日志格式
            log_format = self._get_config_value('logging', 'email_format', 'detailed')
            formatter = logging.Formatter(self.LOG_FORMATS.get(log_format, self.LOG_FORMATS['detailed']))
            handler.setFormatter(formatter)
            
            # 设置日志级别（通常只发送ERROR和CRITICAL级别的日志）
            log_level = self._get_config_value('logging', 'email_level', 'ERROR')
            log_level = self.LOG_LEVELS.get(log_level.upper(), logging.ERROR)
            handler.setLevel(log_level)
            
            # 添加过滤器
            self._add_filters(handler)
            
            self.logger.addHandler(handler)
        except Exception as e:
            print(f"配置邮件处理器失败: {e}")
    
    def _add_network_handler(self):
        """添加网络处理器"""
        try:
            # 获取网络配置
            network_protocol = self._get_config_value('logging', 'network_protocol', 'tcp').lower()
            network_host = self._get_config_value('logging', 'network_host', 'localhost')
            network_port = int(self._get_config_value('logging', 'network_port', '514'))
            
            # 创建网络处理器
            if network_protocol == 'udp':
                handler = DatagramHandler(network_host, network_port)
            else:  # 默认使用TCP
                handler = SocketHandler(network_host, network_port)
            
            # 设置日志格式
            log_format = self._get_config_value('logging', 'network_format', 'standard')
            formatter = logging.Formatter(self.LOG_FORMATS.get(log_format, self.LOG_FORMATS['standard']))
            handler.setFormatter(formatter)
            
            # 设置日志级别
            log_level = self._get_config_value('logging', 'network_level', 'INFO')
            log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
            handler.setLevel(log_level)
            
            # 添加过滤器
            self._add_filters(handler)
            
            self.logger.addHandler(handler)
        except Exception as e:
            print(f"配置网络处理器失败: {e}")
    
    def _add_filters(self, handler):
        """为处理器添加过滤器"""
        # 添加内容过滤器
        include_keywords = self._get_config_value('logging', 'include_keywords', '')
        exclude_keywords = self._get_config_value('logging', 'exclude_keywords', '')
        
        if include_keywords or exclude_keywords:
            include_list = [kw.strip() for kw in include_keywords.split(',') if kw.strip()]
            exclude_list = [kw.strip() for kw in exclude_keywords.split(',') if kw.strip()]
            content_filter = ContentFilter(include_list, exclude_list)
            handler.addFilter(content_filter)
        
        # 添加模块过滤器
        include_modules = self._get_config_value('logging', 'include_modules', '')
        exclude_modules = self._get_config_value('logging', 'exclude_modules', '')
        
        if include_modules or exclude_modules:
            include_list = [mod.strip() for mod in include_modules.split(',') if mod.strip()]
            exclude_list = [mod.strip() for mod in exclude_modules.split(',') if mod.strip()]
            module_filter = ModuleFilter(include_list, exclude_list)
            handler.addFilter(module_filter)
    
    def _get_config_value(self, section: str, key: str, default: str = '') -> str:
        """
        获取配置值
        
        :param section: 配置节
        :param key: 配置项
        :param default: 默认值
        :return: 配置值
        """
        if self.config is not None:
            return self.config.get('logging', key, default)
        return default
    
    def debug(self, msg: str, *args, **kwargs):
        """记录DEBUG级别的日志"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """记录INFO级别的日志"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """记录WARNING级别的日志"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """记录ERROR级别的日志"""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """记录CRITICAL级别的日志"""
        self.logger.critical(msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, **kwargs):
        """记录异常信息"""
        self.logger.exception(msg, *args, **kwargs)
    
    def set_level(self, level: str):
        """
        设置日志级别
        
        :param level: 日志级别
        """
        log_level = self.LOG_LEVELS.get(level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
    
    def get_logger(self) -> logging.Logger:
        """
        获取原始日志器
        
        :return: logging.Logger实例
        """
        return self.logger
    
    def add_filter(self, filter_obj: logging.Filter):
        """
        添加自定义过滤器到所有处理器
        
        :param filter_obj: logging.Filter实例
        """
        # 添加到logger本身
        self.logger.addFilter(filter_obj)
        
        # 添加到所有处理器
        for handler in self.logger.handlers:
            handler.addFilter(filter_obj)
    
    def add_content_filter(self, include_keywords: Optional[List[str]] = None, exclude_keywords: Optional[List[str]] = None):
        """
        添加内容过滤器
        
        :param include_keywords: 只包含这些关键词的日志才会被记录
        :param exclude_keywords: 包含这些关键词的日志会被过滤掉
        """
        filter_obj = ContentFilter(include_keywords, exclude_keywords)
        self.add_filter(filter_obj)
    
    def add_module_filter(self, include_modules: Optional[List[str]] = None, exclude_modules: Optional[List[str]] = None):
        """
        添加模块过滤器
        
        :param include_modules: 只包含这些模块的日志才会被记录
        :param exclude_modules: 包含这些模块的日志会被过滤掉
        """
        filter_obj = ModuleFilter(include_modules, exclude_modules)
        self.add_filter(filter_obj)
    
    @staticmethod
    def get_instance(name: str = __name__, config_file: str = 'config/LogConfig.ini') -> 'LogUtils':
        """
        获取日志工具实例（单例模式）
        
        :param name: 日志名称
        :param config_file: 配置文件路径
        :return: LogUtils实例
        """
        if not hasattr(LogUtils, '_instances'):
            LogUtils._instances = {}
        
        key = f"{name}_{config_file}"
        if key not in LogUtils._instances:
            LogUtils._instances[key] = LogUtils(name, config_file)
        
        return LogUtils._instances[key]
