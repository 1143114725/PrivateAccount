from typing import Optional, List
from models.base_model import BaseModel


class ConsumptionInfoModel:
    """消费类型信息模型"""
    
    def __init__(self, consumption_data: tuple):
        """
        初始化消费类型信息模型
        
        Args:
            consumption_data: 消费类型信息元组，从数据库返回的原始元组
        """
        # 数据库返回的consumption元组结构（长度3）：
        # 索引：0-id, 1-type, 2-enable
        
        self.id = consumption_data[0]
        self.type = consumption_data[1]
        self.enable = consumption_data[2]
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的消费类型信息
        """
        return {
            "id": self.id,
            "type": self.type,
            "enable": self.enable
        }
    
    def __repr__(self) -> str:
        """
        返回消费类型信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ConsumptionInfoModel(id={self.id}, type={self.type}, enable={self.enable})"


class ConsumptionResponseModel(BaseModel):
    """单个消费类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", consumption: Optional[ConsumptionInfoModel] = None):
        """
        初始化单个消费类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            consumption: 消费类型信息模型
        """
        consumption_data = consumption.to_dict() if consumption else None
        super().__init__(errorcode, message, consumption_data)
    
    def __repr__(self) -> str:
        """
        返回单个消费类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ConsumptionResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class ConsumptionsResponseModel(BaseModel):
    """多个消费类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", consumptions: Optional[List[ConsumptionInfoModel]] = None):
        """
        初始化多个消费类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            consumptions: 消费类型信息模型列表
        """
        consumptions_data = [consumption.to_dict() for consumption in consumptions] if consumptions else []
        super().__init__(errorcode, message, consumptions_data)
    
    def __repr__(self) -> str:
        """
        返回多个消费类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"ConsumptionsResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
