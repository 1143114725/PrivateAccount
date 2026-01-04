import pytest
import decimal
from dao.ExpendDAO import ExpendDAO
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture(scope='function')
def test_expend_data():
    """
    提供测试用的支出数据
    """
    return {
        'id': 1,
        'money': 100,
        'account_id': 1,
        'user_id': 1,
        'remark': '测试支出',
        'expend_time': '2023-01-01 12:00:00',
        'create_time': '2023-01-01 12:00:00',
        'enable': True,
        'expend_type_id': 1
    }


@pytest.fixture(scope='function')
def mock_account_data():
    """
    提供测试用的账户数据
    """
    return {
        'id': 1,
        'account_name': '测试账户',
        'balance': decimal.Decimal('1000'),
        'user_id': 1,
        'remark': '测试账户备注',
        'create_time': '2023-01-01 12:00:00',
        'enable': True
    }


def test_create_expend_success(mock_database, test_expend_data, mock_account_data):
    """
    测试创建支出记录成功
    """
    # 配置模拟
    mock_cursor = mock_database.cur
    mock_cursor.lastrowid = test_expend_data['id']
    mock_cursor.rowcount = 1
    
    # 模拟查询账户成功
    mock_database.cur.fetchone.side_effect = [
        (mock_account_data['id'], mock_account_data['account_name'], mock_account_data['balance'], 
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 查询账户返回结果
        (1, "食品", 1),  # 查询支出类型返回结果
        None  # 其他fetchone调用返回None
    ]
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, expend_id, error_msg = expend_dao.create_expend(
        test_expend_data['money'],
        test_expend_data['account_id'],
        test_expend_data['user_id'],
        test_expend_data['remark'],
        test_expend_data['expend_time'],
        test_expend_data['expend_type_id'],
        True
    )
    
    # 验证结果
    assert success is True
    assert expend_id == test_expend_data['id']
    assert error_msg is None
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 5  # START TRANSACTION, 查询账户, 查询支出类型, 插入支出记录, 更新账户余额
    assert mock_database.commit.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_create_expend_account_not_found(mock_database, test_expend_data):
    """
    测试创建支出记录失败 - 账户不存在
    """
    # 配置模拟 - 账户不存在
    mock_database.cur.fetchone.return_value = None  # 查询账户返回None
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, expend_id, error_msg = expend_dao.create_expend(
        test_expend_data['money'],
        test_expend_data['account_id'],
        test_expend_data['user_id'],
        test_expend_data['remark'],
        test_expend_data['expend_time'],
        test_expend_data['expend_type_id'],
        True
    )
    
    # 验证结果
    assert success is False
    assert expend_id == 0
    assert error_msg == "账户不存在或不属于当前用户"
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 2  # START TRANSACTION, 查询账户
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_create_expend_type_not_found(mock_database, test_expend_data, mock_account_data):
    """
    测试创建支出记录失败 - 支出类型不存在
    """
    # 配置模拟 - 支出类型不存在
    mock_database.cur.fetchone.side_effect = [
        (mock_account_data['id'], mock_account_data['account_name'], mock_account_data['balance'], 
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 查询账户返回结果
        None,  # 查询支出类型返回None
        None
    ]
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, expend_id, error_msg = expend_dao.create_expend(
        test_expend_data['money'],
        test_expend_data['account_id'],
        test_expend_data['user_id'],
        test_expend_data['remark'],
        test_expend_data['expend_time'],
        test_expend_data['expend_type_id'],
        True
    )
    
    # 验证结果
    assert success is False
    assert expend_id == 0
    assert error_msg == "支出类型不存在"
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 3  # START TRANSACTION, 查询账户, 查询支出类型
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_create_expend_account_balance_not_enough(mock_database, test_expend_data, mock_account_data):
    """
    测试创建支出记录失败 - 账户余额不足
    """
    # 配置模拟 - 账户余额不足
    mock_database.cur.fetchone.side_effect = [
        (mock_account_data['id'], mock_account_data['account_name'], decimal.Decimal('50'),  # 余额不足
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 查询账户返回结果
        None
    ]
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, expend_id, error_msg = expend_dao.create_expend(
        test_expend_data['money'],  # 100元支出
        test_expend_data['account_id'],
        test_expend_data['user_id'],
        test_expend_data['remark'],
        test_expend_data['expend_time'],
        test_expend_data['expend_type_id'],
        True
    )
    
    # 验证结果
    assert success is False
    assert expend_id == 0
    assert error_msg == "账户余额不足"
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 2  # START TRANSACTION, 查询账户
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_update_expend_account_not_found(mock_database, test_expend_data):
    """
    测试更新支出记录失败 - 账户不存在
    """
    # 配置模拟 - 原支出记录存在，但账户不存在
    mock_database.cur.fetchone.side_effect = [
        (test_expend_data['id'], 50, test_expend_data['account_id'], test_expend_data['user_id'], 
         test_expend_data['remark'], test_expend_data['expend_time'], test_expend_data['create_time'], 
         test_expend_data['enable'], test_expend_data['expend_type_id']),  # 原支出记录
        None,  # 查询账户返回None
        None
    ]
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, error_msg = expend_dao.update_expend(
        test_expend_data['id'],
        test_expend_data['user_id'],
        money=test_expend_data['money']
    )
    
    # 验证结果
    assert success is False
    assert error_msg == "账户不存在或不属于当前用户"
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 4  # 查询原支出记录, 开始事务, 更新支出记录, 查询账户
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_delete_expend_account_not_found(mock_database, test_expend_data):
    """
    测试删除支出记录失败 - 账户不存在
    """
    # 配置模拟 - 支出记录存在，但账户不存在
    mock_database.cur.fetchone.side_effect = [
        (test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
         test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
         test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']),  # 支出记录
        None,  # 查询账户返回None
        None
    ]
    
    # 创建DAO实例
    expend_dao = ExpendDAO()
    
    # 执行测试
    success, error_msg = expend_dao.delete_expend(
        test_expend_data['id'],
        test_expend_data['user_id']
    )
    
    # 验证结果
    assert success is False
    assert error_msg == "账户不存在或不属于当前用户"
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.cur.execute.call_count == 4  # 开始事务, 查询支出记录, 删除支出记录, 查询账户
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1
