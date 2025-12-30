from flask import request, jsonify, Response
from services.UserService import UserService
from utils.LogUtils import LogUtils
from models.user_model import LoginResponseModel, RegisterResponseModel, UserInfoModel
from .account import setup_account_routes
from .consumption import setup_consumption_routes

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

# 创建UserService实例
user_service = UserService()

def setup_routes(app):
    api_logger.info("开始配置API路由")
    
    # 设置账户相关路由
    setup_account_routes(app)
    
    # 设置消费类型相关路由
    setup_consumption_routes(app)
    
    @app.route("/login", methods=["POST"])  # 改为POST方法更安全
    def login():
        api_logger.info("登录路由被调用")
        # 支持手机号或用户名登录
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        phone = request.form.get("phone", "").strip()

        # 记录登录请求
        api_logger.info(f"收到登录请求 - 用户名: {username}，手机号: {phone}")
        api_logger.info(f"password: {password}")

        try:
            # 调用UserService的login方法
            api_logger.info("调用user_service.login方法")
            success, message, user = user_service.login(username, password, phone)
            
            api_logger.info(f"login返回结果: success={success}, message={message}, user={user}")
            
            if success:
                api_logger.info("登录成功，准备返回JSON响应")
                api_logger.info(f"user的长度: {len(user)}")
                api_logger.info(f"user的内容: {user}")
                
                # 使用UserInfoModel处理用户信息
                user_info = UserInfoModel(user)
                # 使用LoginResponseModel构建响应，200表示成功
                login_response = LoginResponseModel(errorcode=200, message=message, user=user_info)
                # 转换为字典格式
                response_data = login_response.to_dict()
                
                api_logger.info(f"response_data: {response_data}")
                return jsonify(response_data), 200
            elif "用户名/手机号或密码错误" in message:
                api_logger.info("登录失败: 用户名/手机号或密码错误")
                # 使用LoginResponseModel构建失败响应，401表示身份验证失败
                login_response = LoginResponseModel(errorcode=401, message=message)
                return jsonify(login_response.to_dict()), 401
            elif "token过期" in message:
                api_logger.info("登录失败: token过期")
                # 使用LoginResponseModel构建失败响应，201表示token过期
                login_response = LoginResponseModel(errorcode=201, message=message)
                return jsonify(login_response.to_dict()), 401
            else:
                api_logger.info(f"登录失败: {message}")
                # 使用LoginResponseModel构建失败响应，400表示请求错误
                login_response = LoginResponseModel(errorcode=400, message=message)
                return jsonify(login_response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"登录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            # 使用LoginResponseModel构建异常响应，500表示服务器错误
            login_response = LoginResponseModel(errorcode=500, message=f"登录失败: {str(e)}")
            return jsonify(login_response.to_dict()), 500

    @app.route("/register", methods=["POST"])
    def register():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        phone = request.form.get("phone", "").strip()
        
        # 记录注册请求
        api_logger.info(f"收到注册请求 - 用户名: {username}，手机号: {phone}")

        try:
            # 调用UserService的register方法
            success, message = user_service.register(username, password, phone)
            
            if success:
                # 使用RegisterResponseModel构建成功响应，200表示成功
                register_response = RegisterResponseModel(errorcode=200, message=message)
                return jsonify(register_response.to_dict()), 200
            else:
                # 使用RegisterResponseModel构建失败响应，400表示请求错误
                register_response = RegisterResponseModel(errorcode=400, message=message)
                return jsonify(register_response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"注册过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            # 使用RegisterResponseModel构建异常响应，500表示服务器错误
            register_response = RegisterResponseModel(errorcode=500, message=f"注册失败: {str(e)}")
            return jsonify(register_response.to_dict()), 500
    
    api_logger.info("API路由配置完成")
