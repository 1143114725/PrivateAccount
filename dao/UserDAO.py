from db.Database import Database
from utils.LogUtils import LogUtils

class UserDAO:
    """
    用户数据访问对象，封装用户相关的数据库操作
    """
    
    logger = LogUtils.get_instance('UserDAO')
    
    def __init__(self):
        """
        初始化UserDAO，创建数据库连接
        """
        UserDAO.logger.info("初始化UserDAO")
        self.db = Database()
    
    def check_username_exists(self, username):
        """
        检查用户名是否已存在
        
        Args:
            username: 要检查的用户名
            
        Returns:
            bool: 如果用户名已存在返回True，否则返回False
        """
        UserDAO.logger.info(f"检查用户名是否存在: {username}")
        try:
            if self.db.connect():
                check_query = "SELECT COUNT(*) FROM user WHERE username = %s"
                if self.db.execute(check_query, (username,)):
                    count = self.db.cur.fetchone()[0]
                    UserDAO.logger.debug(f"用户名{username}存在检查结果: {count > 0}")
                    return count > 0
            return False
        except Exception as e:
            UserDAO.logger.error(f"检查用户名存在时发生错误: {e}")
            return False
        finally:
            self.db.disconnect()
    
    def check_phone_exists(self, phone):
        """
        检查手机号是否已存在
        
        Args:
            phone: 要检查的手机号
            
        Returns:
            bool: 如果手机号已存在返回True，否则返回False
        """
        UserDAO.logger.info(f"检查手机号是否存在: {phone}")
        try:
            if self.db.connect():
                check_query = "SELECT COUNT(*) FROM user WHERE phone = %s"
                if self.db.execute(check_query, (phone,)):
                    count = self.db.cur.fetchone()[0]
                    UserDAO.logger.debug(f"手机号{phone}存在检查结果: {count > 0}")
                    return count > 0
            return False
        except Exception as e:
            UserDAO.logger.error(f"检查手机号存在时发生错误: {e}")
            return False
        finally:
            self.db.disconnect()
    
    def register_user(self, username, encrypted_password, phone, registration_time):
        """
        注册新用户
        
        Args:
            username: 用户名
            encrypted_password: 加密后的密码
            phone: 手机号
            registration_time: 注册时间戳
            
        Returns:
            bool: 如果注册成功返回True，否则返回False
        """
        UserDAO.logger.info(f"注册新用户: {username} ({phone})")
        try:
            if self.db.connect():
                insert_query = "INSERT INTO user (username, password, phone, enable, registration, refresh_token, token_expiration_time) VALUES (%s, %s, %s, TRUE, %s, NULL, NULL)"
                if self.db.execute(insert_query, (username, encrypted_password, phone, registration_time)):
                    self.db.commit()
                    UserDAO.logger.info(f"用户{username}注册成功")
                    return True
                else:
                    self.db.rollback()
                    UserDAO.logger.error(f"用户{username}注册失败: 无法插入用户信息")
                    return False
        except Exception as e:
            UserDAO.logger.error(f"用户{username}注册时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def login_user(self, username=None, phone=None, encrypted_password=None):
        """
        用户登录，支持用户名或手机号登录
        
        Args:
            username: 用户名（可选）
            phone: 手机号（可选）
            encrypted_password: 加密后的密码
            
        Returns:
            dict: 如果登录成功返回用户信息字典，否则返回None
        """
        UserDAO.logger.info(f"用户登录 - 用户名: {username}，手机号: {phone}")
        try:
            if self.db.connect():
                if phone:
                    login_query = "SELECT * FROM user WHERE phone = %s AND password = %s AND enable = TRUE"
                    if self.db.execute(login_query, (phone, encrypted_password)):
                        user = self.db.cur.fetchone()
                        if user:
                            UserDAO.logger.info(f"手机号{phone}登录成功")
                            # 更新最后登录时间
                            user_id = user[0]
                            update_query = "UPDATE user SET last_login_time = CURRENT_TIMESTAMP WHERE id = %s"
                            self.db.execute(update_query, (user_id,))
                            self.db.commit()
                            return user
                elif username:
                    login_query = "SELECT * FROM user WHERE username = %s AND password = %s AND enable = TRUE"
                    if self.db.execute(login_query, (username, encrypted_password)):
                        user = self.db.cur.fetchone()
                        if user:
                            UserDAO.logger.info(f"用户名{username}登录成功")
                            # 更新最后登录时间
                            user_id = user[0]
                            update_query = "UPDATE user SET last_login_time = CURRENT_TIMESTAMP WHERE id = %s"
                            self.db.execute(update_query, (user_id,))
                            self.db.commit()
                            return user
                UserDAO.logger.warning(f"登录失败: 用户名/手机号或密码错误 - 用户名: {username}，手机号: {phone}")
                return None
            else:
                UserDAO.logger.error("登录失败: 数据库连接失败")
                return None
        except Exception as e:
            UserDAO.logger.error(f"用户登录时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def update_token(self, user_id, token, expiration_time):
        """
        更新用户的token信息
        
        Args:
            user_id: 用户ID
            token: 新的token
            expiration_time: token过期时间戳
            
        Returns:
            bool: 更新是否成功
        """
        UserDAO.logger.info(f"更新用户token: user_id={user_id}, token={token[:10]}..., expiration_time={expiration_time}")
        try:
            if self.db.connect():
                update_query = "UPDATE user SET refresh_token = %s, token_expiration_time = %s WHERE id = %s"
                if self.db.execute(update_query, (token, expiration_time, user_id)):
                    self.db.commit()
                    UserDAO.logger.info(f"用户token更新成功: user_id={user_id}")
                    return True
                else:
                    self.db.rollback()
                    UserDAO.logger.error(f"用户token更新失败: user_id={user_id}")
                    return False
        except Exception as e:
            UserDAO.logger.error(f"更新用户token时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def get_user_by_id(self, user_id):
        """
        根据用户ID查询用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            tuple: 如果查询成功返回用户信息元组，否则返回None
        """
        UserDAO.logger.info(f"根据用户ID查询用户信息: {user_id}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM user WHERE id = %s"
                if self.db.execute(select_query, (user_id,)):
                    user = self.db.cur.fetchone()
                    if user:
                        UserDAO.logger.info(f"查询到用户ID={user_id}的信息")
                        return user
                    else:
                        UserDAO.logger.info(f"未查询到用户ID={user_id}的信息")
                        return None
        except Exception as e:
            UserDAO.logger.error(f"查询用户ID={user_id}时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_user_by_phone(self, phone):
        """
        根据手机号查询用户信息
        
        Args:
            phone: 手机号
            
        Returns:
            tuple: 如果查询成功返回用户信息元组，否则返回None
        """
        UserDAO.logger.info(f"根据手机号查询用户信息: {phone}")
        try:
            if self.db.connect():
                select_query = "SELECT * FROM user WHERE phone = %s"
                if self.db.execute(select_query, (phone,)):
                    user = self.db.cur.fetchone()
                    if user:
                        UserDAO.logger.info(f"查询到手机号={phone}的用户信息")
                        return user
                    else:
                        UserDAO.logger.info(f"未查询到手机号={phone}的用户信息")
                        return None
        except Exception as e:
            UserDAO.logger.error(f"查询手机号={phone}的用户信息时发生错误: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def delete_user(self, user_id):
        """
        根据用户ID删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 如果删除成功返回True，否则返回False
        """
        UserDAO.logger.info(f"根据用户ID删除用户: {user_id}")
        try:
            if self.db.connect():
                delete_query = "DELETE FROM user WHERE id = %s"
                if self.db.execute(delete_query, (user_id,)):
                    self.db.commit()
                    UserDAO.logger.info(f"用户ID={user_id}删除成功")
                    return True
                else:
                    self.db.rollback()
                    UserDAO.logger.error(f"用户ID={user_id}删除失败: 无法执行删除操作")
                    return False
        except Exception as e:
            UserDAO.logger.error(f"删除用户ID={user_id}时发生错误: {e}")
            if self.db.cur:
                self.db.rollback()
            return False
        finally:
            self.db.disconnect()
