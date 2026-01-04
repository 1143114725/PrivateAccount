import pytest
import json
from app import app
from unittest.mock import patch
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_token_header():
    """模拟有效的token和userid请求头"""
    return {
        'token': 'valid_token',
        'userid': '1'
    }


@pytest.fixture
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


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.create_expend')
def test_create_expend_success(mock_create_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试创建支出记录成功
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_expend.return_value = (True, "创建支出记录成功", {"id": test_expend_data['id']})
    
    # 发送创建支出请求
    response = client.post('/api/expend', 
                          headers=mock_token_header,
                          data={
                              'money': str(test_expend_data['money']),
                              'account_id': str(test_expend_data['account_id']),
                              'remark': test_expend_data['remark'],
                              'expend_time': test_expend_data['expend_time'],
                              'expend_type_id': str(test_expend_data['expend_type_id'])
                          })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '创建支出记录成功'
    assert data['data']['id'] == test_expend_data['id']


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.create_expend')
def test_create_expend_account_not_found(mock_create_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试创建支出记录失败 - 账户不存在
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    specific_error_msg = "账户不存在或不属于当前用户"
    mock_create_expend.return_value = (False, f"创建支出记录失败: {specific_error_msg}", None)
    
    # 发送创建支出请求
    response = client.post('/api/expend', 
                          headers=mock_token_header,
                          data={
                              'money': str(test_expend_data['money']),
                              'account_id': str(test_expend_data['account_id']),
                              'remark': test_expend_data['remark'],
                              'expend_time': test_expend_data['expend_time'],
                              'expend_type_id': str(test_expend_data['expend_type_id'])
                          })
    
    # 验证响应 - 确保返回具体错误信息
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == f"创建支出记录失败: {specific_error_msg}"
    assert data['data'] is None


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.create_expend')
def test_create_expend_expend_type_not_found(mock_create_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试创建支出记录失败 - 支出类型不存在
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    specific_error_msg = "支出类型不存在"
    mock_create_expend.return_value = (False, f"创建支出记录失败: {specific_error_msg}", None)
    
    # 发送创建支出请求
    response = client.post('/api/expend', 
                          headers=mock_token_header,
                          data={
                              'money': str(test_expend_data['money']),
                              'account_id': str(test_expend_data['account_id']),
                              'remark': test_expend_data['remark'],
                              'expend_time': test_expend_data['expend_time'],
                              'expend_type_id': str(test_expend_data['expend_type_id'])
                          })
    
    # 验证响应 - 确保返回具体错误信息
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == f"创建支出记录失败: {specific_error_msg}"
    assert data['data'] is None


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.create_expend')
def test_create_expend_account_balance_not_enough(mock_create_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试创建支出记录失败 - 账户余额不足
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    specific_error_msg = "账户余额不足"
    mock_create_expend.return_value = (False, f"创建支出记录失败: {specific_error_msg}", None)
    
    # 发送创建支出请求
    response = client.post('/api/expend', 
                          headers=mock_token_header,
                          data={
                              'money': str(test_expend_data['money']),
                              'account_id': str(test_expend_data['account_id']),
                              'remark': test_expend_data['remark'],
                              'expend_time': test_expend_data['expend_time'],
                              'expend_type_id': str(test_expend_data['expend_type_id'])
                          })
    
    # 验证响应 - 确保返回具体错误信息
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == f"创建支出记录失败: {specific_error_msg}"
    assert data['data'] is None


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.update_expend')
def test_update_expend_account_not_found(mock_update_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试更新支出记录失败 - 账户不存在
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    specific_error_msg = "账户不存在或不属于当前用户"
    mock_update_expend.return_value = (False, f"更新支出记录失败: {specific_error_msg}", None)
    
    # 发送更新支出请求
    response = client.put('/api/expend', 
                         headers=mock_token_header,
                         data={
                             'id': str(test_expend_data["id"]),
                             'money': '200',
                             'remark': '更新后的测试支出'
                         })
    
    # 验证响应 - 确保返回具体错误信息
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == f"更新支出记录失败: {specific_error_msg}"
    assert data['data'] is None


@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.ExpendService.ExpendService.delete_expend')
def test_delete_expend_account_not_found(mock_delete_expend, mock_validate_token, mock_get_user, client, mock_token_header, test_expend_data):
    """
    测试删除支出记录失败 - 账户不存在
    """
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    specific_error_msg = "账户不存在或不属于当前用户"
    mock_delete_expend.return_value = (False, f"删除支出记录失败: {specific_error_msg}", None)
    
    # 发送删除支出请求
    response = client.delete('/api/expend', headers=mock_token_header, data={'id': str(test_expend_data["id"])})
    
    # 验证响应 - 确保返回具体错误信息
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == f"删除支出记录失败: {specific_error_msg}"
    assert data['data'] is None
