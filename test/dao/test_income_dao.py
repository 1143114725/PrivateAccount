import pytest
import decimal
from dao.IncomeDAO import IncomeDAO
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture(scope='function')
def test_income_data():
    """
    提供测试用的收入数据
    """
    return {
        'id': 1,
        'money': 100,
        'account_id': 1,
        'user_id': 1,
        'remark': '测试收入',
        'income_time': '2023-01-01 12:00:00',
        'create_time': '2023-01-01 12:00:00',
        'enable': True,
        'income_type_id': 1
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


def test_create_income_success(mock_database, test_income_data, mock_account_data):
    """
    测试创建收入记录成功
    """
    # 配置模拟
    mock_cursor = mock_database.cur
    mock_cursor.lastrowid = test_income_data['id']
    mock_cursor.rowcount = 1
    
    # 模拟查询账户成功
    mock_database.execute.side_effect = [
        True,  # 第一次execute是查询账户
        True,  # 第二次execute是插入收入记录
        True   # 第三次execute是更新账户余额
    ]
    mock_database.cur.fetchone.side_effect = [
        (mock_account_data['id'], mock_account_data['account_name'], mock_account_data['balance'], 
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 查询账户返回结果
        None  # 其他fetchone调用返回None
    ]
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    success, income_id = income_dao.create_income(
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id']
    )
    
    # 验证结果
    assert success is True
    assert income_id == test_income_data['id']
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 3
    assert mock_database.commit.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_create_income_account_not_found(mock_database, test_income_data):
    """
    测试创建收入记录失败 - 账户不存在
    """
    # 配置模拟 - 账户不存在
    mock_database.execute.side_effect = [
        True,  # 查询账户
    ]
    mock_database.cur.fetchone.return_value = None  # 查询账户返回None
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    success, income_id = income_dao.create_income(
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id']
    )
    
    # 验证结果
    assert success is False
    assert income_id == 0
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 1
    assert mock_database.rollback.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_update_income_success(mock_database, test_income_data, mock_account_data):
    """
    测试更新收入记录成功
    """
    # 配置模拟
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 1
    
    # 模拟查询原收入记录和账户
    mock_database.execute.side_effect = [
        True,  # 查询原收入记录
        True,  # 更新收入记录
        True   # 更新账户余额
    ]
    mock_database.cur.fetchone.side_effect = [
        (test_income_data['id'], 50, test_income_data['account_id'], test_income_data['user_id'], 
         test_income_data['remark'], test_income_data['income_time'], test_income_data['create_time'], 
         test_income_data['enable'], test_income_data['income_type_id']),  # 原收入记录
        (mock_account_data['id'], mock_account_data['account_name'], decimal.Decimal('1050'), 
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 账户信息
        None
    ]
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    success = income_dao.update_income(
        test_income_data['id'],
        test_income_data['user_id'],
        money=test_income_data['money']
    )
    
    # 验证结果
    assert success is True
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 3
    assert mock_database.commit.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_delete_income_success(mock_database, test_income_data, mock_account_data):
    """
    测试删除收入记录成功
    """
    # 配置模拟
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 1
    
    # 模拟查询收入记录和账户
    mock_database.execute.side_effect = [
        True,  # 查询收入记录
        True,  # 删除收入记录
        True   # 更新账户余额
    ]
    mock_database.cur.fetchone.side_effect = [
        (test_income_data['id'], test_income_data['money'], test_income_data['account_id'], 
         test_income_data['user_id'], test_income_data['remark'], test_income_data['income_time'], 
         test_income_data['create_time'], test_income_data['enable'], test_income_data['income_type_id']),  # 收入记录
        (mock_account_data['id'], mock_account_data['account_name'], decimal.Decimal('1100'), 
         mock_account_data['user_id'], mock_account_data['remark'], mock_account_data['create_time'], 
         mock_account_data['enable']),  # 账户信息
        None
    ]
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    success = income_dao.delete_income(
        test_income_data['id'],
        test_income_data['user_id']
    )
    
    # 验证结果
    assert success is True
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 3
    assert mock_database.commit.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_get_income_by_id_success(mock_database, test_income_data):
    """
    测试根据ID查询收入记录成功
    """
    # 配置模拟 - 查询成功
    mock_database.execute.return_value = True
    mock_database.cur.fetchone.return_value = (
        test_income_data['id'], test_income_data['money'], test_income_data['account_id'], 
        test_income_data['user_id'], test_income_data['remark'], test_income_data['income_time'], 
        test_income_data['create_time'], test_income_data['enable'], test_income_data['income_type_id']
    )
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    income = income_dao.get_income_by_id(
        test_income_data['id'],
        test_income_data['user_id']
    )
    
    # 验证结果
    assert income is not None
    assert income[0] == test_income_data['id']
    assert income[1] == test_income_data['money']
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 1
    assert mock_database.disconnect.call_count == 1


def test_get_incomes_by_user_id_success(mock_database, test_income_data):
    """
    测试根据用户ID查询收入记录列表成功
    """
    # 配置模拟 - 查询成功
    mock_database.execute.return_value = True
    mock_database.cur.fetchall.return_value = [
        (test_income_data['id'], test_income_data['money'], test_income_data['account_id'], 
         test_income_data['user_id'], test_income_data['remark'], test_income_data['income_time'], 
         test_income_data['create_time'], test_income_data['enable'], test_income_data['income_type_id']),
        (2, 200, test_income_data['account_id'], test_income_data['user_id'], 
         '测试收入2', '2023-01-02 12:00:00', '2023-01-02 12:00:00', 
         True, test_income_data['income_type_id'])
    ]
    
    # 创建DAO实例
    income_dao = IncomeDAO()
    
    # 执行测试
    incomes = income_dao.get_incomes_by_user_id(test_income_data['user_id'])
    
    # 验证结果
    assert incomes is not None
    assert len(incomes) == 2
    assert incomes[0][0] == test_income_data['id']
    assert incomes[1][0] == 2
    
    # 验证调用
    assert mock_database.connect.call_count == 1
    assert mock_database.execute.call_count == 1
    assert mock_database.disconnect.call_count == 1
