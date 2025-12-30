from dao.ExpendTypeDAO import ExpendTypeDAO
from utils.LogUtils import LogUtils


class ExpendTypeService:
    """
    消费类型业务逻辑层，处理消费类型相关的业务规则
    """
    
    logger = LogUtils.get_instance('ExpendTypeService')
    
    def __init__(self):
        """
        初始化ConsumptionService，创建ConsumptionDAO实例
        """
        ExpendTypeService.logger.info("初始化ExpendTypeService")
        self.expend_type_dao = ExpendTypeDAO()
    
    def create_expend_type(self, expend_type_name, enable=True):
        """
        创建新消费类型业务逻辑
        
        Args:
            expend_type_name: 消费类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ExpendTypeService.logger.info(f"创建消费类型请求 - 类型名称: {expend_type_name}, 启用: {enable}")
        
        # 参数验证
        if not expend_type_name:
            ExpendTypeService.logger.warning("创建消费类型失败: 消费类型说明不能为空")
            return False, "消费类型说明不能为空", None
        
        # 调用DAO创建消费类型
        success, expend_type_id = self.expend_type_dao.create_expend_type(expend_type_name, enable)
        if success:
            # 获取创建的消费类型信息
            expend_type = self.expend_type_dao.get_expend_type_by_id(expend_type_id)
            if expend_type:
                ExpendTypeService.logger.info(f"消费类型创建成功 - 消费类型ID: {expend_type_id}, 类型名称: {expend_type_name}")
                return True, "消费类型创建成功", expend_type
            else:
                ExpendTypeService.logger.error(f"消费类型创建成功但无法获取消费类型信息 - 消费类型ID: {expend_type_id}")
                return True, "消费类型创建成功但无法获取消费类型信息", None
        else:
            ExpendTypeService.logger.error(f"消费类型创建失败 - 类型名称: {expend_type_name}")
            return False, "消费类型创建失败", None
    
    def update_expend_type(self, expend_type_id, expend_type_name=None, enable=None):
        """
        修改消费类型信息业务逻辑
        
        Args:
            expend_type_id: 消费类型ID
            expend_type_name: 消费类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ExpendTypeService.logger.info(f"修改消费类型请求 - 消费类型ID: {expend_type_id}, 类型名称: {expend_type_name}, 启用: {enable}")
        
        # 参数验证
        if not expend_type_id:
            ExpendTypeService.logger.warning("修改消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空", None
        
        if expend_type_name is None and enable is None:
            ExpendTypeService.logger.warning("修改消费类型失败: 未提供任何更新字段")
            return False, "未提供任何更新字段", None
        
        # 检查消费类型是否存在
        expend_type = self.expend_type_dao.get_expend_type_by_id(expend_type_id)
        if not expend_type:
            ExpendTypeService.logger.warning(f"修改消费类型失败: 消费类型不存在 - 消费类型ID: {expend_type_id}")
            return False, "消费类型不存在", None
        
        # 调用DAO修改消费类型
        if self.expend_type_dao.update_expend_type(expend_type_id, expend_type_name, enable):
            # 获取更新后的消费类型信息
            updated_expend_type = self.expend_type_dao.get_expend_type_by_id(expend_type_id)
            ExpendTypeService.logger.info(f"消费类型修改成功 - 消费类型ID: {expend_type_id}")
            return True, "消费类型修改成功", updated_expend_type
        else:
            ExpendTypeService.logger.error(f"消费类型修改失败 - 消费类型ID: {expend_type_id}")
            return False, "消费类型修改失败", None
    
    def delete_expend_type(self, expend_type_id):
        """
        删除消费类型业务逻辑
        
        Args:
            expend_type_id: 消费类型ID
            
        Returns:
            tuple: (是否成功, 消息)
        """
        ExpendTypeService.logger.info(f"删除消费类型请求 - 消费类型ID: {expend_type_id}")
        
        # 参数验证
        if not expend_type_id:
            ExpendTypeService.logger.warning("删除消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空"
        
        # 检查消费类型是否存在
        expend_type = self.expend_type_dao.get_expend_type_by_id(expend_type_id)
        if not expend_type:
            ExpendTypeService.logger.warning(f"删除消费类型失败: 消费类型不存在 - 消费类型ID: {expend_type_id}")
            return False, "消费类型不存在"
        
        # 调用DAO删除消费类型
        if self.expend_type_dao.delete_expend_type(expend_type_id):
            ExpendTypeService.logger.info(f"消费类型删除成功 - 消费类型ID: {expend_type_id}")
            return True, "消费类型删除成功"
        else:
            ExpendTypeService.logger.error(f"消费类型删除失败 - 消费类型ID: {expend_type_id}")
            return False, "消费类型删除失败"
    
    def get_expend_type_by_id(self, expend_type_id):
        """
        根据消费类型ID查询消费类型业务逻辑
        
        Args:
            expend_type_id: 消费类型ID
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ExpendTypeService.logger.info(f"查询消费类型请求 - 消费类型ID: {expend_type_id}")
        
        # 参数验证
        if not expend_type_id:
            ExpendTypeService.logger.warning("查询消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空", None
        
        # 调用DAO查询消费类型
        expend_type = self.expend_type_dao.get_expend_type_by_id(expend_type_id)
        if expend_type:
            ExpendTypeService.logger.info(f"查询消费类型成功 - 消费类型ID: {expend_type_id}")
            return True, "查询消费类型成功", expend_type
        else:
            ExpendTypeService.logger.warning(f"查询消费类型失败: 消费类型不存在 - 消费类型ID: {expend_type_id}")
            return False, "消费类型不存在", None
    
    def get_all_expend_types(self):
        """
        查询所有消费类型业务逻辑
        
        Returns:
            tuple: (是否成功, 消息, 消费类型列表)
        """
        ExpendTypeService.logger.info("查询所有消费类型请求")
        
        # 调用DAO查询所有消费类型
        expend_types = self.expend_type_dao.get_all_expend_types()
        ExpendTypeService.logger.info(f"查询所有消费类型成功 - 消费类型数量: {len(expend_types)}")
        return True, "查询所有消费类型成功", expend_types
