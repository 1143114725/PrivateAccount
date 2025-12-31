import pytest
import json
from app import app
from unittest.mock import patch

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

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.AccountService.AccountService.create_account')
def test_add_account_with_integer_balance(mock_create_account, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试添加账户时使用整数余额"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_account.return_value = (True, "账户创建成功", (1, "测试账户", 100, 1))
    
    # 发送添加账户请求
    response = client.post('/api/account', 
                          headers=mock_token_header,
                          data={
                              'account_name': '测试账户',
                              'balance': '100'
                          })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '账户创建成功'
    assert data['data']['balance'] == 100

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.AccountService.AccountService.create_account')
def test_add_account_with_one_decimal_balance(mock_create_account, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试添加账户时使用一位小数余额"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_account.return_value = (True, "账户创建成功", (1, "测试账户", 100.5, 1))
    
    # 发送添加账户请求
    response = client.post('/api/account', 
                          headers=mock_token_header,
                          data={
                              'account_name': '测试账户',
                              'balance': '100.5'
                          })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '账户创建成功'
    assert data['data']['balance'] == 100.5

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.AccountService.AccountService.create_account')
def test_add_account_with_two_decimal_balance(mock_create_account, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试添加账户时使用两位小数余额"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_account.return_value = (True, "账户创建成功", (1, "测试账户", 100.55, 1))
    
    # 发送添加账户请求
    response = client.post('/api/account', 
                          headers=mock_token_header,
                          data={
                              'account_name': '测试账户',
                              'balance': '100.55'
                          })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '账户创建成功'
    assert data['data']['balance'] == 100.55

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.AccountService.AccountService.create_account')
def test_add_account_with_three_decimal_balance(mock_create_account, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试添加账户时使用超过两位小数的余额（应该自动截断到两位小数）"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_account.return_value = (True, "账户创建成功", (1, "测试账户", 100.55, 1))
    
    # 发送添加账户请求，使用三位小数余额
    response = client.post('/api/account', 
                          headers=mock_token_header,
                          data={
                              'account_name': '测试账户',
                              'balance': '100.555'
                          })
    
    # 验证响应 - 应该成功，并且余额被自动截断到两位小数
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '账户创建成功'
    assert data['data']['balance'] == 100.55

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.AccountService.AccountService.update_balance')
@patch('services.AccountService.AccountService.get_account_by_id')
def test_update_account_with_decimal_balance(mock_get_account, mock_update_balance, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试修改账户余额时使用小数余额"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_get_account.return_value = (True, "查询账户成功", (1, "测试账户", 100, 1))
    mock_update_balance.return_value = (True, "账户余额修改成功", (1, "测试账户", 200.75, 1))
    
    # 发送修改账户余额请求
    response = client.put('/api/account/balance', 
                         headers=mock_token_header,
                         data={
                             'account_id': '1',
                             'new_balance': '200.75'
                         })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '账户余额修改成功'
    assert data['data']['balance'] == 200.75