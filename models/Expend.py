from typing import Optional, List
from models.BaseModel import BaseModel
from utils.TimeUtils import TimeUtils


class ExpendInfoModel:
    """支出信息模型"""
    
    def __init__(self, expend_data: tuple):
        """
        初始化支出信息模型
        
        Args:
            expend_data: 支出信息元组，从数据库返回的原始元组
        """
        # 数据库返回的expend元组结构（长度9）：
        # 索引：0-id, 1-money, 2-account_id, 3-user_id, 4-remark, 
        # 5-expend_time, 6-create_time, 7-enable, 8-expend_type_id
        
        self.id = expend_data[0]
        self.money = expend_data[1]
        self.account_id = expend_data[2]
        self.user_id = expend_data[3]
        self.remark = expend_data[4]
        self.expend_time = expend_data[5]
        self.create_time = expend_data[6]
        self.enable = expend_data[7]
        self.expend_type_id = expend_data[8]
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的支出信息
        """
        return {
            "id": self.id,
            "money": self.money,
            "account_id": self.account_id,
            "user_id": self.user_id,
            "remark": self.remark,
            "expend_time": TimeUtils.database_time_to_milliseconds(self.expend_time),
            "create_time": TimeUtils.database_time_to_milliseconds(self.create_time),
            "enable": self.enable,
            "expend_type_id": self.expend_type_id
        }
    
    def __repr__(self) -> str:
        """
        返回支出信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendInfoModel(id={self.id}, money={self.money}, account_id={self.account_id}, user_id={self.user_id}, remark={self.remark}, expend_time={self.expend_time}, create_time={self.create_time}, enable={self.enable}, expend_type_id={self.expend_type_id})"


class ExpendResponseModel(BaseModel):
    """单个支出响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", expend: Optional[ExpendInfoModel] = None):
        """
        初始化单个支出响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            expend: 支出信息模型
        """
        expend_data = expend.to_dict() if expend else None
        super().__init__(errorcode, message, expend_data)
    
    def __repr__(self) -> str:
        """
        返回单个支出响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class ExpendsResponseModel(BaseModel):
    """多个支出响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", expends: Optional[List[ExpendInfoModel]] = None):
        """
        初始化多个支出响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            expends: 支出信息模型列表
        """
        expends_data = [expend.to_dict() for expend in expends] if expends else []
        super().__init__(errorcode, message, expends_data)
    
    def __repr__(self) -> str:
        """
        返回多个支出响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendsResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
