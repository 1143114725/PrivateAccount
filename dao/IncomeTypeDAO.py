from db.Database import Database
from utils.LogUtils import LogUtils

class IncomeTypeDAO:
    """
    收入类型数据访问对象，封装收入类型相关的数据库操作
    """
    
    logger = LogUtils.get_instance('IncomeTypeDAO')
    
    def __init__(self):
        """
        初始化IncomeTypeDAO，创建数据库连接
        """
        IncomeTypeDAO.logger.info("初始化IncomeTypeDAO")
        self.db = Database()
    
    def create_income_type(self, income_type_name, enable=True):
        """
        创建新收入类型
        
        Args:
            income_type_name: 收入类型说明
            enable: 是否禁用，默认true可用
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回收入类型ID，否则返回0
        """
        IncomeTypeDAO.logger.info(f"创建新收入类型: {income_type_name} (启用: {enable})")
        try:
            if self.db.connect():
                insert_query = "INSERT INTO income_type (income_type_name, enable, create_time) VALUES (%s, %s, NOW())"
                if self.db.execute(insert_query, (income_type_name, enable)):
                    self.db.commit()
                    # 获取新创建的收入类型ID
                    income_type_id = self.db.cur.lastrowid
                    IncomeTypeDAO.logger.info(f"收入类型{income_type_name}创建成功，ID: {income_type_id}")
                    return True, income_type_id
                else:
                    self.db.rollback()
                    IncomeTypeDAO.logger.error(f"收入类型{income_type_name}创建失败: 无法插入信息")
                    return False, 0
        except Exception as e:
            IncomeTypeDAO.logger.error(f"收入类型{income_type_name}创建时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_income_type(self, income_type_id, income_type_name=None, enable=None):
        """
        修改收入类型信息
        
        Args:
            income_type_id: 收入类型ID
            income_type_name: 收入类型说明（可选）
            enable: 是否禁用（可选）
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        IncomeTypeDAO.logger.info(f"修改收入类型信息: ID={income_type_id}, 类型={income_type_name}, 启用={enable}")
        try:
            if self.db.connect():
                # 构建动态更新语句
                update_fields = []
                update_values = []
                
                if income_type_name is not None:
                    update_fields.append("income_type_name = %s")
                    update_values.append(income_type_name)
                if enable is not None:
                    update_fields.append("enable = %s")
                    update_values.append(enable)
                
                if not update_fields:
                    IncomeTypeDAO.logger.warning("未提供任何更新字段")
                    return False
                
                update_query = f"UPDATE income_type SET {', '.join(update_fields)} WHERE id = %s"
                update_values.append(income_type_id)
                
                if self.db.execute(update_query, tuple(update_values)):
                    # 检查是否有行被修改
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        IncomeTypeDAO.logger.info(f"收入类型ID={income_type_id}的信息修改成功")
                        return True
                    else:
                        self.db.rollback()
                        IncomeTypeDAO.logger.error(f"收入类型ID={income_type_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    IncomeTypeDAO.logger.error(f"修改收入类型ID={income_type_id}的信息失败")
                    return False
        except Exception as e:
            IncomeTypeDAO.logger.error(f"修改收入类型ID={income_type_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_income_type(self, income_type_id):
        """
        删除收入类型
        
        Args:
            income_type_id: 收入类型ID
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        IncomeTypeDAO.logger.info(f"删除收入类型: ID={income_type_id}")
        try:
            if self.db.connect():
                delete_query = "DELETE FROM income_type WHERE id = %s"
                if self.db.execute(delete_query, (income_type_id,)):
                    # 检查是否有行被删除
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        IncomeTypeDAO.logger.info(f"收入类型ID={income_type_id}删除成功")
                        return True
                    else:
                        self.db.rollback()
                        IncomeTypeDAO.logger.error(f"收入类型ID={income_type_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    IncomeTypeDAO.logger.error(f"删除收入类型ID={income_type_id}失败")
                    return False
        except Exception as e:
            IncomeTypeDAO.logger.error(f"删除收入类型ID={income_type_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_income_type_by_id(self, income_type_id):
        """
        根据收入类型ID查询收入类型
        
        Args:
            income_type_id: 收入类型ID
            
        Returns:
            tuple: 如果查询成功返回收入类型信息，否则返回None
        """
        IncomeTypeDAO.logger.info(f"根据ID查询收入类型: {income_type_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM income_type WHERE id = %s"
                if self.db.execute(select_query, (income_type_id,)):
                    income_type = self.db.cur.fetchone()
                    if income_type:
                        IncomeTypeDAO.logger.info(f"查询到收入类型ID={income_type_id}的信息")
                        return income_type
                    else:
                        IncomeTypeDAO.logger.info(f"未查询到收入类型ID={income_type_id}的信息")
                        return None
        except Exception as e:
            IncomeTypeDAO.logger.error(f"查询收入类型ID={income_type_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_all_income_types(self):
        """
        查询所有收入类型
        
        Returns:
            list: 如果查询成功返回收入类型列表，否则返回空列表
        """
        IncomeTypeDAO.logger.info("查询所有收入类型")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM income_type"
                if self.db.execute(select_query):
                    income_types = self.db.cur.fetchall()
                    if income_types:
                        IncomeTypeDAO.logger.info(f"查询到{len(income_types)}个收入类型")
                        return income_types
                    else:
                        IncomeTypeDAO.logger.info("未查询到任何收入类型")
                        return []
        except Exception as e:
            IncomeTypeDAO.logger.error(f"查询所有收入类型时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()
