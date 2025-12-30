from flask import Flask
import signal
import sys
import logging
from db.Database import Database
from api.user import setup_routes

# 创建Flask应用实例
app = Flask(__name__)

# 设置路由
setup_routes(app)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('App')


def cleanup_resources():
    """
    清理资源：关闭数据库连接池等
    """
    logger.info("开始清理资源...")
    
    # 关闭数据库连接池
    try:
        if Database.pool is not None:
            Database.pool.close()
            Database.pool = None
            logger.info("数据库连接池已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接池时出错: {e}")


def shutdown_handler(signum, frame):
    """
    信号处理函数：优雅关闭服务
    """
    logger.info(f"接收到信号 {signum}，准备关闭服务...")
    cleanup_resources()
    logger.info("服务已优雅关闭")
    sys.exit(0)


if __name__ == "__main__":
    # 注册信号处理
    signal.signal(signal.SIGINT, shutdown_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown_handler)  # kill命令
    
    logger.info("服务启动中...")
    logger.info("监听地址: 0.0.0.0:8080")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)  # 监听所有地址，支持localhost访问
    except KeyboardInterrupt:
        logger.info("接收到键盘中断，准备关闭服务...")
    finally:
        cleanup_resources()
        logger.info("服务已关闭")
