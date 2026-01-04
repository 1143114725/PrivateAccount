from flask import request, jsonify
from functools import wraps
from services.ExpendService import ExpendService
from utils.LogUtils import LogUtils
from utils.AuthUtils import token_required
from utils.TimeUtils import TimeUtils
from datetime import datetime

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

# 创建ExpendService实例
expend_service = ExpendService()

def setup_expend_routes(app):
    """
    设置支出相关的路由
    """
    api_logger.info("开始配置支出API路由")
    
    @app.route("/api/expend", methods=["POST"])
    @token_required
    def create_expend():
        """
        新增支出记录接口
        请求头：token, userid
        请求体：money, account_id, remark, expend_time, expend_type_id
        """
        api_logger.info("新增支出记录路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        money = request.form.get("money", None)
        account_id = request.form.get("account_id", None)
        remark = request.form.get("remark", None)
        expend_time = request.form.get("expend_time", None)
        expend_type_id = request.form.get("expend_type_id", None)
        enable = request.form.get("enable", "True")
        
        # 记录新增支出请求
        api_logger.info(f"收到新增支出请求 - user_id: {user_id}, money: {money}, account_id: {account_id}, remark: {remark}, expend_time: {expend_time}, expend_type_id: {expend_type_id}, enable: {enable}")
        
        try:
            # 验证必填参数
            missing_params = []
            if not money:
                missing_params.append("money")
            if not account_id:
                missing_params.append("account_id")
            if not expend_type_id:
                missing_params.append("expend_type_id")
            
            if missing_params:
                return jsonify({"errorcode": 400, "message": f"参数 {', '.join(missing_params)} 不能为空", "data": None}), 400
            
            # 转换参数类型
            money = float(money.strip()) if money.strip() else None
            account_id = int(account_id.strip()) if account_id.strip() else None
            expend_type_id = int(expend_type_id.strip()) if expend_type_id.strip() else None
            enable = enable.strip().lower() in ['true', '1', 'yes']
            if remark is not None:
                remark = remark.strip()
            
            # 处理时间参数 - 支持毫秒级时间戳或时间字符串
            if expend_time is not None and expend_time.strip():
                expend_time_str = expend_time.strip()
                # 尝试解析为毫秒级时间戳
                try:
                    expend_time_ms = int(expend_time_str)
                    # 转换为datetime对象
                    expend_time_dt = TimeUtils.milliseconds_to_datetime(expend_time_ms)
                except ValueError:
                    # 如果不是数字，尝试作为时间字符串解析
                    try:
                        # 支持多种常见的时间字符串格式
                        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
                        for fmt in formats:
                            try:
                                expend_time_dt = datetime.strptime(expend_time_str, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError("Unsupported time format")
                    except ValueError:
                        return jsonify({"errorcode": 400, "message": "时间格式错误，请使用毫秒级时间戳或有效的时间字符串", "data": None}), 400
            else:
                # 如果未提供时间，使用当前时间
                expend_time_dt = datetime.now()
            
            # 调用ExpendService的create_expend方法
            success, message, data = expend_service.create_expend(money, account_id, user_id, remark, expend_time_dt, expend_type_id, enable)
            
            if success:
                api_logger.info(f"新增支出记录成功 - user_id: {user_id}, expend_id: {data['id']}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"新增支出记录失败 - user_id: {user_id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"新增支出记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"新增支出记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/expend", methods=["PUT"])
    @token_required
    def update_expend():
        """
        更新支出记录接口
        请求头：token, userid
        请求体：id, money(可选), account_id(可选), remark(可选), expend_time(可选), expend_type_id(可选), enable(可选)
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        id = request.form.get("id", None)
        money = request.form.get("money", None)
        account_id = request.form.get("account_id", None)
        remark = request.form.get("remark", None)
        expend_time = request.form.get("expend_time", None)
        expend_type_id = request.form.get("expend_type_id", None)
        enable = request.form.get("enable", None)
        
        api_logger.info(f"更新支出记录路由被调用 - id: {id}")
        
        # 记录更新支出请求
        api_logger.info(f"收到更新支出请求 - user_id: {user_id}, id: {id}, money: {money}, account_id: {account_id}, remark: {remark}, expend_time: {expend_time}, expend_type_id: {expend_type_id}, enable: {enable}")
        
        try:
            # 验证id参数
            if not id:
                return jsonify({"errorcode": 400, "message": "参数id不能为空", "data": None}), 400
            
            # 转换id类型
            id = int(id.strip()) if id.strip() else None
            
            # 转换可选参数类型
            if money is not None:
                money = float(money.strip()) if money.strip() else None
            if account_id is not None:
                account_id = int(account_id.strip()) if account_id.strip() else None
            if expend_type_id is not None:
                expend_type_id = int(expend_type_id.strip()) if expend_type_id.strip() else None
            if enable is not None:
                enable = enable.strip().lower() in ['true', '1', 'yes']
            if remark is not None and remark.strip() == "":
                remark = None
            
            # 处理时间参数 - 支持毫秒级时间戳或时间字符串
            if expend_time is not None and expend_time.strip():
                expend_time_str = expend_time.strip()
                # 尝试解析为毫秒级时间戳
                try:
                    expend_time_ms = int(expend_time_str)
                    # 转换为datetime对象
                    expend_time = TimeUtils.milliseconds_to_datetime(expend_time_ms)
                except ValueError:
                    # 如果不是数字，尝试作为时间字符串解析
                    try:
                        # 支持多种常见的时间字符串格式
                        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
                        for fmt in formats:
                            try:
                                expend_time = datetime.strptime(expend_time_str, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError("Unsupported time format")
                    except ValueError:
                        return jsonify({"errorcode": 400, "message": "时间格式错误，请使用毫秒级时间戳或有效的时间字符串", "data": None}), 400
            elif expend_time is not None and expend_time.strip() == "":
                expend_time = None
            
            # 调用ExpendService的update_expend方法
            success, message, data = expend_service.update_expend(id, user_id, money, account_id, remark, expend_time, enable, expend_type_id)
            
            if success:
                api_logger.info(f"更新支出记录成功 - user_id: {user_id}, expend_id: {id}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"更新支出记录失败 - user_id: {user_id}, expend_id: {id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"更新支出记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"更新支出记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/expend", methods=["DELETE"])
    @token_required
    def delete_expend():
        """
        删除支出记录接口
        请求头：token, userid
        请求体：id
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取id参数
        id = request.form.get("id", None)
        
        # 记录删除支出请求
        api_logger.info(f"收到删除支出请求 - user_id: {user_id}, id: {id}")
        api_logger.info(f"删除支出记录路由被调用 - id: {id}")
        
        try:
            # 验证id参数
            if not id:
                return jsonify({"errorcode": 400, "message": "参数id不能为空", "data": None}), 400
            
            # 转换id类型
            id = int(id.strip()) if id.strip() else None
            
            # 调用ExpendService的delete_expend方法
            success, message, data = expend_service.delete_expend(id, user_id)
            
            if success:
                api_logger.info(f"删除支出记录成功 - user_id: {user_id}, expend_id: {id}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"删除支出记录失败 - user_id: {user_id}, expend_id: {id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except Exception as e:
            api_logger.error(f"删除支出记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"删除支出记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/expend", methods=["GET"])
    @token_required
    def get_expend_by_id():
        """
        获取支出记录接口
        请求头：token, userid
        请求参数：id(可选) - 提供id则获取单个记录，不提供则获取所有记录
        """
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从查询字符串中获取id参数
        id = request.args.get("id", None)
        
        api_logger.info(f"获取支出记录路由被调用 - id: {id}")
        
        # 记录获取支出请求
        api_logger.info(f"收到获取支出请求 - user_id: {user_id}, id: {id}")
        
        try:
            # 检查是否提供了id参数，如果提供则获取单个记录，否则获取所有记录
            if id:
                # 转换id类型
                id = int(id.strip()) if id.strip() else None
                
                # 调用ExpendService的get_expend_by_id方法
                success, message, data = expend_service.get_expend_by_id(id, user_id)
                
                if success:
                    api_logger.info(f"获取单个支出记录成功 - user_id: {user_id}, id: {id}")
                    return jsonify({"errorcode": 200, "message": message, "data": data}), 200
                else:
                    api_logger.warning(f"获取单个支出记录失败 - user_id: {user_id}, id: {id}, message: {message}")
                    return jsonify({"errorcode": 400, "message": message, "data": None}), 400
            else:
                # 调用ExpendService的get_expends_by_user_id方法获取所有记录
                success, message, data = expend_service.get_expends_by_user_id(user_id)
                
                if success:
                    api_logger.info(f"获取所有支出记录成功 - user_id: {user_id}")
                    return jsonify({"errorcode": 200, "message": message, "data": data}), 200
                else:
                    api_logger.warning(f"获取所有支出记录失败 - user_id: {user_id}, message: {message}")
                    return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"获取单个支出记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"获取单个支出记录失败: {str(e)}", "data": None}), 500
    
    api_logger.info("支出API路由配置完成")
