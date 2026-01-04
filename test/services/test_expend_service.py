import pytest
from services.ExpendService import ExpendService
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


@patch('services.ExpendService.ExpendDAO')
def test_create_expend_success(mock_expend_dao, test_expend_data):
    """
    测试创建支出记录成功
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    mock_dao_instance.create_expend.return_value = (True, test_expend_data['id'], None)
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.create_expend(
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
    assert message == "创建支出记录成功"
    assert data == {"id": test_expend_data['id']}


@patch('services.ExpendService.ExpendDAO')
def test_create_expend_account_not_found(mock_expend_dao, test_expend_data):
    """
    测试创建支出记录失败 - 账户不存在
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    error_msg = "账户不存在或不属于当前用户"
    mock_dao_instance.create_expend.return_value = (False, 0, error_msg)
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.create_expend(
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
    assert message == f"创建支出记录失败: {error_msg}"
    assert data is None


@patch('services.ExpendService.ExpendDAO')
def test_create_expend_expend_type_not_found(mock_expend_dao, test_expend_data):
    """
    测试创建支出记录失败 - 支出类型不存在
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    error_msg = "支出类型不存在"
    mock_dao_instance.create_expend.return_value = (False, 0, error_msg)
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.create_expend(
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
    assert message == f"创建支出记录失败: {error_msg}"
    assert data is None


@patch('services.ExpendService.ExpendDAO')
def test_create_expend_account_balance_not_enough(mock_expend_dao, test_expend_data):
    """
    测试创建支出记录失败 - 账户余额不足
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    error_msg = "账户余额不足"
    mock_dao_instance.create_expend.return_value = (False, 0, error_msg)
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.create_expend(
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
    assert message == f"创建支出记录失败: {error_msg}"
    assert data is None


@patch('services.ExpendService.ExpendDAO')
def test_update_expend_success(mock_expend_dao, test_expend_data):
    """
    测试更新支出记录成功
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    mock_dao_instance.update_expend.return_value = (True, None)
    mock_dao_instance.get_expend_by_id.return_value = (
        test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
        test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
        test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']
    )
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.update_expend(
        test_expend_data['id'],
        test_expend_data['user_id'],
        money=200,
        remark='更新后的测试支出'
    )
    
    # 验证结果
    assert success is True
    assert message == "更新支出记录成功"
    assert data == {"id": test_expend_data['id']}


@patch('services.ExpendService.ExpendDAO')
def test_update_expend_account_not_found(mock_expend_dao, test_expend_data):
    """
    测试更新支出记录失败 - 账户不存在
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    error_msg = "账户不存在或不属于当前用户"
    mock_dao_instance.update_expend.return_value = (False, error_msg)
    mock_dao_instance.get_expend_by_id.return_value = (
        test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
        test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
        test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']
    )
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.update_expend(
        test_expend_data['id'],
        test_expend_data['user_id'],
        money=200,
        remark='更新后的测试支出'
    )
    
    # 验证结果
    assert success is False
    assert message == f"更新支出记录失败: {error_msg}"
    assert data is None


@patch('services.ExpendService.ExpendDAO')
def test_delete_expend_success(mock_expend_dao, test_expend_data):
    """
    测试删除支出记录成功
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    mock_dao_instance.delete_expend.return_value = (True, None)
    mock_dao_instance.get_expend_by_id.return_value = (
        test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
        test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
        test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']
    )
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.delete_expend(
        test_expend_data['id'],
        test_expend_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert message == "删除支出记录成功"
    assert data == {"id": test_expend_data['id']}


@patch('services.ExpendService.ExpendDAO')
def test_delete_expend_account_not_found(mock_expend_dao, test_expend_data):
    """
    测试删除支出记录失败 - 账户不存在
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    error_msg = "账户不存在或不属于当前用户"
    mock_dao_instance.delete_expend.return_value = (False, error_msg)
    mock_dao_instance.get_expend_by_id.return_value = (
        test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
        test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
        test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']
    )
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.delete_expend(
        test_expend_data['id'],
        test_expend_data['user_id']
    )
    
    # 验证结果
    assert success is False
    assert message == f"删除支出记录失败: {error_msg}"
    assert data is None


@patch('services.ExpendService.ExpendDAO')
def test_get_expend_by_id_success(mock_expend_dao, test_expend_data):
    """
    测试根据ID查询支出记录成功
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    mock_dao_instance.get_expend_by_id.return_value = (
        test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
        test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
        test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']
    )
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.get_expend_by_id(
        test_expend_data['id'],
        test_expend_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert message == "查询支出记录成功"
    assert data['id'] == test_expend_data['id']
    assert data['money'] == test_expend_data['money']
    assert data['remark'] == test_expend_data['remark']


@patch('services.ExpendService.ExpendDAO')
def test_get_expends_by_user_id_success(mock_expend_dao, test_expend_data):
    """
    测试根据用户ID查询支出记录列表成功
    """
    # 配置模拟
    mock_dao_instance = MagicMock()
    mock_expend_dao.return_value = mock_dao_instance
    mock_dao_instance.get_expends_by_user_id.return_value = [
        (test_expend_data['id'], test_expend_data['money'], test_expend_data['account_id'], 
         test_expend_data['user_id'], test_expend_data['remark'], test_expend_data['expend_time'], 
         test_expend_data['create_time'], test_expend_data['enable'], test_expend_data['expend_type_id']),
        (2, 200, 1, 1, '测试支出2', '2023-01-02 12:00:00', '2023-01-02 12:00:00', True, 1)
    ]
    
    # 创建Service实例
    expend_service = ExpendService()
    
    # 执行测试
    success, message, data = expend_service.get_expends_by_user_id(
        test_expend_data['user_id']
    )
    
    # 验证结果
    assert success is True
    assert message == "查询支出记录列表成功"
    assert len(data) == 2
    assert data[0]['id'] == test_expend_data['id']
    assert data[1]['id'] == 2
