from flask import request, jsonify
from functools import wraps
from services.IncomeService import IncomeService
from utils.LogUtils import LogUtils
from utils.AuthUtils import token_required
from utils.TimeUtils import TimeUtils
from datetime import datetime

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

# 创建IncomeService实例
income_service = IncomeService()

def setup_income_routes(app):
    """
    设置收入相关的路由
    """
    api_logger.info("开始配置收入API路由")
    
    @app.route("/api/income", methods=["POST"])
    @token_required
    def create_income():
        """
        新增收入记录接口
        请求头：token, userid
        请求体：money, account_id, remark, income_time, income_type_id
        """
        api_logger.info("新增收入记录路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        money = request.form.get("money", None)
        account_id = request.form.get("account_id", None)
        remark = request.form.get("remark", None)
        income_time = request.form.get("income_time", None)
        income_type_id = request.form.get("income_type_id", None)
        enable = request.form.get("enable", "True")
        
        # 记录新增收入请求
        api_logger.info(f"收到新增收入请求 - user_id: {user_id}, money: {money}, account_id: {account_id}, remark: {remark}, income_time: {income_time}, income_type_id: {income_type_id}, enable: {enable}")
        
        try:
            # 验证必填参数
            missing_params = []
            if not money:
                missing_params.append("money")
            if not account_id:
                missing_params.append("account_id")
            if not income_type_id:
                missing_params.append("income_type_id")
            
            if missing_params:
                return jsonify({"errorcode": 400, "message": f"参数 {', '.join(missing_params)} 不能为空", "data": None}), 400
            
            # 转换参数类型
            money = float(money.strip()) if money.strip() else None
            account_id = int(account_id.strip()) if account_id.strip() else None
            income_type_id = int(income_type_id.strip()) if income_type_id.strip() else None
            enable = enable.strip().lower() in ['true', '1', 'yes']
            if remark is not None:
                remark = remark.strip()
            
            # 处理时间参数 - 支持毫秒级时间戳或时间字符串
            if income_time is not None and income_time.strip():
                income_time_str = income_time.strip()
                # 尝试解析为毫秒级时间戳
                try:
                    income_time_ms = int(income_time_str)
                    # 转换为datetime对象
                    income_time_dt = TimeUtils.milliseconds_to_datetime(income_time_ms)
                except ValueError:
                    # 如果不是数字，尝试作为时间字符串解析
                    try:
                        # 支持多种常见的时间字符串格式
                        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
                        for fmt in formats:
                            try:
                                income_time_dt = datetime.strptime(income_time_str, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError("Unsupported time format")
                    except ValueError:
                        return jsonify({"errorcode": 400, "message": "时间格式错误，请使用毫秒级时间戳或有效的时间字符串", "data": None}), 400
            else:
                # 如果未提供时间，使用当前时间
                income_time_dt = datetime.now()
            
            # 调用IncomeService的create_income方法
            success, message, data = income_service.create_income(money, account_id, user_id, remark, income_time_dt, income_type_id, enable)
            
            if success:
                api_logger.info(f"新增收入记录成功 - user_id: {user_id}, income_id: {data['id']}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"新增收入记录失败 - user_id: {user_id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"新增收入记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"新增收入记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/income", methods=["PUT"])
    @token_required
    def update_income():
        """
        更新收入记录接口
        请求头：token, userid
        请求体：id, money(可选), account_id(可选), remark(可选), income_time(可选), income_type_id(可选), enable(可选)
        """
        api_logger.info("更新收入记录路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取参数
        id = request.form.get("id", None)
        money = request.form.get("money", None)
        account_id = request.form.get("account_id", None)
        remark = request.form.get("remark", None)
        income_time = request.form.get("income_time", None)
        income_type_id = request.form.get("income_type_id", None)
        enable = request.form.get("enable", None)
        
        # 记录更新收入请求
        api_logger.info(f"收到更新收入请求 - user_id: {user_id}, id: {id}, money: {money}, account_id: {account_id}, remark: {remark}, income_time: {income_time}, income_type_id: {income_type_id}, enable: {enable}")
        
        # 验证id参数
        if not id:
            return jsonify({"errorcode": 400, "message": "id参数不能为空", "data": None}), 400
        
        try:
            id = int(id.strip())
        except ValueError:
            return jsonify({"errorcode": 400, "message": "id参数必须是数字", "data": None}), 400
        
        try:
            # 转换可选参数类型
            if money is not None:
                money = float(money.strip()) if money.strip() else None
            if account_id is not None:
                account_id = int(account_id.strip()) if account_id.strip() else None
            if income_type_id is not None:
                income_type_id = int(income_type_id.strip()) if income_type_id.strip() else None
            if enable is not None:
                enable = enable.strip().lower() in ['true', '1', 'yes']
            if remark is not None and remark.strip() == "":
                remark = None
            
            # 处理时间参数 - 支持毫秒级时间戳或时间字符串
            if income_time is not None and income_time.strip():
                income_time_str = income_time.strip()
                # 尝试解析为毫秒级时间戳
                try:
                    income_time_ms = int(income_time_str)
                    # 转换为datetime对象
                    income_time = TimeUtils.milliseconds_to_datetime(income_time_ms)
                except ValueError:
                    # 如果不是数字，尝试作为时间字符串解析
                    try:
                        # 支持多种常见的时间字符串格式
                        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
                        for fmt in formats:
                            try:
                                income_time = datetime.strptime(income_time_str, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError("Unsupported time format")
                    except ValueError:
                        return jsonify({"errorcode": 400, "message": "时间格式错误，请使用毫秒级时间戳或有效的时间字符串", "data": None}), 400
            elif income_time is not None and income_time.strip() == "":
                income_time = None
            
            # 调用IncomeService的update_income方法
            success, message, data = income_service.update_income(id, user_id, money, account_id, remark, income_time, enable, income_type_id)
            
            if success:
                api_logger.info(f"更新收入记录成功 - user_id: {user_id}, income_id: {id}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"更新收入记录失败 - user_id: {user_id}, income_id: {id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"更新收入记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"更新收入记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/income", methods=["DELETE"])
    @token_required
    def delete_income():
        """
        删除收入记录接口
        请求头：token, userid
        请求体：id
        """
        api_logger.info("删除收入记录路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从请求体中获取id参数
        id = request.form.get("id", None)
        
        # 记录删除收入请求
        api_logger.info(f"收到删除收入请求 - user_id: {user_id}, id: {id}")
        
        # 验证id参数
        if not id:
            return jsonify({"errorcode": 400, "message": "id参数不能为空", "data": None}), 400
        
        try:
            id = int(id.strip())
        except ValueError:
            return jsonify({"errorcode": 400, "message": "id参数必须是数字", "data": None}), 400
        
        try:
            # 调用IncomeService的delete_income方法
            success, message, data = income_service.delete_income(id, user_id)
            
            if success:
                api_logger.info(f"删除收入记录成功 - user_id: {user_id}, income_id: {id}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"删除收入记录失败 - user_id: {user_id}, income_id: {id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except Exception as e:
            api_logger.error(f"删除收入记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"删除收入记录失败: {str(e)}", "data": None}), 500
    
    @app.route("/api/income", methods=["GET"])
    @token_required
    def get_income():
        """
        获取收入记录接口
        请求头：token, userid
        请求参数：id(可选) - 提供id则获取单个记录，不提供则获取所有记录
        """
        api_logger.info("获取收入记录路由被调用")
        
        # 从请求头中获取user_id
        user_id = int(request.headers.get('userid'))
        
        # 从查询字符串中获取id参数
        id = request.args.get("id", None)
        
        # 记录获取收入请求
        api_logger.info(f"收到获取收入请求 - user_id: {user_id}, id: {id}")
        
        try:
            if id:
                # 获取单个收入记录
                id = int(id.strip())
                success, message, data = income_service.get_income_by_id(id, user_id)
            else:
                # 获取所有收入记录
                success, message, data = income_service.get_incomes_by_user_id(user_id)
            
            if success:
                api_logger.info(f"获取收入记录成功 - user_id: {user_id}, id: {id}")
                return jsonify({"errorcode": 200, "message": message, "data": data}), 200
            else:
                api_logger.warning(f"获取收入记录失败 - user_id: {user_id}, id: {id}, message: {message}")
                return jsonify({"errorcode": 400, "message": message, "data": None}), 400
        except ValueError as e:
            api_logger.error(f"参数类型错误: {e}")
            return jsonify({"errorcode": 400, "message": f"参数类型错误: {str(e)}", "data": None}), 400
        except Exception as e:
            api_logger.error(f"获取收入记录过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"errorcode": 500, "message": f"获取收入记录失败: {str(e)}", "data": None}), 500
    
    api_logger.info("收入API路由配置完成")
