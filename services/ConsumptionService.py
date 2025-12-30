from dao.ConsumptionDAO import ConsumptionDAO
from utils.LogUtils import LogUtils


class ConsumptionService:
    """
    消费类型业务逻辑层，处理消费类型相关的业务规则
    """
    
    logger = LogUtils.get_instance('ConsumptionService')
    
    def __init__(self):
        """
        初始化ConsumptionService，创建ConsumptionDAO实例
        """
        ConsumptionService.logger.info("初始化ConsumptionService")
        self.consumption_dao = ConsumptionDAO()
    
    def create_consumption(self, type_name, enable=True):
        """
        创建新消费类型业务逻辑
        
        Args:
            type_name: 消费类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ConsumptionService.logger.info(f"创建消费类型请求 - 类型名称: {type_name}, 启用: {enable}")
        
        # 参数验证
        if not type_name:
            ConsumptionService.logger.warning("创建消费类型失败: 消费类型说明不能为空")
            return False, "消费类型说明不能为空", None
        
        # 调用DAO创建消费类型
        success, consumption_id = self.consumption_dao.create_consumption(type_name, enable)
        if success:
            # 获取创建的消费类型信息
            consumption = self.consumption_dao.get_consumption_by_id(consumption_id)
            if consumption:
                ConsumptionService.logger.info(f"消费类型创建成功 - 消费类型ID: {consumption_id}, 类型名称: {type_name}")
                return True, "消费类型创建成功", consumption
            else:
                ConsumptionService.logger.error(f"消费类型创建成功但无法获取消费类型信息 - 消费类型ID: {consumption_id}")
                return True, "消费类型创建成功但无法获取消费类型信息", None
        else:
            ConsumptionService.logger.error(f"消费类型创建失败 - 类型名称: {type_name}")
            return False, "消费类型创建失败", None
    
    def update_consumption(self, consumption_id, type_name=None, enable=None):
        """
        修改消费类型信息业务逻辑
        
        Args:
            consumption_id: 消费类型ID
            type_name: 消费类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ConsumptionService.logger.info(f"修改消费类型请求 - 消费类型ID: {consumption_id}, 类型名称: {type_name}, 启用: {enable}")
        
        # 参数验证
        if not consumption_id:
            ConsumptionService.logger.warning("修改消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空", None
        
        if type_name is None and enable is None:
            ConsumptionService.logger.warning("修改消费类型失败: 未提供任何更新字段")
            return False, "未提供任何更新字段", None
        
        # 检查消费类型是否存在
        consumption = self.consumption_dao.get_consumption_by_id(consumption_id)
        if not consumption:
            ConsumptionService.logger.warning(f"修改消费类型失败: 消费类型不存在 - 消费类型ID: {consumption_id}")
            return False, "消费类型不存在", None
        
        # 调用DAO修改消费类型
        if self.consumption_dao.update_consumption(consumption_id, type_name, enable):
            # 获取更新后的消费类型信息
            updated_consumption = self.consumption_dao.get_consumption_by_id(consumption_id)
            ConsumptionService.logger.info(f"消费类型修改成功 - 消费类型ID: {consumption_id}")
            return True, "消费类型修改成功", updated_consumption
        else:
            ConsumptionService.logger.error(f"消费类型修改失败 - 消费类型ID: {consumption_id}")
            return False, "消费类型修改失败", None
    
    def delete_consumption(self, consumption_id):
        """
        删除消费类型业务逻辑
        
        Args:
            consumption_id: 消费类型ID
            
        Returns:
            tuple: (是否成功, 消息)
        """
        ConsumptionService.logger.info(f"删除消费类型请求 - 消费类型ID: {consumption_id}")
        
        # 参数验证
        if not consumption_id:
            ConsumptionService.logger.warning("删除消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空"
        
        # 检查消费类型是否存在
        consumption = self.consumption_dao.get_consumption_by_id(consumption_id)
        if not consumption:
            ConsumptionService.logger.warning(f"删除消费类型失败: 消费类型不存在 - 消费类型ID: {consumption_id}")
            return False, "消费类型不存在"
        
        # 调用DAO删除消费类型
        if self.consumption_dao.delete_consumption(consumption_id):
            ConsumptionService.logger.info(f"消费类型删除成功 - 消费类型ID: {consumption_id}")
            return True, "消费类型删除成功"
        else:
            ConsumptionService.logger.error(f"消费类型删除失败 - 消费类型ID: {consumption_id}")
            return False, "消费类型删除失败"
    
    def get_consumption_by_id(self, consumption_id):
        """
        根据消费类型ID查询消费类型业务逻辑
        
        Args:
            consumption_id: 消费类型ID
            
        Returns:
            tuple: (是否成功, 消息, 消费类型信息)
        """
        ConsumptionService.logger.info(f"查询消费类型请求 - 消费类型ID: {consumption_id}")
        
        # 参数验证
        if not consumption_id:
            ConsumptionService.logger.warning("查询消费类型失败: 消费类型ID不能为空")
            return False, "消费类型ID不能为空", None
        
        # 调用DAO查询消费类型
        consumption = self.consumption_dao.get_consumption_by_id(consumption_id)
        if consumption:
            ConsumptionService.logger.info(f"查询消费类型成功 - 消费类型ID: {consumption_id}")
            return True, "查询消费类型成功", consumption
        else:
            ConsumptionService.logger.warning(f"查询消费类型失败: 消费类型不存在 - 消费类型ID: {consumption_id}")
            return False, "消费类型不存在", None
    
    def get_all_consumptions(self):
        """
        查询所有消费类型业务逻辑
        
        Returns:
            tuple: (是否成功, 消息, 消费类型列表)
        """
        ConsumptionService.logger.info("查询所有消费类型请求")
        
        # 调用DAO查询所有消费类型
        consumptions = self.consumption_dao.get_all_consumptions()
        ConsumptionService.logger.info(f"查询所有消费类型成功 - 消费类型数量: {len(consumptions)}")
        return True, "查询所有消费类型成功", consumptions
