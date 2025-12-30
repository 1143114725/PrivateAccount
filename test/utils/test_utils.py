import json
import re
from datetime import datetime, timedelta


def assert_response_success(response, expected_message=None):
    """
    断言响应成功
    
    Args:
        response: Flask测试客户端响应对象
        expected_message: 预期的消息内容（可选）
    """
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['errorcode'] == 200
    
    if expected_message:
        assert data['message'] == expected_message
    else:
        assert '成功' in data['message'] or '查询成功' in data['message']


def assert_response_failure(response, expected_status_code=400, expected_errorcode=None, expected_message=None):
    """
    断言响应失败
    
    Args:
        response: Flask测试客户端响应对象
        expected_status_code: 预期的HTTP状态码
        expected_errorcode: 预期的业务错误码
        expected_message: 预期的错误消息
    """
    assert response.status_code == expected_status_code
    data = json.loads(response.data)
    
    if expected_errorcode:
        assert data['errorcode'] == expected_errorcode
    else:
        assert data['errorcode'] != 200
    
    if expected_message:
        assert expected_message in data['message']
    else:
        assert '失败' in data['message'] or '错误' in data['message'] or '不存在' in data['message']


def validate_token_format(token):
    """
    验证token格式是否正确
    
    Args:
        token: 要验证的token字符串
        
    Returns:
        bool: 如果格式正确返回True，否则返回False
    """
    # JWT格式：header.payload.signature
    token_pattern = re.compile(r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$')
    return bool(token_pattern.match(token))


def create_test_data():
    """
    创建测试数据
    
    Returns:
        dict: 包含各种测试数据的字典
    """
    return {
        'consumption_types': [
            {'id': 1, 'type': '餐饮', 'enable': True},
            {'id': 2, 'type': '交通', 'enable': True},
            {'id': 3, 'type': '购物', 'enable': True},
            {'id': 4, 'type': '娱乐', 'enable': False}
        ],
        'test_user': {
            'id': 1,
            'username': 'test_user',
            'password': 'test_pass',
            'email': 'test@example.com',
            'refresh_token': 'test_refresh_token',
            'token_expiration_time': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        }
    }


def convert_to_dict(model):
    """
    将模型对象转换为字典
    
    Args:
        model: 模型对象
        
    Returns:
        dict: 模型的字典表示
    """
    if hasattr(model, 'to_dict'):
        return model.to_dict()
    elif isinstance(model, (list, tuple)):
        return [convert_to_dict(item) for item in model]
    elif isinstance(model, dict):
        return {k: convert_to_dict(v) for k, v in model.items()}
    else:
        return model
