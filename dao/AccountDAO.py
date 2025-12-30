from db.Database import Database
from utils.LogUtils import LogUtils

class AccountDAO:
    """
    账户数据访问对象，封装账户相关的数据库操作
    """
    
    logger = LogUtils.get_instance('AccountDAO')
    
    def __init__(self):
        """
        初始化AccountDAO，创建数据库连接
        """
        AccountDAO.logger.info("初始化AccountDAO")
        self.db = Database()
    
    def create_account(self, name, balance, user_id):
        """
        创建新账户
        
        Args:
            name: 账户名
            balance: 账户余额
            user_id: 用户ID
            
        Returns:
            bool: 如果创建成功返回True，否则返回False
            int: 如果创建成功返回账户ID，否则返回0
        """
        AccountDAO.logger.info(f"创建新账户: {name} (用户ID: {user_id})")
        try:
            if self.db.connect():
                insert_query = "INSERT INTO account (name, balance, user_id) VALUES (%s, %s, %s)"
                if self.db.execute(insert_query, (name, balance, user_id)):
                    self.db.commit()
                    # 获取新创建的账户ID
                    account_id = self.db.cur.lastrowid
                    AccountDAO.logger.info(f"账户{name}创建成功，账户ID: {account_id}")
                    return True, account_id
                else:
                    self.db.rollback()
                    AccountDAO.logger.error(f"账户{name}创建失败: 无法插入账户信息")
                    return False, 0
        except Exception as e:
            AccountDAO.logger.error(f"账户{name}创建时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False, 0
        finally:
            self.db.disconnect()
    
    def update_balance(self, account_id, new_balance):
        """
        修改账户余额
        
        Args:
            account_id: 账户ID
            new_balance: 新的账户余额
            
        Returns:
            bool: 如果修改成功返回True，否则返回False
        """
        AccountDAO.logger.info(f"修改账户余额: 账户ID={account_id}, 新余额={new_balance}")
        try:
            if self.db.connect():
                update_query = "UPDATE account SET balance = %s WHERE id = %s"
                if self.db.execute(update_query, (new_balance, account_id)):
                    # 检查是否有行被修改
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        AccountDAO.logger.info(f"账户ID={account_id}的余额修改成功")
                        return True
                    else:
                        self.db.rollback()
                        AccountDAO.logger.error(f"账户ID={account_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    AccountDAO.logger.error(f"修改账户ID={account_id}的余额失败")
                    return False
        except Exception as e:
            AccountDAO.logger.error(f"修改账户ID={account_id}的余额时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def delete_account(self, account_id):
        """
        删除账户
        
        Args:
            account_id: 账户ID
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        AccountDAO.logger.info(f"删除账户: 账户ID={account_id}")
        try:
            if self.db.connect():
                delete_query = "DELETE FROM account WHERE id = %s"
                if self.db.execute(delete_query, (account_id,)):
                    # 检查是否有行被删除
                    if self.db.cur.rowcount > 0:
                        self.db.commit()
                        AccountDAO.logger.info(f"账户ID={account_id}删除成功")
                        return True
                    else:
                        self.db.rollback()
                        AccountDAO.logger.error(f"账户ID={account_id}不存在")
                        return False
                else:
                    self.db.rollback()
                    AccountDAO.logger.error(f"删除账户ID={account_id}失败")
                    return False
        except Exception as e:
            AccountDAO.logger.error(f"删除账户ID={account_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_account_by_id(self, account_id):
        """
        根据账户ID查询账户
        
        Args:
            account_id: 账户ID
            
        Returns:
            tuple: 如果查询成功返回账户信息，否则返回None
        """
        AccountDAO.logger.info(f"根据账户ID查询账户: {account_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM account WHERE id = %s"
                if self.db.execute(select_query, (account_id,)):
                    account = self.db.cur.fetchone()
                    if account:
                        AccountDAO.logger.info(f"查询到账户ID={account_id}的信息")
                        return account
                    else:
                        AccountDAO.logger.info(f"未查询到账户ID={account_id}的信息")
                        return None
        except Exception as e:
            AccountDAO.logger.error(f"查询账户ID={account_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_accounts_by_user_id(self, user_id):
        """
        根据用户ID查询所有账户
        
        Args:
            user_id: 用户ID
            
        Returns:
            list: 如果查询成功返回账户列表，否则返回空列表
        """
        AccountDAO.logger.info(f"根据用户ID查询所有账户: {user_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM account WHERE user_id = %s"
                if self.db.execute(select_query, (user_id,)):
                    accounts = self.db.cur.fetchall()
                    if accounts:
                        AccountDAO.logger.info(f"查询到用户ID={user_id}的{len(accounts)}个账户")
                        return accounts
                    else:
                        AccountDAO.logger.info(f"用户ID={user_id}没有账户")
                        return []
        except Exception as e:
            AccountDAO.logger.error(f"查询用户ID={user_id}的账户时发生错误: {e}")
            return []
        finally:
            self.db.disconnect()
