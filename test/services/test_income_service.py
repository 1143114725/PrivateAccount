import pytest
from services.IncomeService import IncomeService
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


def test_create_income_success(mock_income_dao, test_income_data):
    """
    测试创建收入记录业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_income_dao.create_income.return_value = (True, test_income_data['id'])
    mock_income_dao.get_income_by_id.return_value = (
        test_income_data['id'],
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['create_time'],
        test_income_data['enable'],
        test_income_data['income_type_id']
    )
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.create_income(
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id']
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert data is not None
    assert data['id'] == test_income_data['id']
    
    # 验证DAO调用
    mock_income_dao.create_income.assert_called_once_with(
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id'],
        True
    )


def test_create_income_empty_money(mock_income_dao, test_income_data):
    """
    测试创建收入记录时金额为空
    """
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.create_income(
        None,
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id']
    )
    
    # 验证结果
    assert success is False
    assert "参数不能为空" in message
    assert data is None
    
    # 验证DAO调用
    mock_income_dao.create_income.assert_not_called()


def test_create_income_negative_money(mock_income_dao, test_income_data):
    """
    测试创建收入记录时金额为负数
    """
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.create_income(
        -100,
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['income_type_id']
    )
    
    # 验证结果
    assert success is False
    assert "金额必须大于0" in message
    assert data is None
    
    # 验证DAO调用
    mock_income_dao.create_income.assert_not_called()


def test_update_income_success(mock_income_dao, test_income_data):
    """
    测试更新收入记录业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_income_dao.update_income.return_value = True
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.update_income(
        test_income_data['id'],
        test_income_data['user_id'],
        money=200
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert data is not None
    assert data['id'] == test_income_data['id']
    
    # 验证DAO调用
    mock_income_dao.update_income.assert_called_once_with(
        test_income_data['id'],
        test_income_data['user_id'],
        200,  # money
        None,  # account_id
        None,  # remark
        None,  # income_time
        None,  # enable
        None   # income_type_id
    )


def test_delete_income_success(mock_income_dao, test_income_data):
    """
    测试删除收入记录业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_income_dao.delete_income.return_value = True
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.delete_income(
        test_income_data['id'],
        test_income_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert data is not None
    assert data['id'] == test_income_data['id']
    
    # 验证DAO调用
    mock_income_dao.delete_income.assert_called_once_with(
        test_income_data['id'],
        test_income_data['user_id']
    )


def test_get_income_by_id_success(mock_income_dao, test_income_data):
    """
    测试根据ID查询收入记录业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_income_dao.get_income_by_id.return_value = (
        test_income_data['id'],
        test_income_data['money'],
        test_income_data['account_id'],
        test_income_data['user_id'],
        test_income_data['remark'],
        test_income_data['income_time'],
        test_income_data['create_time'],
        test_income_data['enable'],
        test_income_data['income_type_id']
    )
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.get_income_by_id(
        test_income_data['id'],
        test_income_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert data is not None
    assert data['id'] == test_income_data['id']
    assert data['money'] == test_income_data['money']
    
    # 验证DAO调用
    mock_income_dao.get_income_by_id.assert_called_once_with(
        test_income_data['id'],
        test_income_data['user_id']
    )


def test_get_incomes_by_user_id_success(mock_income_dao, test_income_data):
    """
    测试根据用户ID查询收入记录列表业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_income_dao.get_incomes_by_user_id.return_value = [
        (test_income_data['id'],
         test_income_data['money'],
         test_income_data['account_id'],
         test_income_data['user_id'],
         test_income_data['remark'],
         test_income_data['income_time'],
         test_income_data['create_time'],
         test_income_data['enable'],
         test_income_data['income_type_id']),
        (2, 200, 1, 1, '测试收入2', '2023-01-02 12:00:00', '2023-01-02 12:00:00', True, 1)
    ]
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.get_incomes_by_user_id(
        test_income_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert data is not None
    assert len(data) == 2
    assert data[0]['id'] == test_income_data['id']
    assert data[1]['id'] == 2
    
    # 验证DAO调用
    mock_income_dao.get_incomes_by_user_id.assert_called_once_with(
        test_income_data['user_id']
    )


def test_get_income_by_id_not_found(mock_income_dao, test_income_data):
    """
    测试根据ID查询收入记录不存在
    """
    # 配置模拟DAO返回值
    mock_income_dao.get_income_by_id.return_value = None
    
    # 创建Service实例
    income_service = IncomeService()
    
    # 执行测试
    success, message, data = income_service.get_income_by_id(
        999,  # 不存在的ID
        test_income_data['user_id']
    )
    
    # 验证结果
    assert success is False
    assert "不存在" in message
    assert data is None
    
    # 验证DAO调用
    mock_income_dao.get_income_by_id.assert_called_once_with(
        999,
        test_income_data['user_id']
    )
