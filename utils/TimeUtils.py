import time
from datetime import datetime
from typing import Optional

class TimeUtils:
    """
    时间工具类，处理毫秒级时间戳与数据库时间类型的转换
    """
    
    @staticmethod
    def current_milliseconds() -> int:
        """
        获取当前时间的毫秒级时间戳
        
        Returns:
            int: 毫秒级时间戳
        """
        return int(time.time() * 1000)
    
    @staticmethod
    def milliseconds_to_datetime(milliseconds: int) -> datetime:
        """
        将毫秒级时间戳转换为datetime对象
        
        Args:
            milliseconds: 毫秒级时间戳
            
        Returns:
            datetime: datetime对象
        """
        return datetime.fromtimestamp(milliseconds / 1000)
    
    @staticmethod
    def datetime_to_milliseconds(dt: datetime) -> int:
        """
        将datetime对象转换为毫秒级时间戳
        
        Args:
            dt: datetime对象
            
        Returns:
            int: 毫秒级时间戳
        """
        return int(dt.timestamp() * 1000)
    
    @staticmethod
    def str_to_milliseconds(time_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> Optional[int]:
        """
        将时间字符串转换为毫秒级时间戳
        
        Args:
            time_str: 时间字符串
            format: 时间字符串的格式，默认为"%Y-%m-%d %H:%M:%S"
            
        Returns:
            Optional[int]: 毫秒级时间戳，如果转换失败返回None
        """
        try:
            dt = datetime.strptime(time_str, format)
            return TimeUtils.datetime_to_milliseconds(dt)
        except ValueError:
            return None
    
    @staticmethod
    def milliseconds_to_str(milliseconds: int, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        将毫秒级时间戳转换为时间字符串
        
        Args:
            milliseconds: 毫秒级时间戳
            format: 时间字符串的格式，默认为"%Y-%m-%d %H:%M:%S"
            
        Returns:
            str: 时间字符串
        """
        dt = TimeUtils.milliseconds_to_datetime(milliseconds)
        return dt.strftime(format)
    
    @staticmethod
    def database_time_to_milliseconds(db_time) -> Optional[int]:
        """
        将数据库返回的时间类型转换为毫秒级时间戳
        
        Args:
            db_time: 数据库返回的时间类型（可能是datetime对象或字符串）
            
        Returns:
            Optional[int]: 毫秒级时间戳，如果转换失败返回None
        """
        if db_time is None:
            return None
        
        if isinstance(db_time, datetime):
            return TimeUtils.datetime_to_milliseconds(db_time)
        elif isinstance(db_time, str):
            # 尝试自动解析常见的数据库时间字符串格式
            try:
                if '.' in db_time:
                    # 包含毫秒的格式
                    dt = datetime.strptime(db_time, "%Y-%m-%d %H:%M:%S.%f")
                else:
                    # 不包含毫秒的格式
                    dt = datetime.strptime(db_time, "%Y-%m-%d %H:%M:%S")
                return TimeUtils.datetime_to_milliseconds(dt)
            except ValueError:
                return None
        
        return None
    
    @staticmethod
    def milliseconds_to_database_time(milliseconds: int) -> datetime:
        """
        将毫秒级时间戳转换为数据库可用的datetime对象
        
        Args:
            milliseconds: 毫秒级时间戳
            
        Returns:
            datetime: datetime对象
        """
        return TimeUtils.milliseconds_to_datetime(milliseconds)
