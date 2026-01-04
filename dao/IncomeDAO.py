import decimal
from db.Database import Database
from utils.LogUtils import LogUtils

class IncomeDAO:
    """
    收入数据访问对象，封装收入相关的数据库操作
    """
    
    logger = LogUtils.get_instance('IncomeDAO')
    
    def __init__(self):
        """
        初始化IncomeDAO，创建数据库连接
        """
        IncomeDAO.logger.info("初始化IncomeDAO")
        self.db = Database()
    
    def create_income(self, money, account_id, user_id, remark, income_time, income_type_id, enable=True):
        """
        创建新收入记录
        
        Args:
            money: 收入金额
            account_id: 账户ID
            user_id: 用户ID
            remark: 备注
            income_time: 收入时间
            income_type_id: 收入类型ID
            enable: 是否可用，默认true可用
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回收入记录ID，否则返回0
        """
        IncomeDAO.logger.info(f"创建新收入记录: {money} (账户ID: {account_id}, 用户ID: {user_id})")
        try:
            if self.db.connect():
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 1. 检查账户是否存在
                    select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_account_query, (account_id, user_id))
                    account = self.db.cur.fetchone()
                    if not account:
                        IncomeDAO.logger.error(f"创建收入记录失败: 账户不存在或不属于当前用户")
                        self.db.rollback()
                        return False, 0
                    
                    # 2. 插入收入记录
                    insert_query = "INSERT INTO income (money, account_id, user_id, remark, income_time, enable, income_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    self.db.cur.execute(insert_query, (money, account_id, user_id, remark, income_time, enable, income_type_id))
                    income_id = self.db.cur.lastrowid
                    
                    # 3. 更新账户余额
                    current_balance = account[2]  # 账户余额在索引2的位置
                    new_balance = current_balance + decimal.Decimal(str(money))
                    update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                    self.db.cur.execute(update_balance_query, (new_balance, account_id))
                    
                    # 提交事务
                    self.db.commit()
                    IncomeDAO.logger.info(f"收入记录创建成功，ID: {income_id}")
                    return True, income_id
                except Exception as e:
                    IncomeDAO.logger.error(f"创建收入记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False, 0
        except Exception as e:
            IncomeDAO.logger.error(f"创建收入记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_income(self, income_id, user_id, money=None, account_id=None, remark=None, income_time=None, enable=None, income_type_id=None):
        """
        修改收入记录信息
        
        Args:
            income_id: 收入记录ID
            user_id: 用户ID（用于验证权限）
            money: 收入金额（可选）
            account_id: 账户ID（可选）
            remark: 备注（可选）
            income_time: 收入时间（可选）
            enable: 是否可用（可选）
            income_type_id: 收入类型ID（可选）
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        IncomeDAO.logger.info(f"修改收入记录信息: ID={income_id}, 用户ID={user_id}")
        try:
            if self.db.connect():
                # 获取原收入记录信息
                select_query = "SELECT * FROM income WHERE id = %s AND user_id = %s"
                if not self.db.execute(select_query, (income_id, user_id)):
                    self.db.rollback()
                    IncomeDAO.logger.error(f"修改收入记录失败: 无法查询收入记录")
                    return False
                
                original_income = self.db.cur.fetchone()
                if not original_income:
                    self.db.rollback()
                    IncomeDAO.logger.error(f"修改收入记录失败: 收入记录不存在或不属于当前用户")
                    return False
                
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 构建动态更新语句
                    update_fields = []
                    update_values = []
                    
                    # 记录原金额和原账户ID，用于后续更新账户余额
                    original_money = original_income[1]
                    original_account_id = original_income[2]
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
                    
                    if income_time is not None:
                        update_fields.append("income_time = %s")
                        update_values.append(income_time)
                    
                    if enable is not None:
                        update_fields.append("enable = %s")
                        update_values.append(enable)
                    
                    if income_type_id is not None:
                        update_fields.append("income_type_id = %s")
                        update_values.append(income_type_id)
                    
                    # 如果没有提供更新字段，直接提交事务并返回成功
                    if not update_fields:
                        self.db.commit()
                        IncomeDAO.logger.info("没有需要更新的字段，操作成功")
                        return True
                    
                    # 更新收入记录
                    update_query = f"UPDATE income SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
                    update_values.extend([income_id, user_id])
                    self.db.cur.execute(update_query, tuple(update_values))
                    
                    # 不需要检查rowcount，因为我们已经确认记录存在
                    # 即使没有实际更新任何行（内容相同），操作也是成功的
                    
                    # 更新账户余额
                    if original_account_id != new_account_id:
                        # 如果账户ID发生变化，需要同时调整两个账户的余额
                        # 1. 恢复原账户余额
                        select_original_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_original_account_query, (original_account_id, user_id))
                        original_account = self.db.cur.fetchone()
                        if not original_account:
                            self.db.rollback()
                            IncomeDAO.logger.error(f"修改收入记录失败: 原账户不存在")
                            return False
                        
                        new_original_balance = original_account[2] - decimal.Decimal(str(original_money))
                        update_original_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_original_balance_query, (new_original_balance, original_account_id))
                        
                        # 2. 检查新账户是否存在
                        select_new_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_new_account_query, (new_account_id, user_id))
                        new_account = self.db.cur.fetchone()
                        if not new_account:
                            self.db.rollback()
                            IncomeDAO.logger.error(f"修改收入记录失败: 新账户不存在或不属于当前用户")
                            return False
                        
                        # 3. 增加新账户余额
                        new_new_balance = new_account[2] + decimal.Decimal(str(new_money))
                        update_new_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_new_balance_query, (new_new_balance, new_account_id))
                    elif original_money != new_money:
                        # 如果金额发生变化，只需要调整同一个账户的余额
                        select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                        self.db.cur.execute(select_account_query, (original_account_id, user_id))
                        account = self.db.cur.fetchone()
                        if not account:
                            self.db.rollback()
                            IncomeDAO.logger.error(f"修改收入记录失败: 账户不存在")
                            return False
                        
                        # 计算新余额
                        current_balance = account[2]
                        # 先减去原金额，再加新金额
                        new_balance = current_balance - decimal.Decimal(str(original_money)) + decimal.Decimal(str(new_money))
                        
                        update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                        self.db.cur.execute(update_balance_query, (new_balance, original_account_id))
                    
                    # 提交事务
                    self.db.commit()
                    IncomeDAO.logger.info(f"收入记录ID={income_id}的信息修改成功")
                    return True
                except Exception as e:
                    IncomeDAO.logger.error(f"修改收入记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False
        except Exception as e:
            IncomeDAO.logger.error(f"修改收入记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_income(self, income_id, user_id):
        """
        删除收入记录
        
        Args:
            income_id: 收入记录ID
            user_id: 用户ID（用于验证权限）
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        IncomeDAO.logger.info(f"删除收入记录: ID={income_id}, 用户ID={user_id}")
        try:
            if self.db.connect():
                # 开始事务
                self.db.cur.execute("START TRANSACTION")
                
                try:
                    # 1. 查询收入记录
                    select_query = "SELECT * FROM income WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_query, (income_id, user_id))
                    income = self.db.cur.fetchone()
                    if not income:
                        self.db.rollback()
                        IncomeDAO.logger.error(f"删除收入记录失败: 收入记录不存在或不属于当前用户")
                        return False
                    
                    # 2. 删除收入记录
                    delete_query = "DELETE FROM income WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(delete_query, (income_id, user_id))
                    
                    # 3. 减少账户余额
                    account_id = income[2]  # 账户ID在索引2的位置
                    money = income[1]  # 收入金额在索引1的位置
                    
                    select_account_query = "SELECT * FROM account WHERE id = %s AND user_id = %s"
                    self.db.cur.execute(select_account_query, (account_id, user_id))
                    account = self.db.cur.fetchone()
                    if not account:
                        self.db.rollback()
                        IncomeDAO.logger.error(f"删除收入记录失败: 账户不存在")
                        return False
                    
                    new_balance = account[2] - decimal.Decimal(str(money))  # 账户余额在索引2的位置
                    update_balance_query = "UPDATE account SET balance = %s WHERE id = %s"
                    self.db.cur.execute(update_balance_query, (new_balance, account_id))
                    
                    # 提交事务
                    self.db.commit()
                    IncomeDAO.logger.info(f"收入记录ID={income_id}删除成功")
                    return True
                except Exception as e:
                    IncomeDAO.logger.error(f"删除收入记录时事务处理失败: {e}")
                    self.db.rollback()
                    return False
        except Exception as e:
            IncomeDAO.logger.error(f"删除收入记录时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_income_by_id(self, income_id, user_id):
        """
        根据收入记录ID查询收入记录
        
        Args:
            income_id: 收入记录ID
            user_id: 用户ID（用于验证权限）
            
        Returns:
            tuple: 如果查询成功返回收入记录信息，否则返回None
        """
        IncomeDAO.logger.info(f"根据ID查询收入记录: {income_id}, 用户ID: {user_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM income WHERE id = %s AND user_id = %s"
                if self.db.execute(select_query, (income_id, user_id)):
                    income = self.db.cur.fetchone()
                    if income:
                        IncomeDAO.logger.info(f"查询到收入记录ID={income_id}的信息")
                        return income
                    else:
                        IncomeDAO.logger.info(f"未查询到收入记录ID={income_id}的信息")
                        return None
        except Exception as e:
            IncomeDAO.logger.error(f"查询收入记录ID={income_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_incomes_by_user_id(self, user_id, account_id=None, income_type_id=None, start_time=None, end_time=None):
        """
        根据用户ID查询收入记录列表
        
        Args:
            user_id: 用户ID
            account_id: 账户ID（可选）
            income_type_id: 收入类型ID（可选）
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            
        Returns:
            list: 如果查询成功返回收入记录列表，否则返回空列表
        """
        IncomeDAO.logger.info(f"根据用户ID查询收入记录: {user_id}")
        try:
            if self.db.connect():
                # 构建查询语句
                select_query = "SELECT * FROM income WHERE user_id = %s"
                query_params = [user_id]
                
                if account_id is not None:
                    select_query += " AND account_id = %s"
                    query_params.append(account_id)
                
                if income_type_id is not None:
                    select_query += " AND income_type_id = %s"
                    query_params.append(income_type_id)
                
                if start_time is not None:
                    select_query += " AND income_time >= %s"
                    query_params.append(start_time)
                
                if end_time is not None:
                    select_query += " AND income_time <= %s"
                    query_params.append(end_time)
                
                # 按收入时间倒序排序
                select_query += " ORDER BY income_time DESC"
                
                if self.db.execute(select_query, tuple(query_params)):
                    incomes = self.db.cur.fetchall()
                    if incomes:
                        IncomeDAO.logger.info(f"查询到用户ID={user_id}的{len(incomes)}个收入记录")
                        return incomes
                    else:
                        IncomeDAO.logger.info(f"用户ID={user_id}没有收入记录")
                        return []
        except Exception as e:
            IncomeDAO.logger.error(f"查询用户ID={user_id}的收入记录时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()
