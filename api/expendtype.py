from flask import request, jsonify
from functools import wraps
from services.ExpendTypeService import ExpendTypeService
from utils.LogUtils import LogUtils
from utils.TokenUtils import TokenUtils
from services.UserService import UserService
from models.expendtypemodel import ExpendTypeInfoModel, ExpendTypeResponseModel, ExpendTypesResponseModel
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
expend_type_service = ExpendTypeService()

def setup_expendtype_routes(app):
    """
    设置消费类型相关的路由
    """
    api_logger.info("开始配置消费类型API路由")
    
    @app.route("/api/expendtype", methods=["POST"])
    @token_required
    def addexpendtype():
        """
        新增消费类型接口
        请求体：type_name, enable（可选，默认为True）
        """
        api_logger.info("新增消费类型路由被调用")
        
        # 从请求体中获取参数
        expend_type_name = request.form.get("expend_type_name", "").strip()
        enable_str = request.form.get("enable", "True").strip().lower()
        enable = enable_str in ("true", "1", "yes", "y")
        
        # 记录请求信息
        api_logger.info(f"收到新增消费类型请求 - expend_type_name: {expend_type_name}, enable: {enable}")
            
        try:
            # 验证参数
            if not expend_type_name:
                api_logger.warning("新增消费类型失败: 消费类型说明不能为空")
                return jsonify({"errorcode": 400, "message": "消费类型说明不能为空", "data": None}), 400
            
            # 调用ExpendTypeService的create_expend_type方法
            success, message, expend_type = expend_type_service.create_expend_type(expend_type_name, enable)
            
            if success:
                api_logger.info(f"消费类型新增成功 - expenditure_type_id: {expend_type[0]}")
                # 使用ExpendTypeInfoModel处理消费类型信息
                expend_type_info = ExpendTypeInfoModel(expend_type)
                # 使用ExpendTypeResponseModel构建响应
                response = ExpendTypeResponseModel(errorcode=200, message=message, expend_type=expend_type_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"消费类型新增失败 - {message}")
                response = ExpendTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"新增消费类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = ExpendTypeResponseModel(errorcode=500, message=f"新增消费类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/expendtype", methods=["PUT"])
    @token_required
    def updateexpendtype():
        """
        修改消费类型信息接口
        请求体：consumption_id, type_name（可选）, enable（可选）
        """
        api_logger.info("修改消费类型路由被调用")
            
        # 从请求体中获取参数
        expend_type_id_str = request.form.get("id", "").strip()
        expend_type_name = request.form.get("expend_type_name", None)
        enable_str = request.form.get("enable", None)
            
        # 验证并转换expend_type_id
        try:
            expend_type_id = int(expend_type_id_str)
        except ValueError:
            api_logger.warning(f"修改消费类型失败: 消费类型ID不是有效的整数 - {expend_type_id_str}")
            return jsonify({"errorcode": 400, "message": "消费类型ID必须是有效的整数", "data": None}), 400
            
        # 处理enable参数
        enable = None
        if enable_str is not None:
            enable_str = enable_str.strip().lower()
            enable = enable_str in ("true", "1", "yes", "y")
            
        # 记录请求信息
        api_logger.info(f"收到修改消费类型请求 - expend_type_id: {expend_type_id}, expend_type_name: {expend_type_name}, enable: {enable}")
            
        try:
            # 验证参数
            if expend_type_name is not None:
                expend_type_name = expend_type_name.strip()
                if not expend_type_name:
                    api_logger.warning("修改消费类型失败: 消费类型说明不能为空")
                    return jsonify({"errorcode": 400, "message": "消费类型说明不能为空", "data": None}), 400
            
            # 调用ExpendTypeService的update_expend_type方法
            success, message, expend_type = expend_type_service.update_expend_type(expend_type_id, expend_type_name, enable)
            
            if success:
                api_logger.info(f"消费类型修改成功 - id: {expend_type_id}")
                # 使用ExpendTypeInfoModel处理消费类型信息
                expend_type_info = ExpendTypeInfoModel(expend_type)
                # 使用ExpendTypeResponseModel构建响应
                response = ExpendTypeResponseModel(errorcode=200, message=message, expend_type=expend_type_info)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"消费类型修改失败 - {message}")
                response = ExpendTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"修改消费类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = ExpendTypeResponseModel(errorcode=500, message=f"修改消费类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/expendtype", methods=["DELETE"])
    @token_required
    def deleteexpendtype():
        """
        删除消费类型接口
        请求体：id
        """
        api_logger.info("删除消费类型路由被调用")
        
        # 从请求体中获取参数
        expend_type_id_str = request.form.get("id", "").strip()
        
        # 验证并转换expend_type_id
        try:
            expend_type_id = int(expend_type_id_str)
        except ValueError:
            api_logger.warning(f"删除消费类型失败: 消费类型ID不是有效的整数 - {expend_type_id_str}")
            return jsonify({"errorcode": 400, "message": "消费类型ID必须是有效的整数", "data": None}), 400
        
        # 记录请求信息
        api_logger.info(f"收到删除消费类型请求 - expend_type_id: {expend_type_id}")
        
        try:
            # 调用ExpendTypeService的delete_expend_type方法
            success, message = expend_type_service.delete_expend_type(expend_type_id)
            
            if success:
                api_logger.info(f"消费类型删除成功 - expend_type_id: {expend_type_id}")
                # 使用ExpendTypeResponseModel构建响应
                response = ExpendTypeResponseModel(errorcode=200, message=message)
                return jsonify(response.to_dict()), 200
            else:
                api_logger.error(f"消费类型删除失败 - {message}")
                response = ExpendTypeResponseModel(errorcode=400, message=message)
                return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"删除消费类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = ExpendTypeResponseModel(errorcode=500, message=f"删除消费类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    @app.route("/api/expendtype", methods=["GET"])
    @token_required
    def getexpendtypes():
        """
        查询消费类型接口
        查询参数：id（可选），如果不传id或id为空则查询所有消费类型
        无论是否传入id，都返回数组格式
        """
        api_logger.info("查询消费类型路由被调用")
        
        # 从查询参数中获取参数
        expend_type_id_str = request.args.get("id", None)
        
        # 处理id参数为空的情况，与不传递id时的处理逻辑一致
        if expend_type_id_str == "":
            expend_type_id_str = None
        
        # 记录请求信息
        api_logger.info(f"收到查询消费类型请求 - id: {expend_type_id_str}")
        
        try:
            if expend_type_id_str is not None:
                # 查询单个消费类型
                try:
                    expend_type_id = int(expend_type_id_str)
                except ValueError:
                    api_logger.warning(f"查询消费类型失败: 消费类型ID不是有效的整数 - {expend_type_id_str}")
                    return jsonify({"errorcode": 400, "message": "消费类型ID必须是有效的整数", "data": None}), 400
                
                # 调用ExpendTypeService的get_expend_type_by_id方法
                success, message, expend_type = expend_type_service.get_expend_type_by_id(expend_type_id)
                
                if success:
                    api_logger.info(f"查询单个消费类型成功 - expend_type_id: {expend_type_id}")
                    # 使用ExpendTypeInfoModel处理消费类型信息，并包装成数组
                    expend_type_info = ExpendTypeInfoModel(expend_type)
                    expend_type_infos = [expend_type_info]
                    # 使用ExpendTypesResponseModel构建响应
                    response = ExpendTypesResponseModel(errorcode=200, message=message, expend_types=expend_type_infos)
                    return jsonify(response.to_dict()), 200
                else:
                    api_logger.error(f"查询单个消费类型失败 - {message}")
                    response = ExpendTypesResponseModel(errorcode=404, message=message)
                    return jsonify(response.to_dict()), 404
            else:
                # 查询所有消费类型
                # 调用ExpendTypeService的get_all_expend_types方法
                success, message, expend_types = expend_type_service.get_all_expend_types()
                
                if success:
                    api_logger.info(f"查询所有消费类型成功 - 消费类型数量: {len(expend_types)}")
                    # 使用ExpendTypeInfoModel处理消费类型信息列表
                    expend_type_infos = [ExpendTypeInfoModel(expend_type) for expend_type in expend_types]
                    # 使用ExpendTypesResponseModel构建响应
                    response = ExpendTypesResponseModel(errorcode=200, message=message, expend_types=expend_type_infos)
                    return jsonify(response.to_dict()), 200
                else:
                    api_logger.error(f"查询所有消费类型失败 - {message}")
                    response = ExpendTypesResponseModel(errorcode=400, message=message)
                    return jsonify(response.to_dict()), 400
        except Exception as e:
            api_logger.error(f"查询消费类型过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            response = ExpendTypesResponseModel(errorcode=500, message=f"查询消费类型失败: {str(e)}")
            return jsonify(response.to_dict()), 500
    
    api_logger.info("消费类型API路由配置完成")
