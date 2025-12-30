from typing import Optional
from models.base_model import BaseModel


class UserInfoModel:
    """用户信息模型"""
    
    def __init__(self, user_data: tuple):
        """
        初始化用户信息模型
        
        Args:
            user_data: 用户信息元组，可以是直接从数据库返回的原始元组或从UserService返回的带有额外token信息的元组
        """
        # 从数据库直接返回的原始user元组结构（长度9）：
        # 索引：0-id, 1-username, 2-password, 3-phone, 4-refresh_token, 5-token_expiration_time, 6-registration, 7-enable, 8-last_login_time
        
        # 从UserService返回的user_with_token元组结构（长度11）：
        # 索引：0-id, 1-username, 2-password, 3-phone, 4-refresh_token, 5-token_expiration_time, 6-registration, 7-enable, 8-last_login_time, 9-new_token, 10-new_token_expiration_time
        
        self.id = user_data[0]
        self.username = user_data[1]
        self.phone = user_data[3]
        self.enable = bool(user_data[7])  # enable在user表中的实际索引是7，转换为布尔值
        self.registration = user_data[6]  # registration在user表中的实际索引是6
        
        # 检查user_data的长度，判断是原始元组还是带有新token信息的元组
        if len(user_data) == 11:  # user_with_token元组
            # 使用新生成的token信息
            self.token = user_data[9]
            self.token_expiration_time = user_data[10]
        else:  # 原始user元组
            # 使用数据库中的token信息
            self.token = user_data[4]  # refresh_token在user表中的实际索引是4
            self.token_expiration_time = user_data[5]  # token_expiration_time在user表中的实际索引是5
    
    def to_dict(self, include_registration: bool = False) -> dict:
        """
        转换为字典格式
        
        Args:
            include_registration: 是否包含registration字段，默认不包含
            
        Returns:
            字典格式的用户信息
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "phone": self.phone,
            "enable": self.enable,
            "token": self.token,
            "token_expiration_time": self.token_expiration_time
        }
        
        # 根据参数决定是否包含registration字段
        if include_registration:
            user_dict["registration"] = self.registration
            
        return user_dict
    
    def __repr__(self) -> str:
        """
        返回用户信息的字符串表示
        
        Returns:
            字符串表示
        """
        return f"UserInfoModel(id={self.id}, username={self.username}, phone={self.phone})"


class LoginResponseModel(BaseModel):
    """登录响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", user: Optional[UserInfoModel] = None):
        """
        初始化登录响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 登录消息
            user: 用户信息模型
        """
        user_data = user.to_dict() if user else None
        super().__init__(errorcode, message, user_data)
    
    def __repr__(self) -> str:
        """
        返回登录响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"LoginResponseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"


class RegisterResponseModel(BaseModel):
    """注册响应模型"""
    
    def __init__(self, errorcode: int, message: str = "", user_info: tuple = None):
        """
        初始化注册响应模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 注册消息
            user_info: 用户信息元组 (id, username, phone, registration)
        """
        if user_info:
            data = {
                "id": user_info[0],
                "username": user_info[1],
                "phone": user_info[2],
                "registration": user_info[3]
            }
        else:
            data = None
            
        super().__init__(errorcode, message, data)
    
    def __repr__(self) -> str:
        """
        返回注册响应的字符串表示
        
        Returns:
            字符串表示
        """
        return f"RegisterResponseModel(errorcode={self.errorcode}, message={self.message})"
