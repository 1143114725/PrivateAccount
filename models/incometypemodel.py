from typing import Optional, List
from models.BaseModel import BaseModel


class IncomeTypeInfoModel:
    """收入类型信息模型"""
    
    def __init__(self, income_type_data: tuple):
        """
        初始化收入类型信息模型
        
        Args:
            income_type_data: 收入类型信息元组，从数据库返回的原始元组
        """
        # 数据库返回的income_type元组结构（长度4）：
        # 索引：0-id, 1-income_type_name, 2-create_time, 3-enable
        
        self.id = income_type_data[0]
        self.income_type_name = income_type_data[1]
        self.create_time = income_type_data[2] if len(income_type_data) > 2 else None
        self.enable = income_type_data[3] if len(income_type_data) > 3 else None
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的收入类型信息
        """
        return {
            "id": self.id,
            "income_type_name": self.income_type_name,
            "enable": self.enable,
            "create_time": self.create_time
        }
    
    def __repr__(self) -> str:
        """
        返回收入类型信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomeTypeInfoModel(id={self.id}, income_type_name={self.income_type_name}, enable={self.enable}, create_time={self.create_time})"


class IncomeTypeResponseModel(BaseModel):
    """单个收入类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", income_type: Optional[IncomeTypeInfoModel] = None):
        """
        初始化单个收入类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            income_type: 收入类型信息模型
        """
        income_type_data = income_type.to_dict() if income_type else None
        super().__init__(errorcode, message, income_type_data)
    
    def __repr__(self) -> str:
        """
        返回单个收入类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomeTypeResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class IncomeTypesResponseModel(BaseModel):
    """多个收入类型响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", income_types: Optional[List[IncomeTypeInfoModel]] = None):
        """
        初始化多个收入类型响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            income_types: 收入类型信息模型列表
        """
        income_types_data = [income_type.to_dict() for income_type in income_types] if income_types else []
        super().__init__(errorcode, message, income_types_data)
    
    def __repr__(self) -> str:
        """
        返回多个收入类型响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomeTypesResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
