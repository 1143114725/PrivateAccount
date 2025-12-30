from typing import Optional, List
from models.base_model import BaseModel


class ExpendTypeInfoModel:
    """消费类型信息模型"""
    
    def __init__(self, expend_type_data: tuple):
        """
        初始化消费类型信息模型
        
        Args:
            expend_type_data: 消费类型信息元组，从数据库返回的原始元组
        """
        # 数据库返回的expend_type元组结构（长度4）：
        # 索引：0-id, 1-expend_type_name, 2-enable, 3-create_time
        
        self.id = expend_type_data[0]
        self.expend_type_name = expend_type_data[1]
        self.enable = expend_type_data[2]
        self.create_time = expend_type_data[3] if len(expend_type_data) > 3 else None
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的消费类型信息
        """
        return {
            "id": self.id,
            "expend_type_name": self.expend_type_name,
            "enable": self.enable,
            "create_time": self.create_time
        }
    
    def __repr__(self) -> str:
        """
        返回消费类型信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendTypeInfoModel(id={self.id}, expend_type_name={self.expend_type_name}, enable={self.enable}, create_time={self.create_time})"


class ExpendTypeResponseModel(BaseModel):
    """单个消费类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", expend_type: Optional[ExpendTypeInfoModel] = None):
        """
        初始化单个消费类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            expend_type: 消费类型信息模型
        """
        expend_type_data = expend_type.to_dict() if expend_type else None
        super().__init__(errorcode, message, expend_type_data)
    
    def __repr__(self) -> str:
        """
        返回单个消费类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendTypeResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class ExpendTypesResponseModel(BaseModel):
    """多个消费类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", expend_types: Optional[List[ExpendTypeInfoModel]] = None):
        """
        初始化多个消费类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            expend_types: 消费类型信息模型列表
        """
        expend_types_data = [expend_type.to_dict() for expend_type in expend_types] if expend_types else []
        super().__init__(errorcode, message, expend_types_data)
    
    def __repr__(self) -> str:
        """
        返回多个消费类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ExpendTypesResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
