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
@patch('services.IncomeService.IncomeService.create_income')
def test_create_income(mock_create_income, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试创建收入记录"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_create_income.return_value = (True, "创建收入记录成功", {"id": 1})
    
    # 发送创建收入请求
    response = client.post('/api/income', 
                          headers=mock_token_header,
                          data={
                              'money': '100',
                              'account_id': '1',
                              'remark': '测试收入',
                              'income_time': '2023-01-01 12:00:00',
                              'income_type_id': '1'
                          })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '创建收入记录成功'
    assert data['data']['id'] == 1

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.IncomeService.IncomeService.update_income')
def test_update_income(mock_update_income, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试更新收入记录"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_update_income.return_value = (True, "更新收入记录成功", {"id": 1})
    
    # 发送更新收入请求
    response = client.put('/api/income/1', 
                         headers=mock_token_header,
                         data={
                             'money': '200',
                             'remark': '更新后的测试收入'
                         })
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '更新收入记录成功'
    assert data['data']['id'] == 1

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.IncomeService.IncomeService.delete_income')
def test_delete_income(mock_delete_income, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试删除收入记录"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_delete_income.return_value = (True, "删除收入记录成功", {"id": 1})
    
    # 发送删除收入请求
    response = client.delete('/api/income/1', headers=mock_token_header)
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '删除收入记录成功'
    assert data['data']['id'] == 1

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.IncomeService.IncomeService.get_income_by_id')
def test_get_income_by_id(mock_get_income, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试获取单个收入记录"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_get_income.return_value = (True, "查询收入记录成功", {
        "id": 1,
        "money": 100,
        "account_id": 1,
        "user_id": 1,
        "remark": "测试收入",
        "income_time": "2023-01-01 12:00:00",
        "create_time": "2023-01-01 12:00:00",
        "enable": True,
        "income_type_id": 1
    })
    
    # 发送获取收入请求
    response = client.get('/api/income/1', headers=mock_token_header)
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '查询收入记录成功'
    assert data['data']['id'] == 1
    assert data['data']['money'] == 100

@patch('services.UserService.UserService.get_user_by_id')
@patch('utils.TokenUtils.TokenUtils.validate_token')
@patch('services.IncomeService.IncomeService.get_incomes_by_user_id')
def test_get_all_incomes(mock_get_incomes, mock_validate_token, mock_get_user, client, mock_token_header):
    """测试获取所有收入记录"""
    # 设置mock返回值
    mock_validate_token.return_value = True
    mock_get_user.return_value = (1, "testuser", "password", "13800138000", "enable", 1620000000000, "token", "token_expire")
    mock_get_incomes.return_value = (True, "查询收入记录列表成功", [
        {
            "id": 1,
            "money": 100,
            "account_id": 1,
            "user_id": 1,
            "remark": "测试收入1",
            "income_time": "2023-01-01 12:00:00",
            "create_time": "2023-01-01 12:00:00",
            "enable": True,
            "income_type_id": 1
        },
        {
            "id": 2,
            "money": 200,
            "account_id": 1,
            "user_id": 1,
            "remark": "测试收入2",
            "income_time": "2023-01-02 12:00:00",
            "create_time": "2023-01-02 12:00:00",
            "enable": True,
            "income_type_id": 2
        }
    ])
    
    # 发送获取所有收入请求
    response = client.get('/api/income', headers=mock_token_header)
    
    # 验证响应
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '查询收入记录列表成功'
    assert len(data['data']) == 2
    assert data['data'][0]['id'] == 1
    assert data['data'][1]['id'] == 2
