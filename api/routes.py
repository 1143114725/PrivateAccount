from flask import Flask
from .user import setup_user_routes
from .account import setup_account_routes
from .expendtype import setup_expendtype_routes
from .incometype import setup_incometype_routes
from .expend import setup_expend_routes
from .income import setup_income_routes
from utils.LogUtils import LogUtils

# 初始化API日志记录器
api_logger = LogUtils.get_instance('API')

def setup_all_routes(app: Flask):
    """
    设置所有API路由的集中管理函数
    
    Args:
        app: Flask应用实例
    """
    api_logger.info("开始配置所有API路由")
    
    # 设置用户相关路由
    setup_user_routes(app)
    
    # 设置账户相关路由
    setup_account_routes(app)
    
    # 设置消费类型相关路由
    setup_expendtype_routes(app)
    
    # 设置收入类型相关路由
    setup_incometype_routes(app)
    
    # 设置支出相关路由
    setup_expend_routes(app)
    
    # 设置收入相关路由
    setup_income_routes(app)
    
    api_logger.info("所有API路由配置完成")
