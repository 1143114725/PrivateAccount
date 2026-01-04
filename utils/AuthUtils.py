from flask import request, jsonify
from functools import wraps
from services.UserService import UserService
from utils.LogUtils import LogUtils
from utils.TokenUtils import TokenUtils

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

# 创建UserService实例
user_service = UserService()

# 鉴权装饰器
def token_required(f):
    """
    验证token的装饰器
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # 从header中获取token和user_id
        token = request.headers.get('token', '').strip()
        user_id_header = request.headers.get('userid', '').strip()
        
        # 确保token是字符串类型
        token = str(token)
        
        api_logger.info(f"开始token验证 - token: {token[:10]}..., user_id_header: {user_id_header}")
        
        # 验证token和user_id是否存在
        if not token:
            api_logger.warning("token验证失败: token为空")
            return jsonify({"errorcode": 401, "message": "未提供token", "data": None}), 401
        
        if not user_id_header:
            api_logger.warning("token验证失败: userid为空")
            return jsonify({"errorcode": 401, "message": "未提供userid", "data": None}), 401
        
        try:
            user_id = int(user_id_header)
        except ValueError:
            api_logger.warning("token验证失败: userid不是有效的整数")
            return jsonify({"errorcode": 401, "message": "无效的userid", "data": None}), 401
        
        # 根据user_id查询用户信息
        user = user_service.get_user_by_id(user_id)
        if not user:
            api_logger.warning(f"token验证失败: 用户不存在 - user_id: {user_id}")
            return jsonify({"errorcode": 401, "message": "用户不存在", "data": None}), 401
        
        # 从user元组中获取token和过期时间
        stored_token = user[4]  # refresh_token
        token_expiration_time = user[5]  # token_expiration_time
        
        # 确保stored_token是字符串类型
        if stored_token is not None:
            stored_token = str(stored_token)
        
        # 验证token
        if TokenUtils.validate_token(token, stored_token, token_expiration_time):
            api_logger.info("token验证成功")
            return f(*args, **kwargs)
        else:
            api_logger.warning("token验证失败: token无效或已过期")
            return jsonify({"errorcode": 401, "message": "无效或已过期的token", "data": None}), 401
    
    return decorated
