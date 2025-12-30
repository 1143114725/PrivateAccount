class BaseModel:
    """API返回数据的基础模型类"""
    
    def __init__(self, errorcode: int, message: str = "", data: any = None):
        """
        初始化基础模型
        
        Args:
            errorcode: 错误码，200表示成功，其他表示不同的错误类型
            message: 响应消息，描述请求结果
            data: 响应数据
        """
        self.errorcode = errorcode
        self.message = message
        self.data = data
    
    def to_dict(self) -> dict:
        """
        转换为字典格式，用于JSON响应
        
        Returns:
            字典格式的响应数据
        """
        return {
            "errorcode": self.errorcode,
            "message": self.message,
            "data": self.data
        }
    
    def __repr__(self) -> str:
        """
        返回模型的字符串表示
        
        Returns:
            字符串表示
        """
        return f"BaseModel(errorcode={self.errorcode}, message={self.message}, data={self.data})"
