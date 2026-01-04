import decimal
from db.Database import Database
from utils.LogUtils import LogUtils

class ExpendDAO:
    """
    支出数据访问对象，封装支出相关的数据库操作
    """
    
    logger = LogUtils.get_instance('ExpendDAO')
    
    def __init__(self):
        """
        初始化ExpendDAO，创建数据库连接
        """
        ExpendDAO.logger.info("初始化ExpendDAO")
        self.db = Database()
    
    def create_expend(self, money, account_id, user_id, remark, expend_time, expend_type_id, enable=True):
        """
        创建新支出记录
        
        Args:
            money: 支出金额
            account_id: 账户ID
            user_id: 用户ID
            remark: 备注
            expend_time: 支出时间
            expend_type_id: 消费类型ID
            enable: 是否可用，默认true可用
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回支出记录ID，否则返回0
        """
        ExpendDAO.logger.info(f"创建新支出记录: {money} (账户ID: {account_id}, 用户ID: {user_id})")
        try:
            if self.db.connect():
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 1. 检查账户是否存在且余额足够
                    select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_account_query, (account_id, user_id))
                    account = self.db.cur.fetchone()
                    if not account:
                        ExpendDAO.logger.error(f"创建支出记录失败: 账户不存在或不属于当前用户")
                        self.db.rollback()
                        return False, 0
                    
                    current_balance = account[2]  # 账户余额在索引2的位置
                    if current_balance < money:
                        ExpendDAO.logger.error(f"创建支出记录失败: 账户余额不足")
                        self.db.rollback()
                        return False, 0
                    
                    # 2. 插入支出记录
                    insert_query = "INSERT INTO expend (money, account_id, user_id, remark, expend_time, enable, expend_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    self.db.cur.execute(insert_query, (money, account_id, user_id, remark, expend_time, enable, expend_type_id))
                    expend_id = self.db.cur.lastrowid
                    
                    # 3. 更新账户余额
                    new_balance = current_balance - decimal.Decimal(str(money))
                    update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                    self.db.cur.execute(update_balance_query, (new_balance, account_id))
                    
                    # 提交事务
                    self.db.commit()
                    ExpendDAO.logger.info(f"支出记录创建成功，ID: {expend_id}")
                    return True, expend_id
                except Exception as e:
                    ExpendDAO.logger.error(f"创建支出记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False, 0
        except Exception as e:
            ExpendDAO.logger.error(f"创建支出记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_expend(self, expend_id, user_id, money=None, account_id=None, remark=None, expend_time=None, enable=None, expend_type_id=None):
        """
        修改支出记录信息
        
        Args:
            expend_id: 支出记录ID
            user_id: 用户ID（用于验证权限）
            money: 支出金额（可选）
            account_id: 账户ID（可选）
            remark: 备注（可选）
            expend_time: 支出时间（可选）
            enable: 是否可用（可选）
            expend_type_id: 消费类型ID（可选）
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        ExpendDAO.logger.info(f"修改支出记录信息: ID={expend_id}, 用户ID={user_id}")
        try:
            if self.db.connect():
                # 获取原支出记录信息
                select_query = "SELECT * FROM expend WHERE id = %s AND user_id = %s"
                if not self.db.execute(select_query, (expend_id, user_id)):
                    self.db.rollback()
                    ExpendDAO.logger.error(f"修改支出记录失败: 无法查询支出记录")
                    return False
                
                original_expend = self.db.cur.fetchone()
                if not original_expend:
                    self.db.rollback()
                    ExpendDAO.logger.error(f"修改支出记录失败: 支出记录不存在或不属于当前用户")
                    return False
                
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 构建动态更新语句
                    update_fields = []
                    update_values = []
                    
                    # 记录原金额和原账户ID，用于后续更新账户余额
                    original_money = original_expend[1]
                    original_account_id = original_expend[2]
                    new_money = original_money
                    new_account_id = original_account_id
                    
                    if money is not None:
                        update_fields.append("money = %s")
                        update_values.append(money)
                        new_money = money
                    
                    if account_id is not None and account_id != original_account_id:
                        update_fields.append("account_id = %s")
                        update_values.append(account_id)
                        new_account_id = account_id
                    
                    if remark is not None:
                        update_fields.append("remark = %s")
                        update_values.append(remark)
                    
                    if expend_time is not None:
                        update_fields.append("expend_time = %s")
                        update_values.append(expend_time)
                    
                    if enable is not None:
                        update_fields.append("enable = %s")
                        update_values.append(enable)
                    
                    if expend_type_id is not None:
                        update_fields.append("expend_type_id = %s")
                        update_values.append(expend_type_id)
                    
                    if not update_fields:
                        self.db.rollback()
                        ExpendDAO.logger.warning("未提供任何更新字段")
                        return False
                    
                    # 更新支出记录
                    update_query = f"UPDATE expend SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
                    update_values.extend([expend_id, user_id])
                    self.db.cur.execute(update_query, tuple(update_values))
                    
                    # 检查是否有行被修改
                    if self.db.cur.rowcount == 0:
                        self.db.rollback()
                        ExpendDAO.logger.error(f"修改支出记录失败: 支出记录不存在或不属于当前用户")
                        return False
                    
                    # 更新账户余额
                    if original_account_id != new_account_id:
                        # 如果账户ID发生变化，需要同时调整两个账户的余额
                        # 1. 恢复原账户余额
                        select_original_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_original_account_query, (original_account_id, user_id))
                        original_account = self.db.cur.fetchone()
                        if not original_account:
                            self.db.rollback()
                            ExpendDAO.logger.error(f"修改支出记录失败: 原账户不存在")
                            return False
                        
                        new_original_balance = original_account[2] + decimal.Decimal(str(original_money))
                        update_original_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_original_balance_query, (new_original_balance, original_account_id))
                        
                        # 2. 检查新账户是否存在且余额足够
                        select_new_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_new_account_query, (new_account_id, user_id))
                        new_account = self.db.cur.fetchone()
                        if not new_account:
                            self.db.rollback()
                            ExpendDAO.logger.error(f"修改支出记录失败: 新账户不存在或不属于当前用户")
                            return False
                        
                        current_new_balance = new_account[2]
                        if current_new_balance < new_money:
                            self.db.rollback()
                            ExpendDAO.logger.error(f"修改支出记录失败: 新账户余额不足")
                            return False
                        
                        # 3. 扣除新账户余额
                        new_new_balance = current_new_balance - decimal.Decimal(str(new_money))
                        update_new_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_new_balance_query, (new_new_balance, new_account_id))
                    elif original_money != new_money:
                        # 如果金额发生变化，只需要调整同一个账户的余额
                        select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_account_query, (original_account_id, user_id))
                        account = self.db.cur.fetchone()
                        if not account:
                            self.db.rollback()
                            ExpendDAO.logger.error(f"修改支出记录失败: 账户不存在")
                            return False
                        
                        # 计算新余额
                        current_balance = account[2]
                        # 先恢复原金额，再扣除新金额
                        new_balance = current_balance + decimal.Decimal(str(original_money)) - decimal.Decimal(str(new_money))
                        
                        if new_balance < 0:
                            self.db.rollback()
                            ExpendDAO.logger.error(f"修改支出记录失败: 账户余额不足")
                            return False
                        
                        update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_balance_query, (new_balance, original_account_id))
                    
                    # 提交事务
                    self.db.commit()
                    ExpendDAO.logger.info(f"支出记录ID={expend_id}的信息修改成功")
                    return True
                except Exception as e:
                    ExpendDAO.logger.error(f"修改支出记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False
        except Exception as e:
            ExpendDAO.logger.error(f"修改支出记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_expend(self, expend_id, user_id):
        """
        删除支出记录
        
        Args:
            expend_id: 支出记录ID
            user_id: 用户ID（用于验证权限）
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        ExpendDAO.logger.info(f"删除支出记录: ID={expend_id}, 用户ID={user_id}")
        try:
            if self.db.connect():
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 1. 查询支出记录
                    select_query = "SELECT * FROM expend WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_query, (expend_id, user_id))
                    expend = self.db.cur.fetchone()
                    if not expend:
                        self.db.rollback()
                        ExpendDAO.logger.error(f"删除支出记录失败: 支出记录不存在或不属于当前用户")
                        return False
                    
                    # 2. 删除支出记录
                    delete_query = "DELETE FROM expend WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(delete_query, (expend_id, user_id))
                    
                    # 3. 恢复账户余额
                    account_id = expend[2]  # 账户ID在索引2的位置
                    money = expend[1]  # 支出金额在索引1的位置
                    
                    select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_account_query, (account_id, user_id))
                    account = self.db.cur.fetchone()
                    if not account:
                        self.db.rollback()
                        ExpendDAO.logger.error(f"删除支出记录失败: 账户不存在")
                        return False
                    
                    new_balance = account[2] + decimal.Decimal(str(money))  # 账户余额在索引2的位置
                    update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                    self.db.cur.execute(update_balance_query, (new_balance, account_id))
                    
                    # 提交事务
                    self.db.commit()
                    ExpendDAO.logger.info(f"支出记录ID={expend_id}删除成功")
                    return True
                except Exception as e:
                    ExpendDAO.logger.error(f"删除支出记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False
        except Exception as e:
            ExpendDAO.logger.error(f"删除支出记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_expend_by_id(self, expend_id, user_id):
        """
        根据支出记录ID查询支出记录
        
        Args:
            expend_id: 支出记录ID
            user_id: 用户ID（用于验证权限）
            
        Returns:
            tuple: 如果查询成功返回支出记录信息，否则返回None
        """
        ExpendDAO.logger.info(f"根据ID查询支出记录: {expend_id}, 用户ID: {user_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM expend WHERE id = %s AND user_id = %s"
                if self.db.execute(select_query, (expend_id, user_id)):
                    expend = self.db.cur.fetchone()
                    if expend:
                        ExpendDAO.logger.info(f"查询到支出记录ID={expend_id}的信息")
                        return expend
                    else:
                        ExpendDAO.logger.info(f"未查询到支出记录ID={expend_id}的信息")
                        return None
        except Exception as e:
            ExpendDAO.logger.error(f"查询支出记录ID={expend_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_expends_by_user_id(self, user_id, account_id=None, expend_type_id=None, start_time=None, end_time=None):
        """
        根据用户ID查询支出记录列表
        
        Args:
            user_id: 用户ID
            account_id: 账户ID（可选）
            expend_type_id: 消费类型ID（可选）
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            
        Returns:
            list: 如果查询成功返回支出记录列表，否则返回空列表
        """
        ExpendDAO.logger.info(f"根据用户ID查询支出记录: {user_id}")
        try:
            if self.db.connect():
                # 构建查询语句
                select_query = "SELECT * FROM expend WHERE user_id = %s"
                query_params = [user_id]
                
                if account_id is not None:
                    select_query += " AND account_id = %s"
                    query_params.append(account_id)
                
                if expend_type_id is not None:
                    select_query += " AND expend_type_id = %s"
                    query_params.append(expend_type_id)
                
                if start_time is not None:
                    select_query += " AND expend_time >= %s"
                    query_params.append(start_time)
                
                if end_time is not None:
                    select_query += " AND expend_time <= %s"
                    query_params.append(end_time)
                
                # 按支出时间倒序排序
                select_query += " ORDER BY expend_time DESC"
                
                if self.db.execute(select_query, tuple(query_params)):
                    expends = self.db.cur.fetchall()
                    if expends:
                        ExpendDAO.logger.info(f"查询到用户ID={user_id}的{len(expends)}个支出记录")
                        return expends
                    else:
                        ExpendDAO.logger.info(f"用户ID={user_id}没有支出记录")
                        return []
        except Exception as e:
            ExpendDAO.logger.error(f"查询用户ID={user_id}的支出记录时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()
