from dao.UserDAO import UserDAO
from utils.MD5Utils import MD5Utils
from utils.LogUtils import LogUtils
from utils.TokenUtils import TokenUtils
import re
import time

class UserService:
    """
    用户业务逻辑层，处理用户注册和登录的业务规则
    """
    
    logger = LogUtils.get_instance('UserService')
    
    def __init__(self):
        """
        初始化UserService，创建UserDAO实例
        """
        UserService.logger.info("初始化UserService")
        self.user_dao = UserDAO()
    
    def validate_phone(self, phone):
        """
        验证手机号格式（中国手机号）
        
        Args:
            phone: 要验证的手机号
            
        Returns:
            bool: 如果手机号格式正确返回True，否则返回False
        """
        phone_pattern = r'^1[3-9]\d{9}$'
        return re.match(phone_pattern, phone) is not None
    
    def register(self, username, password, phone):
        """
        用户注册业务逻辑
        
        Args:
            username: 用户名
            password: 密码
            phone: 手机号
            
        Returns:
            tuple: (是否成功, 消息)
        """
        UserService.logger.info(f"用户注册请求 - 用户名: {username}，手机号: {phone}")
        
        # 参数验证
        if not username:
            UserService.logger.warning("注册失败: 用户名不能为空")
            return False, "用户名不能为空"
        
        if not password:
            UserService.logger.warning("注册失败: 密码不能为空")
            return False, "密码不能为空"
        
        if not phone:
            UserService.logger.warning("注册失败: 手机号不能为空")
            return False, "手机号不能为空"
        
        if not self.validate_phone(phone):
            UserService.logger.warning(f"注册失败: 手机号格式不正确 - {phone}")
            return False, "手机号格式不正确"
        
        # 检查用户名是否已存在
        if self.user_dao.check_username_exists(username):
            UserService.logger.warning(f"注册失败: 用户名已存在 - {username}")
            return False, "用户名已存在"
        
        # 检查手机号是否已存在
        if self.user_dao.check_phone_exists(phone):
            UserService.logger.warning(f"注册失败: 手机号已存在 - {phone}")
            return False, "手机号已存在"
        
        # 密码加密
        encrypted_password = MD5Utils.encrypt(password)
        UserService.logger.debug("密码加密完成")
        
        # 生成注册时间戳
        registration_time = int(time.time() * 1000)
        
        # 调用DAO进行注册
        if self.user_dao.register_user(username, encrypted_password, phone, registration_time):
            UserService.logger.info(f"用户注册成功: {username} ({phone})")
            
            # 注册成功后获取用户信息
            user = self.user_dao.get_user_by_phone(phone)
            if user:
                # 返回用户信息：id, username, phone, registration
                UserService.logger.info(f"获取注册用户信息成功 - 用户ID: {user[0]}")
                return True, "注册成功", (user[0], user[1], user[3], user[6])
            else:
                UserService.logger.error(f"用户注册成功但无法获取用户信息: {username} ({phone})")
                return True, "注册成功但无法获取用户信息", None
        else:
            UserService.logger.error(f"用户注册失败: {username} ({phone})")
            return False, "注册失败: 无法插入用户信息", None
    
    def login(self, username=None, password=None, phone=None):
        """
        用户登录业务逻辑
        
        Args:
            username: 用户名（可选）
            password: 密码
            phone: 手机号（可选）
            
        Returns:
            tuple: (是否成功, 消息, 用户信息)
        """
        print(f"DEBUG: 用户登录请求 - 用户名: {username}，手机号: {phone}")
        UserService.logger.info(f"用户登录请求 - 用户名: {username}，手机号: {phone}")
        
        # 参数验证
        if not password:
            print("DEBUG: 登录失败: 密码不能为空")
            UserService.logger.warning("登录失败: 密码不能为空")
            return False, "密码不能为空", None
        
        if not username and not phone:
            print("DEBUG: 登录失败: 用户名或手机号不能为空")
            UserService.logger.warning("登录失败: 用户名或手机号不能为空")
            return False, "用户名或手机号不能为空", None
        
        # 密码加密
        encrypted_password = MD5Utils.encrypt(password)
        print(f"DEBUG: 密码加密完成，加密后: {encrypted_password}")
        UserService.logger.debug("密码加密完成")
        
        # 调用DAO进行登录
        print("DEBUG: 调用DAO进行登录")
        user = self.user_dao.login_user(username=username, phone=phone, encrypted_password=encrypted_password)
        print(f"DEBUG: DAO返回的用户信息: {user}")
        
        if user:
            print(f"DEBUG: 用户登录成功 - 用户名: {username}，手机号: {phone}")
            UserService.logger.info(f"用户登录成功 - 用户名: {username}，手机号: {phone}")
            
            # 生成token
            user_id = user[0]  # user是一个元组，第一个元素是id
            print(f"DEBUG: 生成token，user_id: {user_id}, username: {user[1]}, phone: {user[3]}")
            token, token_expiration_time = TokenUtils.generate_token(user_id, user[1], user[3])  # user[1]是username，user[3]是phone
            print(f"DEBUG: token生成结果: token={token}, expiration={token_expiration_time}")
            
            if token:
                # 更新token到数据库
                print(f"DEBUG: 更新token到数据库，user_id: {user_id}, token: {token}, expiration: {token_expiration_time}")
                update_result = self.user_dao.update_token(user_id, token, token_expiration_time)
                print(f"DEBUG: token更新结果: {update_result}")
                if update_result:
                    print(f"DEBUG: 用户token更新成功 - user_id: {user_id}")
                    UserService.logger.info(f"用户token更新成功 - user_id: {user_id}")
                    # 返回用户信息时包含token
                    user_with_token = list(user) + [token, token_expiration_time]
                    print(f"DEBUG: 返回的用户信息 - user_with_token长度: {len(user_with_token)}")
                    print(f"DEBUG: 返回的用户信息 - user_with_token内容: {user_with_token}")
                    # 打印每个元素及其类型
                    for i, item in enumerate(user_with_token):
                        print(f"DEBUG: user_with_token[{i}]: {item}, 类型: {type(item)}")
                    return True, "login success", user_with_token
                else:
                    print(f"DEBUG: 用户token更新失败 - user_id: {user_id}")
                    UserService.logger.error(f"用户token更新失败 - user_id: {user_id}")
                    return False, "登录失败: token更新失败", None
            else:
                print(f"DEBUG: 用户token生成失败 - user_id: {user_id}")
                UserService.logger.error(f"用户token生成失败 - user_id: {user_id}")
                return False, "登录失败: token生成失败", None
        else:
            print(f"DEBUG: 登录失败: 用户名/手机号或密码错误 - 用户名: {username}，手机号: {phone}")
            UserService.logger.warning(f"登录失败: 用户名/手机号或密码错误 - 用户名: {username}，手机号: {phone}")
            return False, "用户名/手机号或密码错误", None
    
    def get_user_by_id(self, user_id):
        """
        根据用户ID查询用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            tuple: 如果查询成功返回用户信息元组，否则返回None
        """
        UserService.logger.info(f"根据用户ID查询用户信息: {user_id}")
        try:
            # 调用DAO查询用户
            user = self.user_dao.get_user_by_id(user_id)
            if user:
                UserService.logger.info(f"查询用户成功 - 用户ID: {user_id}")
                return user
            else:
                UserService.logger.warning(f"查询用户失败: 用户不存在 - 用户ID: {user_id}")
                return None
        except Exception as e:
            UserService.logger.error(f"查询用户时发生错误: {e}")
            return None
