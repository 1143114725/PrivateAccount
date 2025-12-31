import pytest
import json
from unittest.mock import patch
from services.ExpendTypeService import ExpendTypeService
from services.UserService import UserService
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture
def mock_expend_type_service():
    """
    创建模拟的ExpendTypeService
    """
    with patch('api.expendtype.expend_type_service') as mock_service:
        yield mock_service


@pytest.fixture
def mock_user_service():
    """
    创建模拟的UserService
    """
    with patch('api.expendtype.user_service') as mock_service:
        yield mock_service


@pytest.fixture
def mock_token_validation():
    """
    创建模拟的token验证
    """
    with patch('api.expendtype.TokenUtils.validate_token') as mock_validate:
        mock_validate.return_value = True
        yield mock_validate


@pytest.fixture
def valid_headers():
    """
    创建有效的请求头
    """
    return {
        'token': 'valid_token_123',
        'userid': '1'
    }


@pytest.fixture
def invalid_headers():
    """
    创建无效的请求头
    """
    return {
        'token': 'invalid_token_456',
        'userid': '1'
    }


@pytest.fixture
def missing_headers():
    """
    创建缺少必要参数的请求头
    """
    return {
        'token': '',
        'userid': ''
    }


def test_addexpendtype_success(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试新增消费类型API成功
    """
    # 配置模拟
    test_data = {'expend_type_name': '餐饮', 'enable': True}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    mock_expend_type_service.create_expend_type.return_value = (
        True, "消费类型创建成功", (1, '餐饮', True)
    )
    
    # 执行测试
    response = test_client.post(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert "成功" in data['message']
    assert data['data'] is not None
    assert data['data']['expend_type_name'] == '餐饮'
    
    # 验证Service调用
    mock_expend_type_service.create_expend_type.assert_called_once_with(
        '餐饮', True
    )


def test_addexpendtype_empty_type_name(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试新增消费类型时类型名称为空
    """
    # 配置模拟
    test_data = {'expend_type_name': '', 'enable': True}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    
    # 执行测试
    response = test_client.post(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert "不能为空" in data['message']
    
    # 验证Service未被调用
    mock_expend_type_service.create_expend_type.assert_not_called()


def test_addexpendtype_invalid_token(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    invalid_headers
):
    """
    测试新增消费类型时token无效
    """
    # 配置模拟 - token验证失败
    mock_token_validation.return_value = False
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    
    # 执行测试
    response = test_client.post(
        '/api/expendtype',
        data={'expend_type_name': '餐饮', 'enable': True},
        headers=invalid_headers
    )
    
    # 验证结果
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['errorcode'] == 401
    assert "验证失败" in data['message']
    
    # 验证Service未被调用
    mock_expend_type_service.create_expend_type.assert_not_called()


def test_updateexpendtype_success(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试修改消费类型API成功
    """
    # 配置模拟
    test_data = {'id': '1', 'expend_type_name': '更新后的餐饮', 'enable': 'false'}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    mock_expend_type_service.update_expend_type.return_value = (
        True, "消费类型修改成功", (1, '更新后的餐饮', False)
    )
    
    # 执行测试
    response = test_client.put(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert "成功" in data['message']
    assert data['data']['expend_type_name'] == '更新后的餐饮'
    assert data['data']['enable'] is False
    
    # 验证Service调用
    mock_expend_type_service.update_expend_type.assert_called_once_with(1, '更新后的餐饮', False)


def test_updateexpendtype_invalid_id(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试修改消费类型时ID无效
    """
    # 配置模拟
    test_data = {'id': 'invalid_id', 'expend_type_name': '更新后的餐饮', 'enable': 'false'}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    
    # 执行测试
    response = test_client.put(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert "必须是有效的整数" in data['message']
    
    # 验证Service未被调用
    mock_expend_type_service.update_expend_type.assert_not_called()


def test_deleteexpendtype_success(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试删除消费类型API成功
    """
    # 配置模拟
    test_data = {'id': '1'}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    mock_expend_type_service.delete_expend_type.return_value = (
        True, "消费类型删除成功"
    )
    
    # 执行测试
    response = test_client.delete(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert "成功" in data['message']
    
    # 验证Service调用
    mock_expend_type_service.delete_expend_type.assert_called_once_with(1)


def test_deleteexpendtype_invalid_id(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试删除消费类型时ID无效
    """
    # 配置模拟
    test_data = {'id': 'invalid_id'}
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    
    # 执行测试
    response = test_client.delete(
        '/api/expendtype',
        data=test_data,
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['errorcode'] == 400
    assert "必须是有效的整数" in data['message']
    
    # 验证Service未被调用
    mock_expend_type_service.delete_expend_type.assert_not_called()


def test_getexpendtype_success(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试查询单个消费类型API成功
    """
    # 配置模拟
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    mock_expend_type_service.get_expend_type_by_id.return_value = (
        True, "查询消费类型成功", (1, '餐饮', True)
    )
    
    # 执行测试
    response = test_client.get(
        '/api/expendtype?id=1',
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert "成功" in data['message']
    assert isinstance(data['data'], list)  # 验证返回的是数组
    assert len(data['data']) == 1  # 验证数组包含一个元素
    assert data['data'][0]['id'] == 1
    assert data['data'][0]['expend_type_name'] == '餐饮'
    
    # 验证Service调用
    mock_expend_type_service.get_expend_type_by_id.assert_called_once_with(1)


def test_getexpendtypes_success(
    test_client, 
    mock_expend_type_service, 
    mock_user_service, 
    mock_token_validation, 
    valid_headers
):
    """
    测试查询所有消费类型API成功
    """
    # 配置模拟
    mock_user_service.get_user_by_id.return_value = (
        1, 'test_user', 'test_pass', 'test@example.com', 
        'valid_token_123', '2023-12-31 23:59:59'
    )
    mock_expend_type_service.get_all_expend_types.return_value = (
        True, "查询所有消费类型成功", [
            (1, '餐饮', True),
            (2, '交通', True),
            (3, '购物', True)
        ]
    )
    
    # 执行测试
    response = test_client.get(
        '/api/expendtype',
        headers=valid_headers
    )
    
    # 验证结果
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    assert "成功" in data['message']
    assert len(data['data']) == 3
    assert data['data'][0]['expend_type_name'] == '餐饮'
    assert data['data'][1]['expend_type_name'] == '交通'
    assert data['data'][2]['expend_type_name'] == '购物'
    
    # 验证Service调用
    mock_expend_type_service.get_all_expend_types.assert_called_once()


def test_missing_headers(test_client, mock_token_validation, missing_headers):
    """
    测试缺少必要请求头
    """
    # 执行测试
    response = test_client.get(
            '/api/expendtype',
            headers=missing_headers
        )
    
    # 验证结果
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['errorcode'] == 401
    assert "未提供token" in data['message'] or "未提供userid" in data['message']
