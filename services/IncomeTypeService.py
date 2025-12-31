from dao.IncomeTypeDAO import IncomeTypeDAO
from utils.LogUtils import LogUtils


class IncomeTypeService:
    """
    收入类型业务逻辑层，处理收入类型相关的业务规则
    """
    
    logger = LogUtils.get_instance('IncomeTypeService')
    
    def __init__(self):
        """
        初始化IncomeTypeService，创建IncomeTypeDAO实例
        """
        IncomeTypeService.logger.info("初始化IncomeTypeService")
        self.income_type_dao = IncomeTypeDAO()
    
    def create_income_type(self, income_type_name, enable=True):
        """
        创建新收入类型业务逻辑
        
        Args:
            income_type_name: 收入类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            tuple: (是否成功, 消息, 收入类型信息)
        """
        IncomeTypeService.logger.info(f"创建收入类型请求 - 类型名称: {income_type_name}, 启用: {enable}")
        
        # 参数验证
        if not income_type_name:
            IncomeTypeService.logger.warning("创建收入类型失败: 收入类型说明不能为空")
            return False, "收入类型说明不能为空", None
        
        # 调用DAO创建收入类型
        success, income_type_id = self.income_type_dao.create_income_type(income_type_name, enable)
        if success:
            # 获取创建的收入类型信息
            income_type = self.income_type_dao.get_income_type_by_id(income_type_id)
            if income_type:
                IncomeTypeService.logger.info(f"收入类型创建成功 - 收入类型ID: {income_type_id}, 类型名称: {income_type_name}")
                return True, "收入类型创建成功", income_type
            else:
                IncomeTypeService.logger.error(f"收入类型创建成功但无法获取收入类型信息 - 收入类型ID: {income_type_id}")
                return True, "收入类型创建成功但无法获取收入类型信息", None
        else:
            IncomeTypeService.logger.error(f"收入类型创建失败 - 类型名称: {income_type_name}")
            return False, "收入类型创建失败", None
    
    def update_income_type(self, income_type_id, income_type_name=None, enable=None):
        """
        修改收入类型信息业务逻辑
        
        Args:
            income_type_id: 收入类型ID
            income_type_name: 收入类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            tuple: (是否成功, 消息, 收入类型信息)
        """
        IncomeTypeService.logger.info(f"修改收入类型请求 - 收入类型ID: {income_type_id}, 类型名称: {income_type_name}, 启用: {enable}")
        
        # 参数验证
        if not income_type_id:
            IncomeTypeService.logger.warning("修改收入类型失败: 收入类型ID不能为空")
            return False, "收入类型ID不能为空", None
        
        if income_type_name is None and enable is None:
            IncomeTypeService.logger.warning("修改收入类型失败: 未提供任何更新字段")
            return False, "未提供任何更新字段", None
        
        # 检查收入类型是否存在
        income_type = self.income_type_dao.get_income_type_by_id(income_type_id)
        if not income_type:
            IncomeTypeService.logger.warning(f"修改收入类型失败: 收入类型不存在 - 收入类型ID: {income_type_id}")
            return False, "收入类型不存在", None
        
        # 调用DAO修改收入类型
        if self.income_type_dao.update_income_type(income_type_id, income_type_name, enable):
            # 获取更新后的收入类型信息
            updated_income_type = self.income_type_dao.get_income_type_by_id(income_type_id)
            IncomeTypeService.logger.info(f"收入类型修改成功 - 收入类型ID: {income_type_id}")
            return True, "收入类型修改成功", updated_income_type
        else:
            IncomeTypeService.logger.error(f"收入类型修改失败 - 收入类型ID: {income_type_id}")
            return False, "收入类型修改失败", None
    
    def delete_income_type(self, income_type_id):
        """
        删除收入类型业务逻辑
        
        Args:
            income_type_id: 收入类型ID
            
        Returns:
            tuple: (是否成功, 消息)
        """
        IncomeTypeService.logger.info(f"删除收入类型请求 - 收入类型ID: {income_type_id}")
        
        # 参数验证
        if not income_type_id:
            IncomeTypeService.logger.warning("删除收入类型失败: 收入类型ID不能为空")
            return False, "收入类型ID不能为空"
        
        # 检查收入类型是否存在
        income_type = self.income_type_dao.get_income_type_by_id(income_type_id)
        if not income_type:
            IncomeTypeService.logger.warning(f"删除收入类型失败: 收入类型不存在 - 收入类型ID: {income_type_id}")
            return False, "收入类型不存在"
        
        # 调用DAO删除收入类型
        if self.income_type_dao.delete_income_type(income_type_id):
            IncomeTypeService.logger.info(f"收入类型删除成功 - 收入类型ID: {income_type_id}")
            return True, "收入类型删除成功"
        else:
            IncomeTypeService.logger.error(f"收入类型删除失败 - 收入类型ID: {income_type_id}")
            return False, "收入类型删除失败"
    
    def get_income_type_by_id(self, income_type_id):
        """
        根据收入类型ID查询收入类型业务逻辑
        
        Args:
            income_type_id: 收入类型ID
            
        Returns:
            tuple: (是否成功, 消息, 收入类型信息)
        """
        IncomeTypeService.logger.info(f"查询收入类型请求 - 收入类型ID: {income_type_id}")
        
        # 参数验证
        if not income_type_id:
            IncomeTypeService.logger.warning("查询收入类型失败: 收入类型ID不能为空")
            return False, "收入类型ID不能为空", None
        
        # 调用DAO查询收入类型
        income_type = self.income_type_dao.get_income_type_by_id(income_type_id)
        if income_type:
            IncomeTypeService.logger.info(f"查询收入类型成功 - 收入类型ID: {income_type_id}")
            return True, "查询收入类型成功", income_type
        else:
            IncomeTypeService.logger.warning(f"查询收入类型失败: 收入类型不存在 - 收入类型ID: {income_type_id}")
            return False, "收入类型不存在", None
    
    def get_all_income_types(self):
        """
        查询所有收入类型业务逻辑
        
        Returns:
            tuple: (是否成功, 消息, 收入类型列表)
        """
        IncomeTypeService.logger.info("查询所有收入类型请求")
        
        # 调用DAO查询所有收入类型
        income_types = self.income_type_dao.get_all_income_types()
        IncomeTypeService.logger.info(f"查询所有收入类型成功 - 收入类型数量: {len(income_types)}")
        return True, "查询所有收入类型成功", income_types
