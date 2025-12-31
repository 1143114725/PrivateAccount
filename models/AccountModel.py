from typing import Optional, List
from models.BaseModel import BaseModel


class AccountInfoModel:
    """账户信息模型"""
    
    def __init__(self, account_data: tuple):
        """
        初始化账户信息模型
        
        Args:
            account_data: 账户信息元组，从数据库返回的原始元组
        """
        # 数据库返回的account元组结构（长度4）：
        # 索引：0-id, 1-name, 2-balance, 3-user_id
        
        self.id = account_data[0]
        self.name = account_data[1]
        self.balance = account_data[2]
        self.user_id = account_data[3]
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            字典格式的账户信息
        """
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance,
            "user_id": self.user_id
        }
    
    def __repr__(self) -> str:
        """
        返回账户信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"AccountInfoModel(id={self.id}, name={self.name}, balance={self.balance}, user_id={self.user_id})"


class AccountResponseModel(BaseModel):
    """单个账户响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", account: Optional[AccountInfoModel] = None):
        """
        初始化单个账户响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            account: 账户信息模型
        """
        account_data = account.to_dict() if account else None
        super().__init__(errorcode, message, account_data)
    
    def __repr__(self) -> str:
        """
        返回单个账户响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"AccountResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class AccountsResponseModel(BaseModel):
    """多个账户响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", accounts: Optional[List[AccountInfoModel]] = None):
        """
        初始化多个账户响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息
            accounts: 账户信息模型列表
        """
        accounts_data = [account.to_dict() for account in accounts] if accounts else []
        super().__init__(errorcode, message, accounts_data)
    
    def __repr__(self) -> str:
        """
        返回多个账户响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"AccountsResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"