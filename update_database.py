import pymysql
import configparser
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.LogUtils import LogUtils

# 初始化日志
logger = LogUtils.get_instance('DatabaseUpdate')

# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config', 'DateBaseConfig.ini')
config.read(config_path)

# 获取数据库配置
env = config.get('app', 'env', fallback='test')
db_config = {
    'host': config.get(env, 'host'),
    'port': config.getint(env, 'port'),
    'user': config.get(env, 'user'),
    'password': config.get(env, 'password'),
    'database': config.get(env, 'database'),
    'charset': config.get(env, 'charset')
}

try:
    # 连接数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    logger.info("成功连接到数据库")
    
    # 执行SQL语句修改字段名
    sql = "ALTER TABLE expend CHANGE consumption_id expend_type_id BIGINT COMMENT '消费类型id';"
    cursor.execute(sql)
    
    # 提交事务
    conn.commit()
    
    logger.info("数据库表结构修改成功：将expend表中的consumption_id字段改为expend_type_id")
    
    # 关闭游标和连接
    cursor.close()
    conn.close()
    
    logger.info("数据库连接已关闭")
    
except Exception as e:
    logger.error(f"修改数据库表结构时发生错误：{str(e)}")
    if 'conn' in locals() and conn:
        conn.rollback()
        conn.close()