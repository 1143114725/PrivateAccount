import pytest
import json
from app import app
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('services.UserService.UserService.register')
def test_register_success(mock_register, client):
    """测试注册成功的情况"""
    # 设置mock返回值，模拟注册成功
    mock_register.return_value = (True, "注册成功", (1, "testuser", "13800138000", 1620000000000))
    
    # 发送注册请求
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '123456',
        'phone': '13800138000'
    })
    
    # 验证响应状态码
    assert response.status_code == 200
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert data['message'] == '注册成功'
    assert data['data'] is not None
    assert data['data']['id'] == 1
    assert data['data']['username'] == 'testuser'
    assert data['data']['phone'] == '13800138000'
    assert data['data']['registration'] == 1620000000000  # 验证registration字段不为null
    
    # 验证mock被调用
    mock_register.assert_called_once_with('testuser', '123456', '13800138000')

@patch('services.UserService.UserService.register')
def test_register_username_empty(mock_register, client):
    """测试用户名为空的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "用户名不能为空", None)
    
    # 发送注册请求，用户名为空
    response = client.post('/register', data={
        'username': '',
        'password': '123456',
        'phone': '13800138000'
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '用户名不能为空'
    assert data['data'] is None

@patch('services.UserService.UserService.register')
def test_register_password_empty(mock_register, client):
    """测试密码为空的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "密码不能为空", None)
    
    # 发送注册请求，密码为空
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '',
        'phone': '13800138000'
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '密码不能为空'
    assert data['data'] is None

@patch('services.UserService.UserService.register')
def test_register_phone_empty(mock_register, client):
    """测试手机号为空的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "手机号不能为空", None)
    
    # 发送注册请求，手机号为空
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '123456',
        'phone': ''
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '手机号不能为空'
    assert data['data'] is None

@patch('services.UserService.UserService.register')
def test_register_phone_invalid(mock_register, client):
    """测试手机号格式不正确的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "手机号格式不正确", None)
    
    # 发送注册请求，手机号格式不正确
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '123456',
        'phone': '1234567890'
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '手机号格式不正确'
    assert data['data'] is None

@patch('services.UserService.UserService.register')
def test_register_username_exists(mock_register, client):
    """测试用户名已存在的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "用户名已存在", None)
    
    # 发送注册请求，用户名为已存在的用户名
    response = client.post('/register', data={
        'username': 'existinguser',
        'password': '123456',
        'phone': '13800138000'
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '用户名已存在'
    assert data['data'] is None

@patch('services.UserService.UserService.register')
def test_register_phone_exists(mock_register, client):
    """测试手机号已存在的情况"""
    # 设置mock返回值，模拟注册失败
    mock_register.return_value = (False, "手机号已存在", None)
    
    # 发送注册请求，手机号为已存在的手机号
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '123456',
        'phone': '13800138000'
    })
    
    # 验证响应状态码
    assert response.status_code == 400
    
    # 验证响应数据
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert data['message'] == '手机号已存在'
    assert data['data'] is None
