from db.Database import Database
from utils.LogUtils import LogUtils

class ExpendTypeDAO:
    """
    消费类型数据访问对象，封装消费类型相关的数据库操作
    """
    
    logger = LogUtils.get_instance('ExpendTypeDAO')
    
    def __init__(self):
        """
        初始化ExpendTypeDAO，创建数据库连接
        """
        ExpendTypeDAO.logger.info("初始化ExpendTypeDAO")
        self.db = Database()
    
    def create_expend_type(self, expend_type_name, enable=True):
        """
        创建新消费类型
        
        Args:
            expend_type_name: 消费类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回消费类型ID，否则返回0
        """
        ExpendTypeDAO.logger.info(f"创建新消费类型: {expend_type_name} (启用: {enable})")
        try:
            if self.db.connect():
                insert_query = "INSERT INTO expend_type (expend_type_name, enable, create_time) VALUES (%s, %s, NOW())"
                if self.db.execute(insert_query, (expend_type_name, enable)):
                    self.db.commit()
                    # 获取新创建的消费类型ID
                    expend_type_id = self.db.cur.lastrowid
                    ExpendTypeDAO.logger.info(f"消费类型{expend_type_name}创建成功，ID: {expend_type_id}")
                    return True, expend_type_id
                else:
                    self.db.rollback()
                    ExpendTypeDAO.logger.error(f"消费类型{expend_type_name}创建失败: 无法插入信息")
                    return False, 0
        except Exception as e:
            ExpendTypeDAO.logger.error(f"消费类型{expend_type_name}创建时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_expend_type(self, expend_type_id, expend_type_name=None, enable=None):
        """
        修改消费类型信息
        
        Args:
            expend_type_id: 消费类型ID
            expend_type_name: 消费类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        ExpendTypeDAO.logger.info(f"修改消费类型信息: ID={expend_type_id}, 类型={expend_type_name}, 启用={enable}")
        try:
            if self.db.connect():
                # 构建动态更新语句
                update_fields = []
                update_values = []
                
                if expend_type_name is not None:
                    update_fields.append("expend_type_name = %s")
                    update_values.append(expend_type_name)
                if enable is not None:
                    update_fields.append("enable = %s")
                    update_values.append(enable)
                
                if not update_fields:
                    ExpendTypeDAO.logger.warning("未提供任何更新字段")
                    return False
                
                update_query = f"UPDATE expend_type SET {', '.join(update_fields)} WHERE id = %s"
                update_values.append(expend_type_id)
                
                if self.db.execute(update_query, tuple(update_values)):
                    # 检查是否有行被修改
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        ExpendTypeDAO.logger.info(f"消费类型ID={expend_type_id}的信息修改成功")
                        return True
                    else:
                        self.db.rollback()
                        ExpendTypeDAO.logger.error(f"消费类型ID={expend_type_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    ExpendTypeDAO.logger.error(f"修改消费类型ID={expend_type_id}的信息失败")
                    return False
        except Exception as e:
            ExpendTypeDAO.logger.error(f"修改消费类型ID={expend_type_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_expend_type(self, expend_type_id):
        """
        删除消费类型
        
        Args:
            expend_type_id: 消费类型ID
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        ExpendTypeDAO.logger.info(f"删除消费类型: ID={expend_type_id}")
        try:
            if self.db.connect():
                delete_query = "DELETE FROM expend_type WHERE id = %s"
                if self.db.execute(delete_query, (expend_type_id,)):
                    # 检查是否有行被删除
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        ExpendTypeDAO.logger.info(f"消费类型ID={expend_type_id}删除成功")
                        return True
                    else:
                        self.db.rollback()
                        ExpendTypeDAO.logger.error(f"消费类型ID={expend_type_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    ExpendTypeDAO.logger.error(f"删除消费类型ID={expend_type_id}失败")
                    return False
        except Exception as e:
            ExpendTypeDAO.logger.error(f"删除消费类型ID={expend_type_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_expend_type_by_id(self, expend_type_id):
        """
        根据消费类型ID查询消费类型
        
        Args:
            expend_type_id: 消费类型ID
            
        Returns:
            tuple: 如果查询成功返回消费类型信息，否则返回None
        """
        ExpendTypeDAO.logger.info(f"根据ID查询消费类型: {expend_type_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM expend_type WHERE id = %s"
                if self.db.execute(select_query, (expend_type_id,)):
                    expend_type = self.db.cur.fetchone()
                    if expend_type:
                        ExpendTypeDAO.logger.info(f"查询到消费类型ID={expend_type_id}的信息")
                        return expend_type
                    else:
                        ExpendTypeDAO.logger.info(f"未查询到消费类型ID={expend_type_id}的信息")
                        return None
        except Exception as e:
            ExpendTypeDAO.logger.error(f"查询消费类型ID={expend_type_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_all_expend_types(self):
        """
        查询所有消费类型
        
        Returns:
            list: 如果查询成功返回消费类型列表，否则返回空列表
        """
        ExpendTypeDAO.logger.info("查询所有消费类型")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM expend_type"
                if self.db.execute(select_query):
                    expend_types = self.db.cur.fetchall()
                    if expend_types:
                        ExpendTypeDAO.logger.info(f"查询到{len(expend_types)}个消费类型")
                        return expend_types
                    else:
                        ExpendTypeDAO.logger.info("未查询到任何消费类型")
                        return []
        except Exception as e:
            ExpendTypeDAO.logger.error(f"查询所有消费类型时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()

