from flask import request, jsonify
from functools import wraps
from services.IncomeTypeService import IncomeTypeService
from utils.LogUtils import LogUtils
from utils.TokenUtils import TokenUtils
from services.UserService import UserService
from models.incometypemodel import IncomeTypeInfoModel, IncomeTypeResponseModel, IncomeTypesResponseModel
import time

# 创建UserService实例
user_service = UserService()

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

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
            api_logger.warning("token验证失败")
            return jsonify({"errorcode": 401, "message": "token验证失败", "data": None}), 401
    return decorated

# 创建服务实例
income_type_service = IncomeTypeService()

def setup_incometype_routes(app):
    """
    设置收入类型相关的路由
    """
    api_logger.info("开始配置收入类型API路由")
    
    @app.route("/api/incometype", methods=["POST"])
    @token_required
    def addincometype():
        """
        新增收入类型接口
        请求体：income_type_name, enable（可选，默认为True）
        """
        api_logger.info("新增收入类型路由被调用")
        
        # 从请求体中获取参数
        income_type_name = request.form.get("income_type_name", "").strip()
        enable_str = request.form.get("enable", "True").strip().lower()
        enable = enable_str in ("true", "1", "yes", "y")
        
        # 记录请求信息
        api_logger.info(f"收到新增收入类型请求 - income_type_name: {income_type_name}, enable: {enable}")
            
        try:
            # 验证参数
            if not income_type_name:
                api_logger.warning("新增收入类型失败: 收入类型说明不能为空")
                return jsonify({"errorcode": 400, "message": "收入类型说明不能为空", "data": None}), 400
            
            # 调用IncomeTypeService的create_income_type方法
            success, message, income_type = income_type_service.create_income_type(income_type_name, enable)
            
            if success:
                api_logger.info(f"收入类型新增成功 - income_type_id: {income_type[0]}")
                # 使用IncomeTypeInfoModel处理收入类型信息
                income_type_info = IncomeTypeInfoModel(income_type)
                # 使用IncomeTypeResponseModel构建响应
                response = IncomeTypeResponseModel(errorcode=200, message=message, income_type=income_type_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"收入类型新增失败 - {message}")
                response = IncomeTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"新增收入类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = IncomeTypeResponseModel(errorcode=500, message=f"新增收入类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/incometype", methods=["PUT"])
    @token_required
    def updateincometype():
        """
        修改收入类型信息接口
        请求体：id, income_type_name（可选）, enable（可选）
        """
        api_logger.info("修改收入类型路由被调用")
            
        # 从请求体中获取参数
        income_type_id_str = request.form.get("id", "").strip()
        income_type_name = request.form.get("income_type_name", None)
        enable_str = request.form.get("enable", None)
            
        # 验证并转换income_type_id
        try:
            income_type_id = int(income_type_id_str)
        except ValueError:
            api_logger.warning(f"修改收入类型失败: 收入类型ID不是有效的整数 - {income_type_id_str}")
            return jsonify({"errorcode": 400, "message": "收入类型ID必须是有效的整数", "data": None}), 400
            
        # 处理enable参数
        enable = None
        if enable_str is not None:
            enable_str = enable_str.strip().lower()
            enable = enable_str in ("true", "1", "yes", "y")
            
        # 记录请求信息
        api_logger.info(f"收到修改收入类型请求 - income_type_id: {income_type_id}, income_type_name: {income_type_name}, enable: {enable}")
            
        try:
            # 验证参数
            if income_type_name is not None:
                income_type_name = income_type_name.strip()
                if not income_type_name:
                    api_logger.warning("修改收入类型失败: 收入类型说明不能为空")
                    return jsonify({"errorcode": 400, "message": "收入类型说明不能为空", "data": None}), 400
            
            # 调用IncomeTypeService的update_income_type方法
            success, message, income_type = income_type_service.update_income_type(income_type_id, income_type_name, enable)
            
            if success:
                api_logger.info(f"收入类型修改成功 - id: {income_type_id}")
                # 使用IncomeTypeInfoModel处理收入类型信息
                income_type_info = IncomeTypeInfoModel(income_type)
                # 使用IncomeTypeResponseModel构建响应
                response = IncomeTypeResponseModel(errorcode=200, message=message, income_type=income_type_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"收入类型修改失败 - {message}")
                response = IncomeTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"修改收入类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = IncomeTypeResponseModel(errorcode=500, message=f"修改收入类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/incometype", methods=["DELETE"])
    @token_required
    def deleteincometype():
        """
        删除收入类型接口
        请求体：id
        """
        api_logger.info("删除收入类型路由被调用")
        
        # 从请求体中获取参数
        income_type_id_str = request.form.get("id", "").strip()
        
        # 验证并转换income_type_id
        try:
            income_type_id = int(income_type_id_str)
        except ValueError:
            api_logger.warning(f"删除收入类型失败: 收入类型ID不是有效的整数 - {income_type_id_str}")
            return jsonify({"errorcode": 400, "message": "收入类型ID必须是有效的整数", "data": None}), 400
        
        # 记录请求信息
        api_logger.info(f"收到删除收入类型请求 - income_type_id: {income_type_id}")
        
        try:
            # 调用IncomeTypeService的delete_income_type方法
            success, message = income_type_service.delete_income_type(income_type_id)
            
            if success:
                api_logger.info(f"收入类型删除成功 - income_type_id: {income_type_id}")
                # 使用IncomeTypeResponseModel构建响应
                response = IncomeTypeResponseModel(errorcode=200, message=message)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"收入类型删除失败 - {message}")
                response = IncomeTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"删除收入类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = IncomeTypeResponseModel(errorcode=500, message=f"删除收入类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/incometype", methods=["GET"])
    @token_required
    def getincometypes():
        """
        查询收入类型接口
        查询参数：id（可选），如果不传id或id为空则查询所有收入类型
        无论是否传入id，都返回数组格式
        """
        api_logger.info("查询收入类型路由被调用")
        
        # 从查询参数中获取参数
        income_type_id_str = request.args.get("id", None)
        
        # 处理id参数为空的情况，与不传递id时的处理逻辑一致
        if income_type_id_str == "":
            income_type_id_str = None
        
        # 记录请求信息
        api_logger.info(f"收到查询收入类型请求 - id: {income_type_id_str}")
        
        try:
            if income_type_id_str is not None:
                # 查询单个收入类型
                try:
                    income_type_id = int(income_type_id_str)
                except ValueError:
                    api_logger.warning(f"查询收入类型失败: 收入类型ID不是有效的整数 - {income_type_id_str}")
                    return jsonify({"errorcode": 400, "message": "收入类型ID必须是有效的整数", "data": None}), 400
                
                # 调用IncomeTypeService的get_income_type_by_id方法
                success, message, income_type = income_type_service.get_income_type_by_id(income_type_id)
                
                if success:
                    api_logger.info(f"查询单个收入类型成功 - income_type_id: {income_type_id}")
                    # 使用IncomeTypeInfoModel处理收入类型信息，并包装成数组
                    income_type_info = IncomeTypeInfoModel(income_type)
                    income_type_infos = [income_type_info]
                    # 使用IncomeTypesResponseModel构建响应
                    response = IncomeTypesResponseModel(errorcode=200, message=message, income_types=income_type_infos)
                    return jsonify(response.to_dict()), 200
                else:
                    api_logger.error(f"查询单个收入类型失败 - {message}")
                    response = IncomeTypesResponseModel(errorcode=404, message=message)
                    return jsonify(response.to_dict()), 404
            else:
                # 查询所有收入类型
                # 调用IncomeTypeService的get_all_income_types方法
                success, message, income_types = income_type_service.get_all_income_types()
                
                if success:
                    api_logger.info(f"查询所有收入类型成功 - 收入类型数量: {len(income_types)}")
                    # 使用IncomeTypeInfoModel处理收入类型信息列表
                    income_type_infos = [IncomeTypeInfoModel(income_type) for income_type in income_types]
                    # 使用IncomeTypesResponseModel构建响应
                    response = IncomeTypesResponseModel(errorcode=200, message=message, income_types=income_type_infos)
                    return jsonify(response.to_dict()), 200
                else:
                    api_logger.error(f"查询所有收入类型失败 - {message}")
                    response = IncomeTypesResponseModel(errorcode=400, message=message)
                    return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"查询收入类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = IncomeTypesResponseModel(errorcode=500, message=f"查询收入类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    api_logger.info("收入类型API路由配置完成")
