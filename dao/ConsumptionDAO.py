from db.Database import Database
from utils.LogUtils import LogUtils

class ConsumptionDAO:
    """
    消费类型数据访问对象，封装消费类型相关的数据库操作
    """
    
    logger = LogUtils.get_instance('ConsumptionDAO')
    
    def __init__(self):
        """
        初始化ConsumptionDAO，创建数据库连接
        """
        ConsumptionDAO.logger.info("初始化ConsumptionDAO")
        self.db = Database()
    
    def create_consumption(self, type_name, enable=True):
        """
        创建新消费类型
        
        Args:
            type_name: 消费类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回消费类型ID，否则返回0
        """
        ConsumptionDAO.logger.info(f"创建新消费类型: {type_name} (启用: {enable})")
        try:
            if self.db.connect():
                insert_query = "INSERT INTO consumption (type, enable) VALUES (%s, %s)"
                if self.db.execute(insert_query, (type_name, enable)):
                    self.db.commit()
                    # 获取新创建的消费类型ID
                    consumption_id = self.db.cur.lastrowid
                    ConsumptionDAO.logger.info(f"消费类型{type_name}创建成功，ID: {consumption_id}")
                    return True, consumption_id
                else:
                    self.db.rollback()
                    ConsumptionDAO.logger.error(f"消费类型{type_name}创建失败: 无法插入信息")
                    return False, 0
        except Exception as e:
            ConsumptionDAO.logger.error(f"消费类型{type_name}创建时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_consumption(self, consumption_id, type_name=None, enable=None):
        """
        修改消费类型信息
        
        Args:
            consumption_id: 消费类型ID
            type_name: 消费类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        ConsumptionDAO.logger.info(f"修改消费类型信息: ID={consumption_id}, 类型={type_name}, 启用={enable}")
        try:
            if self.db.connect():
                # 构建动态更新语句
                update_fields = []
                update_values = []
                
                if type_name is not None:
                    update_fields.append("type = %s")
                    update_values.append(type_name)
                if enable is not None:
                    update_fields.append("enable = %s")
                    update_values.append(enable)
                
                if not update_fields:
                    ConsumptionDAO.logger.warning("未提供任何更新字段")
                    return False
                
                update_query = f"UPDATE consumption SET {', '.join(update_fields)} WHERE id = %s"
                update_values.append(consumption_id)
                
                if self.db.execute(update_query, tuple(update_values)):
                    # 检查是否有行被修改
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        ConsumptionDAO.logger.info(f"消费类型ID={consumption_id}的信息修改成功")
                        return True
                    else:
                        self.db.rollback()
                        ConsumptionDAO.logger.error(f"消费类型ID={consumption_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    ConsumptionDAO.logger.error(f"修改消费类型ID={consumption_id}的信息失败")
                    return False
        except Exception as e:
            ConsumptionDAO.logger.error(f"修改消费类型ID={consumption_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_consumption(self, consumption_id):
        """
        删除消费类型
        
        Args:
            consumption_id: 消费类型ID
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        ConsumptionDAO.logger.info(f"删除消费类型: ID={consumption_id}")
        try:
            if self.db.connect():
                delete_query = "DELETE FROM consumption WHERE id = %s"
                if self.db.execute(delete_query, (consumption_id,)):
                    # 检查是否有行被删除
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        ConsumptionDAO.logger.info(f"消费类型ID={consumption_id}删除成功")
                        return True
                    else:
                        self.db.rollback()
                        ConsumptionDAO.logger.error(f"消费类型ID={consumption_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    ConsumptionDAO.logger.error(f"删除消费类型ID={consumption_id}失败")
                    return False
        except Exception as e:
            ConsumptionDAO.logger.error(f"删除消费类型ID={consumption_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_consumption_by_id(self, consumption_id):
        """
        根据消费类型ID查询消费类型
        
        Args:
            consumption_id: 消费类型ID
            
        Returns:
            tuple: 如果查询成功返回消费类型信息，否则返回None
        """
        ConsumptionDAO.logger.info(f"根据ID查询消费类型: {consumption_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM consumption WHERE id = %s"
                if self.db.execute(select_query, (consumption_id,)):
                    consumption = self.db.cur.fetchone()
                    if consumption:
                        ConsumptionDAO.logger.info(f"查询到消费类型ID={consumption_id}的信息")
                        return consumption
                    else:
                        ConsumptionDAO.logger.info(f"未查询到消费类型ID={consumption_id}的信息")
                        return None
        except Exception as e:
            ConsumptionDAO.logger.error(f"查询消费类型ID={consumption_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_all_consumptions(self):
        """
        查询所有消费类型
        
        Returns:
            list: 如果查询成功返回消费类型列表，否则返回空列表
        """
        ConsumptionDAO.logger.info("查询所有消费类型")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM consumption"
                if self.db.execute(select_query):
                    consumptions = self.db.cur.fetchall()
                    if consumptions:
                        ConsumptionDAO.logger.info(f"查询到{len(consumptions)}个消费类型")
                        return consumptions
                    else:
                        ConsumptionDAO.logger.info("未查询到任何消费类型")
                        return []
        except Exception as e:
            ConsumptionDAO.logger.error(f"查询所有消费类型时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()
