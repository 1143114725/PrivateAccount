from flask import request, jsonify, Response
from services.AccountService import AccountService
from services.UserService import UserService
from utils.LogUtils import LogUtils
from utils.TokenUtils import TokenUtils
from models.account_model import AccountInfoModel, AccountResponseModel, AccountsResponseModel
from functools import wraps
import time

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

# 创建服务实例
account_service = AccountService()
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
        
        # 简化调试信息，只打印user元组结构
        api_logger.info(f"调试信息 - user元组长度: {len(user)}")
        for i, item in enumerate(user):
            api_logger.info(f"调试信息 - user[{i}]: {item}, 类型: {type(item)}")
        
        # 从user元组中获取token和过期时间 - 根据实际查询结果设置正确的索引
        stored_token = user[4]  # refresh_token
        token_expiration_time = user[5]  # token_expiration_time
        
        # 确保stored_token是字符串类型
        if stored_token is not None:
            stored_token = str(stored_token)
        
        # 调试信息：打印token比较
        api_logger.info(f"调试信息 - 传入的token: {token}, 类型: {type(token)}, 长度: {len(token)}")
        api_logger.info(f"调试信息 - 存储的token: {stored_token}, 类型: {type(stored_token)}, 长度: {len(str(stored_token)) if stored_token is not None else 0}")
        api_logger.info(f"调试信息 - token_expiration_time: {token_expiration_time}, 类型: {type(token_expiration_time)}")
        api_logger.info(f"调试信息 - 当前时间戳: {int(time.time() * 1000)}")
        
        # 验证token
        if TokenUtils.validate_token(token, stored_token, token_expiration_time):
            api_logger.info("token验证成功")
            return f(*args, **kwargs)
        else:
            api_logger.warning("token验证失败: token无效或已过期")
            return jsonify({"errorcode": 401, "message": "无效或已过期的token", "data": None}), 401
    
    return decorated

def setup_account_routes(app):
    """
    设置账户相关的路由
    """
    api_logger.info("开始配置账户API路由")
    
    @app.route("/api/account", methods=["POST"])
    @token_required
    def add_account():
        """
        添加账户接口
        请求头：token, userid
        请求体：account_name, balance（可选，默认为0）
        """
        api_logger.info("添加账户路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        account_name = request.form.get("account_name", "").strip()
        balance = request.form.get("balance", "0")
        
        # 记录请求信息
        api_logger.info(f"收到添加账户请求 - user_id: {user_id}, account_name: {account_name}, balance: {balance}")
        
        try:
            # 验证参数
            if not account_name:
                api_logger.warning("添加账户失败: 账户名不能为空")
                return jsonify({"errorcode": 400, "message": "账户名不能为空", "data": None}), 400
            
            # 转换余额为小数（自动截取两位小数）
            try:
                balance = float(balance)
                # 自动截取两位小数
                balance = round(balance, 2)
            except ValueError:
                api_logger.warning(f"添加账户失败: 余额不是有效的数字 - {balance}")
                return jsonify({"errorcode": 400, "message": "余额必须是有效的数字", "data": None}), 400
            
            # 调用AccountService的create_account方法
            success, message, account = account_service.create_account(user_id, account_name, balance)
            
            if success:
                api_logger.info(f"账户添加成功 - account_id: {account[0]}")
                # 使用AccountInfoModel处理账户信息
                account_info = AccountInfoModel(account)
                # 使用AccountResponseModel构建响应
                response = AccountResponseModel(errorcode=200, message=message, account=account_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"账户添加失败 - {message}")
                response = AccountResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"添加账户过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = AccountResponseModel(errorcode=500, message=f"添加账户失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/account/balance", methods=["PUT"])
    @token_required
    def update_account_balance():
        """
        修改账户余额接口
        请求头：token, userid
        请求体：account_id, new_balance
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        account_id = request.form.get("account_id", "")
        new_balance = request.form.get("new_balance", "")
        
        # 验证并转换account_id
        try:
            account_id = int(account_id)
        except ValueError:
            api_logger.warning(f"修改账户余额失败: 账户ID不是有效的整数 - {account_id}")
            return jsonify({"errorcode": 400, "message": "账户ID必须是有效的整数", "data": None}), 400
        
        api_logger.info(f"修改账户余额路由被调用 - account_id: {account_id}")
        
        # 记录请求信息
        api_logger.info(f"收到修改账户余额请求 - account_id: {account_id}, new_balance: {new_balance}")
        
        try:
            # 验证参数
            if not new_balance:
                api_logger.warning("修改账户余额失败: 新余额不能为空")
                return jsonify({"errorcode": 400, "message": "新余额不能为空", "data": None}), 400
            
            # 转换余额为小数（自动截取两位小数）
            try:
                new_balance = float(new_balance)
                # 自动截取两位小数
                new_balance = round(new_balance, 2)
            except ValueError:
                api_logger.warning(f"修改账户余额失败: 新余额不是有效的数字 - {new_balance}")
                return jsonify({"errorcode": 400, "message": "新余额必须是有效的数字", "data": None}), 400
            
            # 检查账户是否存在且属于该用户
            account = account_service.get_account_by_id(account_id)[2]
            if not account:
                api_logger.warning(f"修改账户余额失败: 账户不存在 - account_id: {account_id}")
                return jsonify({"errorcode": 404, "message": "账户不存在", "data": None}), 404
            
            if account[3] != user_id:
                api_logger.warning(f"修改账户余额失败: 账户不属于该用户 - account_id: {account_id}, user_id: {user_id}")
                return jsonify({"errorcode": 403, "message": "无权操作此账户", "data": None}), 403
            
            # 调用AccountService的update_balance方法
            success, message, updated_account = account_service.update_balance(account_id, new_balance)
            
            if success:
                api_logger.info(f"账户余额修改成功 - account_id: {account_id}, new_balance: {new_balance}")
                # 使用AccountInfoModel处理账户信息
                account_info = AccountInfoModel(updated_account)
                # 使用AccountResponseModel构建响应
                response = AccountResponseModel(errorcode=200, message=message, account=account_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"账户余额修改失败 - {message}")
                response = AccountResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"修改账户余额过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = AccountResponseModel(errorcode=500, message=f"修改账户余额失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/account", methods=["DELETE"])
    @token_required
    def delete_account():
        """
        删除账户接口
        请求头：token, userid
        请求体：account_id
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        account_id = request.form.get("account_id", "")
        
        # 验证并转换account_id
        try:
            account_id = int(account_id)
        except ValueError:
            api_logger.warning(f"删除账户失败: 账户ID不是有效的整数 - {account_id}")
            return jsonify({"errorcode": 400, "message": "账户ID必须是有效的整数", "data": None}), 400
        
        api_logger.info(f"删除账户路由被调用 - account_id: {account_id}")
        
        # 记录请求信息
        api_logger.info(f"收到删除账户请求 - account_id: {account_id}, user_id: {user_id}")
        
        try:
            # 检查账户是否存在且属于该用户
            account = account_service.get_account_by_id(account_id)[2]
            if not account:
                api_logger.warning(f"删除账户失败: 账户不存在 - account_id: {account_id}")
                return jsonify({"errorcode": 404, "message": "账户不存在", "data": None}), 404
            
            if account[3] != user_id:
                api_logger.warning(f"删除账户失败: 账户不属于该用户 - account_id: {account_id}, user_id: {user_id}")
                return jsonify({"errorcode": 403, "message": "无权操作此账户", "data": None}), 403
            
            # 调用AccountService的delete_account方法
            success, message = account_service.delete_account(account_id)
            
            if success:
                api_logger.info(f"账户删除成功 - account_id: {account_id}")
                # 使用AccountResponseModel构建响应
                response = AccountResponseModel(errorcode=200, message=message)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"账户删除失败 - {message}")
                response = AccountResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"删除账户过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = AccountResponseModel(errorcode=500, message=f"删除账户失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/account", methods=["GET"])
    @token_required
    def get_user_accounts():
        """
        查询用户所有账户接口
        请求头：token, userid
        """
        api_logger.info("查询用户账户路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 记录请求信息
        api_logger.info(f"收到查询用户账户请求 - user_id: {user_id}")
        
        try:
            # 调用AccountService的get_accounts_by_user_id方法
            success, message, accounts = account_service.get_accounts_by_user_id(user_id)
            
            if success:
                api_logger.info(f"查询用户账户成功 - user_id: {user_id}, 账户数量: {len(accounts)}")
                # 使用AccountInfoModel处理账户信息列表
                account_infos = [AccountInfoModel(account) for account in accounts]
                # 使用AccountsResponseModel构建响应
                response = AccountsResponseModel(errorcode=200, message=message, accounts=account_infos)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"查询用户账户失败 - {message}")
                response = AccountsResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"查询用户账户过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = AccountsResponseModel(errorcode=500, message=f"查询用户账户失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/account/single", methods=["GET"])
    @token_required
    def get_account_by_id():
        """
        根据账户ID查询账户接口
        请求头：token, userid
        查询参数：account_id
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从查询参数中获取参数
        account_id = request.args.get("account_id", "")
        
        # 验证并转换account_id
        try:
            account_id = int(account_id)
        except ValueError:
            api_logger.warning(f"查询账户失败: 账户ID不是有效的整数 - {account_id}")
            return jsonify({"errorcode": 400, "message": "账户ID必须是有效的整数", "data": None}), 400
        
        api_logger.info(f"查询单个账户路由被调用 - account_id: {account_id}")
        
        # 记录请求信息
        api_logger.info(f"收到查询单个账户请求 - account_id: {account_id}, user_id: {user_id}")
        
        try:
            # 调用AccountService的get_account_by_id方法
            success, message, account = account_service.get_account_by_id(account_id)
            
            if success:
                # 检查账户是否属于该用户
                if account[3] != user_id:
                    api_logger.warning(f"查询账户失败: 账户不属于该用户 - account_id: {account_id}, user_id: {user_id}")
                    return jsonify({"errorcode": 403, "message": "无权访问此账户", "data": None}), 403
                
                api_logger.info(f"查询账户成功 - account_id: {account_id}")
                # 使用AccountInfoModel处理账户信息
                account_info = AccountInfoModel(account)
                # 使用AccountResponseModel构建响应
                response = AccountResponseModel(errorcode=200, message=message, account=account_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"查询账户失败 - {message}")
                response = AccountResponseModel(errorcode=404, message=message)
                return jsonify(response.to_dict()), 404
        except Exception as e:
            api_logger.error(f"查询账户过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = AccountResponseModel(errorcode=500, message=f"查询账户失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    api_logger.info("账户API路由配置完成")