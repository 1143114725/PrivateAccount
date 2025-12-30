from dao.AccountDAO import AccountDAO
from utils.LogUtils import LogUtils


class AccountService:
    """
    账户业务逻辑层，处理账户相关的业务规则
    """
    
    logger = LogUtils.get_instance('AccountService')
    
    def __init__(self):
        """
        初始化AccountService，创建AccountDAO实例
        """
        AccountService.logger.info("初始化AccountService")
        self.account_dao = AccountDAO()
    
    def create_account(self, user_id, account_name, balance=0):
        """
        创建新账户业务逻辑
        
        Args:
            user_id: 用户ID
            account_name: 账户名
            balance: 账户余额，默认为0
            
        Returns:
            tuple: (是否成功, 消息, 账户信息)
        """
        AccountService.logger.info(f"创建账户请求 - 用户ID: {user_id}, 账户名: {account_name}, 余额: {balance}")
        
        # 参数验证
        if not user_id:
            AccountService.logger.warning("创建账户失败: 用户ID不能为空")
            return False, "用户ID不能为空", None
        
        if not account_name:
            AccountService.logger.warning("创建账户失败: 账户名不能为空")
            return False, "账户名不能为空", None
        
        if balance < 0:
            AccountService.logger.warning(f"创建账户失败: 余额不能为负数 - {balance}")
            return False, "余额不能为负数", None
        
        # 调用DAO创建账户
        success, account_id = self.account_dao.create_account(account_name, balance, user_id)
        if success:
            # 获取创建的账户信息
            account = self.account_dao.get_account_by_id(account_id)
            if account:
                AccountService.logger.info(f"账户创建成功 - 账户ID: {account_id}, 账户名: {account_name}")
                return True, "账户创建成功", account
            else:
                AccountService.logger.error(f"账户创建成功但无法获取账户信息 - 账户ID: {account_id}")
                return True, "账户创建成功但无法获取账户信息", None
        else:
            AccountService.logger.error(f"账户创建失败 - 账户名: {account_name}")
            return False, "账户创建失败", None
    
    def update_balance(self, account_id, new_balance):
        """
        修改账户余额业务逻辑
        
        Args:
            account_id: 账户ID
            new_balance: 新的账户余额
            
        Returns:
            tuple: (是否成功, 消息, 账户信息)
        """
        AccountService.logger.info(f"修改账户余额请求 - 账户ID: {account_id}, 新余额: {new_balance}")
        
        # 参数验证
        if not account_id:
            AccountService.logger.warning("修改余额失败: 账户ID不能为空")
            return False, "账户ID不能为空", None
        
        if new_balance < 0:
            AccountService.logger.warning(f"修改余额失败: 余额不能为负数 - {new_balance}")
            return False, "余额不能为负数", None
        
        # 检查账户是否存在
        account = self.account_dao.get_account_by_id(account_id)
        if not account:
            AccountService.logger.warning(f"修改余额失败: 账户不存在 - 账户ID: {account_id}")
            return False, "账户不存在", None
        
        # 调用DAO修改余额
        if self.account_dao.update_balance(account_id, new_balance):
            # 获取更新后的账户信息
            updated_account = self.account_dao.get_account_by_id(account_id)
            AccountService.logger.info(f"账户余额修改成功 - 账户ID: {account_id}")
            return True, "账户余额修改成功", updated_account
        else:
            AccountService.logger.error(f"账户余额修改失败 - 账户ID: {account_id}")
            return False, "账户余额修改失败", None
    
    def delete_account(self, account_id):
        """
        删除账户业务逻辑
        
        Args:
            account_id: 账户ID
            
        Returns:
            tuple: (是否成功, 消息)
        """
        AccountService.logger.info(f"删除账户请求 - 账户ID: {account_id}")
        
        # 参数验证
        if not account_id:
            AccountService.logger.warning("删除账户失败: 账户ID不能为空")
            return False, "账户ID不能为空"
        
        # 检查账户是否存在
        account = self.account_dao.get_account_by_id(account_id)
        if not account:
            AccountService.logger.warning(f"删除账户失败: 账户不存在 - 账户ID: {account_id}")
            return False, "账户不存在"
        
        # 调用DAO删除账户
        if self.account_dao.delete_account(account_id):
            AccountService.logger.info(f"账户删除成功 - 账户ID: {account_id}")
            return True, "账户删除成功"
        else:
            AccountService.logger.error(f"账户删除失败 - 账户ID: {account_id}")
            return False, "账户删除失败"
    
    def get_account_by_id(self, account_id):
        """
        根据账户ID查询账户业务逻辑
        
        Args:
            account_id: 账户ID
            
        Returns:
            tuple: (是否成功, 消息, 账户信息)
        """
        AccountService.logger.info(f"查询账户请求 - 账户ID: {account_id}")
        
        # 参数验证
        if not account_id:
            AccountService.logger.warning("查询账户失败: 账户ID不能为空")
            return False, "账户ID不能为空", None
        
        # 调用DAO查询账户
        account = self.account_dao.get_account_by_id(account_id)
        if account:
            AccountService.logger.info(f"查询账户成功 - 账户ID: {account_id}")
            return True, "查询账户成功", account
        else:
            AccountService.logger.warning(f"查询账户失败: 账户不存在 - 账户ID: {account_id}")
            return False, "账户不存在", None
    
    def get_accounts_by_user_id(self, user_id):
        """
        根据用户ID查询所有账户业务逻辑
        
        Args:
            user_id: 用户ID
            
        Returns:
            tuple: (是否成功, 消息, 账户列表)
        """
        AccountService.logger.info(f"查询用户所有账户请求 - 用户ID: {user_id}")
        
        # 参数验证
        if not user_id:
            AccountService.logger.warning("查询账户失败: 用户ID不能为空")
            return False, "用户ID不能为空", []
        
        # 调用DAO查询账户列表
        accounts = self.account_dao.get_accounts_by_user_id(user_id)
        AccountService.logger.info(f"查询用户账户成功 - 用户ID: {user_id}, 账户数量: {len(accounts)}")
        return True, "查询用户账户成功", accounts