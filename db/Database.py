import pymysql
from dbutils.pooled_db import PooledDB
from utils.ConfigManager import ConfigManager
from utils.LogUtils import LogUtils

class Database:
    # 类变量，保存连接池实例和配置管理器实例
    pool = None
    config_manager = None
    logger = None
    
    def __init__(self, config_file='config/DateBaseConfig.ini', default_env='dev'):
        self.config_file = config_file
        self.default_env = default_env
        self.conn = None
        self.cur = None
        
        # 初始化日志器（如果尚未初始化）
        if Database.logger is None:
            try:
                Database.logger = LogUtils.get_instance('Database')
            except Exception as e:
                # 如果日志器初始化失败，使用基本的logging配置作为后备
                import logging
                logging.basicConfig(level=logging.ERROR)
                logging.error(f"初始化日志器失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 初始化配置管理器（如果尚未初始化）
        if Database.config_manager is None:
            try:
                Database.config_manager = ConfigManager(config_file, env_override=True)
                Database.logger.info(f"配置管理器初始化成功，配置文件: {config_file}")
            except Exception as e:
                Database.logger.error(f"初始化配置管理器失败: {e}")
                import traceback
                traceback.print_exc()
                return
        
        # 如果连接池不存在，则创建连接池
        if Database.pool is None:
            try:
                self._load_config()
                self._create_pool()
            except Exception as e:
                if Database.logger is not None:
                    Database.logger.error(f"初始化数据库连接池失败: {e}")
                else:
                    # 如果日志器不可用，使用基本的logging配置作为后备
                    import logging
                    logging.basicConfig(level=logging.ERROR)
                    logging.error(f"初始化数据库连接池失败: {e}")
                import traceback
                traceback.print_exc()
    
    def _load_config(self):
        # 使用类共享的ConfigManager实例获取配置
        config = Database.config_manager
        Database.logger.info("开始加载数据库配置")
        
        # 获取当前环境
        current_env = config.get('app', 'env', default=self.default_env)
        Database.logger.info(f"当前环境: {current_env}")
        
        # 验证必要的配置项是否存在
        required_keys = ['host', 'port', 'user', 'password', 'database', 'charset']
        try:
            config.validate(required_sections=[current_env], required_keys={current_env: required_keys})
            Database.logger.info(f"配置验证成功，环境: {current_env}")
        except ValueError as e:
            Database.logger.error(f"配置验证失败: {e}")
            raise
        
        self.db_config = {
            'host': config.get(current_env, 'host'),
            'port': config.getint(current_env, 'port'),
            'user': config.get(current_env, 'user'),
            'password': config.get(current_env, 'password'),
            'database': config.get(current_env, 'database'),
            'charset': config.get(current_env, 'charset')
        }
        
        # 记录数据库配置信息（隐藏密码）
        log_config = self.db_config.copy()
        if 'password' in log_config:
            log_config['password'] = '******'
        Database.logger.info(f"数据库配置加载完成: {log_config}")
    
    def _create_pool(self):
        """创建数据库连接池"""
        Database.logger.info("开始创建数据库连接池")
        
        pool_params = {
            'creator': pymysql,  # 使用pymysql作为数据库连接的创建者
            'maxconnections': 20,  # 连接池允许的最大连接数，0表示不限制
            'mincached': 5,  # 初始化时连接池中的空闲连接数
            'maxcached': 10,  # 连接池中最多允许的空闲连接数，0表示不限制
            'maxshared': 10,  # 连接池中最多允许的共享连接数，0表示不共享
            'blocking': True,  # 当连接池没有可用连接时，是否阻塞等待，True表示等待
            'maxusage': None,  # 一个连接最多被重复使用的次数，None表示不限制
            'setsession': [],  # 开始会话前执行的命令列表
            'ping': 0,  # 检查连接是否可用的方式，0表示从不检查
            **self.db_config
        }
        
        # 记录连接池参数（隐藏密码）
        log_params = pool_params.copy()
        if 'password' in log_params:
            log_params['password'] = '******'
        Database.logger.info(f"连接池参数: {log_params}")
        
        try:
            Database.pool = PooledDB(**pool_params)
            Database.logger.info("数据库连接池创建成功")
        except Exception as e:
            Database.logger.error(f"创建数据库连接池失败: {e}")
            raise
    
    def connect(self):
        try:
            Database.logger.info("尝试从连接池获取数据库连接")
            # 从连接池获取连接
            self.conn = Database.pool.connection()
            self.cur = self.conn.cursor()
            Database.logger.info("成功获取数据库连接")
            return True
        except Exception as e:
            Database.logger.error(f"数据库连接错误: {e}")
            return False
    
    def disconnect(self):
        Database.logger.info("开始释放数据库连接资源")
        if self.cur:
            try:
                self.cur.close()
                Database.logger.info("游标关闭成功")
            except Exception as e:
                Database.logger.error(f"游标关闭错误: {e}")
        if self.conn:
            try:
                # 将连接放回连接池
                self.conn.close()
                Database.logger.info("数据库连接已放回连接池")
            except Exception as e:
                Database.logger.error(f"数据库连接放回连接池错误: {e}")
        Database.logger.info("数据库连接资源释放完成")
    
    def execute(self, query, params=None):
        try:
            if not self.conn:
                if not self.connect():
                    return False
            
            # 记录 SQL 执行信息（隐藏可能的敏感信息）
            Database.logger.debug(f"准备执行 SQL: {query}")
            if params:
                # 不记录完整参数，避免敏感信息泄露
                Database.logger.debug(f"SQL 参数类型: {type(params).__name__}")
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            
            affected_rows = self.cur.rowcount
            Database.logger.info(f"SQL 执行成功，影响行数: {affected_rows}")
            return True
        except pymysql.ProgrammingError as e:
            Database.logger.error(f"SQL 语句执行错误: {e}")
            Database.logger.debug(f"错误 SQL: {query}")
            return False
        except pymysql.Error as e:
            Database.logger.error(f"发生数据库错误: {e}")
            Database.logger.debug(f"错误 SQL: {query}")
            # 发生数据库错误时，尝试重新连接
            if self.connect():
                Database.logger.info("数据库重新连接成功")
            else:
                Database.logger.error("数据库重新连接失败")
            return False
    
    def commit(self):
        try:
            if self.conn:
                Database.logger.info("准备提交事务")
                self.conn.commit()
                Database.logger.info("事务提交成功")
                return True
            Database.logger.warning("尝试提交事务时连接已关闭")
            return False
        except pymysql.Error as e:
            Database.logger.error(f"提交事务错误: {e}")
            return False
    
    def rollback(self):
        try:
            if self.conn:
                Database.logger.info("准备回滚事务")
                self.conn.rollback()
                Database.logger.info("事务回滚成功")
                return True
            Database.logger.warning("尝试回滚事务时连接已关闭")
            return False
        except pymysql.Error as e:
            Database.logger.error(f"回滚事务错误: {e}")
            return False
    
    def __enter__(self):
        Database.logger.info("进入数据库上下文管理器")
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        Database.logger.info("退出数据库上下文管理器")
        if exc_type:
            Database.logger.warning(f"上下文管理器中发生异常: {exc_type.__name__}: {exc_val}")
            self.rollback()
        else:
            self.commit()
        self.disconnect()
