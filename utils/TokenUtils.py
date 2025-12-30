#!/usr/bin/env python3
"""
Token工具类，用于生成和验证token
"""

import time
import hashlib
import random
import string
from utils.LogUtils import LogUtils

class TokenUtils:
    """
    Token工具类，提供token的生成和验证功能
    """
    
    logger = LogUtils.get_instance('TokenUtils')
    
    @staticmethod
    def generate_token(user_id, username, phone, expiration_days=7):
        """
        生成token
        
        Args:
            user_id: 用户ID
            username: 用户名
            phone: 手机号
            expiration_days: token过期天数，默认7天
            
        Returns:
            tuple: (token, 过期时间戳)
        """
        try:
            # 生成随机字符串
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            
            # 当前时间戳
            current_time = int(time.time() * 1000)
            
            # 过期时间戳
            expiration_time = current_time + (expiration_days * 24 * 60 * 60 * 1000)
            
            # 拼接token内容
            token_content = f"{user_id}|{username}|{phone}|{current_time}|{expiration_time}|{random_str}"
            
            # 使用MD5加密生成token
            token = hashlib.md5(token_content.encode('utf-8')).hexdigest()
            
            TokenUtils.logger.info(f"生成token成功: user_id={user_id}, token={token[:10]}...")
            
            return token, expiration_time
        except Exception as e:
            TokenUtils.logger.error(f"生成token失败: {e}")
            return None, None
    
    @staticmethod
    def validate_token(token, stored_token, expiration_time):
        """
        验证token
        
        Args:
            token: 要验证的token
            stored_token: 存储的token
            expiration_time: 过期时间戳
            
        Returns:
            bool: token是否有效
        """
        try:
            # 检查token是否存在
            if not token or not stored_token:
                TokenUtils.logger.warning("token或存储的token为空")
                return False
            
            # 检查token是否匹配
            TokenUtils.logger.debug(f"token比较前调试信息：")
            TokenUtils.logger.debug(f"  token: {repr(token)}")
            TokenUtils.logger.debug(f"  stored_token: {repr(stored_token)}")
            TokenUtils.logger.debug(f"  token hex: {token.encode('utf-8').hex()}")
            TokenUtils.logger.debug(f"  stored_token hex: {stored_token.encode('utf-8').hex()}")
            TokenUtils.logger.debug(f"  token length: {len(token)}")
            TokenUtils.logger.debug(f"  stored_token length: {len(stored_token)}")
            TokenUtils.logger.debug(f"  token == stored_token: {token == stored_token}")
            
            if token != stored_token:
                TokenUtils.logger.warning("token不匹配")
                return False
            
            # 检查token是否过期
            current_time = int(time.time() * 1000)
            if current_time > expiration_time:
                TokenUtils.logger.warning("token已过期")
                return False
            
            TokenUtils.logger.info("token验证成功")
            return True
        except Exception as e:
            TokenUtils.logger.error(f"验证token失败: {e}")
            return False
    
    @staticmethod
    def refresh_token(user_id, username, phone):
        """
        刷新token
        
        Args:
            user_id: 用户ID
            username: 用户名
            phone: 手机号
            
        Returns:
            tuple: (新token, 新过期时间戳)
        """
        # 直接调用生成token方法，默认7天过期
        return TokenUtils.generate_token(user_id, username, phone)
