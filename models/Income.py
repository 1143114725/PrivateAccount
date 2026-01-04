from typing import Optional, List
from models.BaseModel import BaseModel


class IncomeInfoModel:
    """收入信息模型"""
    
    def __init__(self, income_data: tuple):
        """
        初始化收入信息模型
        
        Args:
            income_data: 收入信息元组，从数据库返回的原始元组
        """
        # 数据库返回的income元组结构（长度9）：
        # 索引：0-id, 1-money, 2-account_id, 3-user_id, 4-remark, 
        # 5-income_time, 6-create_time, 7-enable, 8-income_type_id
        
        self.id = income_data[0]
        self.money = income_data[1]
        self.account_id = income_data[2]
        self.user_id = income_data[3]
        self.remark = income_data[4]
        self.income_time = income_data[5]
        self.create_time = income_data[6]
        self.enable = income_data[7]
        self.income_type_id = income_data[8]
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的收入信息
        """
        return {
            "id": self.id,
            "money": self.money,
            "account_id": self.account_id,
            "user_id": self.user_id,
            "remark": self.remark,
            "income_time": self.income_time,
            "create_time": self.create_time,
            "enable": self.enable,
            "income_type_id": self.income_type_id
        }
    
    def __repr__(self) -> str:
        """
        返回收入信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomeInfoModel(id={self.id}, money={self.money}, account_id={self.account_id}, user_id={self.user_id}, remark={self.remark}, income_time={self.income_time}, create_time={self.create_time}, enable={self.enable}, income_type_id={self.income_type_id})"


class IncomeResponseModel(BaseModel):
    """单个收入响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", income: Optional[IncomeInfoModel] = None):
        """
        初始化单个收入响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            income: 收入信息模型
        """
        income_data = income.to_dict() if income else None
        super().__init__(errorcode, message, income_data)
    
    def __repr__(self) -> str:
        """
        返回单个收入响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomeResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class IncomesResponseModel(BaseModel):
    """多个收入响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", incomes: Optional[List[IncomeInfoModel]] = None):
        """
        初始化多个收入响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            incomes: 收入信息模型列表
        """
        incomes_data = [income.to_dict() for income in incomes] if incomes else []
        super().__init__(errorcode, message, incomes_data)
    
    def __repr__(self) -> str:
        """
        返回多个收入响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"IncomesResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
