import pytest
from flask import Flask
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from db.Database import Database
from utils.ConfigManager import ConfigManager


@pytest.fixture(scope='session')
def test_app():
    """
    创建测试用的Flask应用实例
    """
    # 使用测试配置
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def test_client(test_app):
    """
    创建测试客户端
    """
    return test_app.test_client()


@pytest.fixture(scope='function')
def mock_database():
    """
    创建模拟的数据库连接
    """
    # 同时patch两个可能的导入路径
    with (patch('db.Database.Database') as mock_db_class,
          patch('dao.ExpendTypeDAO.Database') as mock_dao_db_class):
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_dao_db_class.return_value = mock_db
        
        # 模拟数据库游标和连接
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        
        # 配置基本方法模拟
        mock_db.connect.return_value = True
        mock_db.conn = mock_conn
        mock_db.cur = mock_cursor
        mock_db.execute.return_value = True
        mock_db.commit.return_value = True
        mock_db.rollback.return_value = True
        mock_db.disconnect.return_value = None
        
        # 配置游标方法模拟
        mock_cursor.lastrowid = 1
        mock_cursor.rowcount = 1
        mock_cursor.fetchone.return_value = None
        mock_cursor.fetchall.return_value = None
        
        # 模拟类变量pool
        mock_pool = Mock()
        mock_pool.connection.return_value = mock_conn
        mock_db_class.pool = mock_pool
        mock_dao_db_class.pool = mock_pool
        
        # 确保实例也能访问到pool
        mock_db.pool = mock_pool
        
        yield mock_db


@pytest.fixture(scope='function')
def mock_config_manager():
    """
    创建模拟的配置管理器
    """
    with patch('utils.ConfigManager.ConfigManager') as mock_config_class:
        mock_config = Mock()
        mock_config_class.return_value = mock_config
        
        # 设置默认配置
        mock_config.get.side_effect = lambda section, key, default=None: {
            ('app', 'env'): 'test',
            ('test', 'host'): 'localhost',
            ('test', 'port'): '3306',
            ('test', 'user'): 'test_user',
            ('test', 'password'): 'test_pass',
            ('test', 'database'): 'test_db',
            ('test', 'charset'): 'utf8mb4'
        }.get((section, key), default)
        
        mock_config.getint.side_effect = lambda section, key, default=None: {
            ('test', 'port'): 3306
        }.get((section, key), default)
        
        yield mock_config


@pytest.fixture(scope='function')
def test_token():
    """
    创建测试用的token
    """
    from utils.TokenUtils import TokenUtils
    from datetime import datetime, timedelta
    
    user_id = 1
    # 创建一个有效期内的token
    token = TokenUtils.generate_token(user_id, 'test_refresh_token')
    
    return token, user_id


@pytest.fixture(scope='function')
def expired_token():
    """
    创建过期的token
    """
    from utils.TokenUtils import TokenUtils
    from datetime import datetime, timedelta
    
    user_id = 1
    
    # 模拟过期时间
    with patch('utils.TokenUtils.datetime') as mock_datetime:
        # 设置当前时间为未来时间，使生成的token立即过期
        mock_datetime.now.return_value = datetime.now() - timedelta(days=2)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        token = TokenUtils.generate_token(user_id, 'test_refresh_token')
        
    return token, user_id


@pytest.fixture(scope='function')
def mock_logger():
    """
    创建模拟的日志记录器
    """
    with patch('utils.LogUtils.LogUtils.get_instance') as mock_get_logger:
        mock_log = Mock()
        mock_get_logger.return_value = mock_log
        
        yield mock_log


@pytest.fixture(scope='function')
def test_expend_type_data():
    """
    提供测试用的消费类型数据
    """
    return {
        'id': 1,
        'expend_type_name': '餐饮',
        'enable': True,
        'create_time': '2023-01-01 00:00:00'
    }


@pytest.fixture(scope='function')
def mock_expend_type_dao():
    """
    创建模拟的ExpendTypeDAO
    """
    # 同时patch两个可能的导入路径
    with (patch('dao.ExpendTypeDAO.ExpendTypeDAO') as mock_dao_class,
          patch('services.ExpendTypeService.ExpendTypeDAO') as mock_service_dao_class):
        mock_dao = Mock()
        mock_dao_class.return_value = mock_dao
        mock_service_dao_class.return_value = mock_dao
        
        # 设置默认模拟返回值
        mock_dao.create_expend_type.return_value = (True, 1)
        mock_dao.get_expend_type_by_id.return_value = (1, '餐饮', True, '2023-01-01 00:00:00')
        mock_dao.get_all_expend_types.return_value = [(1, '餐饮', True, '2023-01-01 00:00:00'), (2, '交通', True, '2023-01-01 00:00:00')]
        mock_dao.update_expend_type.return_value = True
        mock_dao.delete_expend_type.return_value = True
        
        yield mock_dao
