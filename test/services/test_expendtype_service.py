import pytest
from services.ExpendTypeService import ExpendTypeService
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def test_create_expend_type_success(mock_expend_type_dao, test_expend_type_data):
    """
    测试创建消费类型业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_expend_type_dao.create_expend_type.return_value = (True, test_expend_type_data['id'])
    mock_expend_type_dao.get_expend_type_by_id.return_value = (
        test_expend_type_data['id'],
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable'],
        test_expend_type_data['create_time']
    )
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, expend_type = expend_type_service.create_expend_type(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert expend_type is not None
    assert expend_type[0] == test_expend_type_data['id']
    
    # 验证DAO调用
    mock_expend_type_dao.create_expend_type.assert_called_once_with(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])


def test_create_expend_type_empty_type_name(mock_expend_type_dao):
    """
    测试创建消费类型时类型名称为空
    """
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试 - 类型名称为空
    success, message, expend_type = expend_type_service.create_expend_type("")
    
    # 验证结果
    assert success is False
    assert "不能为空" in message
    assert expend_type is None
    
    # 验证DAO调用
    mock_expend_type_dao.create_expend_type.assert_not_called()


def test_create_expend_type_dao_failure(mock_expend_type_dao, test_expend_type_data):
    """
    测试创建消费类型DAO层失败
    """
    # 配置模拟DAO返回值 - 创建失败
    mock_expend_type_dao.create_expend_type.return_value = (False, 0)
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, expend_type = expend_type_service.create_expend_type(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 验证结果
    assert success is False
    assert "失败" in message
    assert expend_type is None
    
    # 验证DAO调用
    mock_expend_type_dao.create_expend_type.assert_called_once()
    mock_expend_type_dao.get_expend_type_by_id.assert_not_called()


def test_update_expend_type_success(mock_expend_type_dao, test_expend_type_data):
    """
    测试修改消费类型业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_expend_type_dao.get_expend_type_by_id.return_value = (
        test_expend_type_data['id'],
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable'],
        test_expend_type_data['create_time']
    )
    mock_expend_type_dao.update_expend_type.return_value = True
    updated_expend_type = (test_expend_type_data['id'], "更新后的餐饮", False, test_expend_type_data['create_time'])
    mock_expend_type_dao.get_expend_type_by_id.return_value = updated_expend_type
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, updated = expend_type_service.update_expend_type(
        test_expend_type_data['id'],
        "更新后的餐饮",
        False
    )
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert updated is not None
    assert updated[0] == test_expend_type_data['id']
    assert updated[1] == "更新后的餐饮"
    assert updated[2] == False
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_any_call(test_expend_type_data['id'])
    mock_expend_type_dao.update_expend_type.assert_called_once_with(
        test_expend_type_data['id'],
        "更新后的餐饮",
        False
    )
    mock_expend_type_dao.get_expend_type_by_id.assert_any_call(test_expend_type_data['id'])


def test_update_expend_type_empty_id(mock_expend_type_dao):
    """
    测试修改消费类型时ID为空
    """
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试 - ID为空
    success, message, updated = expend_type_service.update_expend_type(None, "更新后的餐饮", False)
    
    # 验证结果
    assert success is False
    assert "不能为空" in message
    assert updated is None
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_not_called()
    mock_expend_type_dao.update_expend_type.assert_not_called()


def test_update_expend_type_no_fields(mock_expend_type_dao):
    """
    测试修改消费类型时未提供任何更新字段
    """
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试 - 未提供更新字段
    success, message, updated = expend_type_service.update_expend_type(1)
    
    # 验证结果
    assert success is False
    assert "未提供任何更新字段" in message
    assert updated is None
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_not_called()
    mock_expend_type_dao.update_expend_type.assert_not_called()


def test_update_expend_type_not_found(mock_expend_type_dao, test_expend_type_data):
    """
    测试修改消费类型时消费类型不存在
    """
    # 配置模拟DAO返回值 - 消费类型不存在
    mock_expend_type_dao.get_expend_type_by_id.return_value = None
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, updated = expend_type_service.update_expend_type(
        test_expend_type_data['id'],
        "更新后的餐饮",
        False
    )
    
    # 验证结果
    assert success is False
    assert "不存在" in message
    assert updated is None
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])
    mock_expend_type_dao.update_expend_type.assert_not_called()


def test_delete_expend_type_success(mock_expend_type_dao, test_expend_type_data):
    """
    测试删除消费类型业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_expend_type_dao.get_expend_type_by_id.return_value = (
        test_expend_type_data['id'],
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable'],
        test_expend_type_data['create_time']
    )
    mock_expend_type_dao.delete_expend_type.return_value = True
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message = expend_type_service.delete_expend_type(test_expend_type_data['id'])
    
    # 验证结果
    assert success is True
    assert "成功" in message
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])
    mock_expend_type_dao.delete_expend_type.assert_called_once_with(test_expend_type_data['id'])


def test_delete_expend_type_empty_id(mock_expend_type_dao):
    """
    测试删除消费类型时ID为空
    """
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试 - ID为空
    success, message = expend_type_service.delete_expend_type(None)
    
    # 验证结果
    assert success is False
    assert "不能为空" in message
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_not_called()
    mock_expend_type_dao.delete_expend_type.assert_not_called()


def test_delete_expend_type_not_found(mock_expend_type_dao, test_expend_type_data):
    """
    测试删除消费类型时消费类型不存在
    """
    # 配置模拟DAO返回值 - 消费类型不存在
    mock_expend_type_dao.get_expend_type_by_id.return_value = None
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message = expend_type_service.delete_expend_type(test_expend_type_data['id'])
    
    # 验证结果
    assert success is False
    assert "不存在" in message
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])
    mock_expend_type_dao.delete_expend_type.assert_not_called()


def test_get_expend_type_by_id_success(mock_expend_type_dao, test_expend_type_data):
    """
    测试根据ID查询消费类型业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_expend_type_dao.get_expend_type_by_id.return_value = (
        test_expend_type_data['id'],
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable'],
        test_expend_type_data['create_time']
    )
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, expend_type = expend_type_service.get_expend_type_by_id(test_expend_type_data['id'])
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert expend_type is not None
    assert expend_type[0] == test_expend_type_data['id']
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])


def test_get_expend_type_by_id_empty_id(mock_expend_type_dao):
    """
    测试根据ID查询消费类型时ID为空
    """
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试 - ID为空
    success, message, expend_type = expend_type_service.get_expend_type_by_id(None)
    
    # 验证结果
    assert success is False
    assert "不能为空" in message
    assert expend_type is None
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_not_called()


def test_get_expend_type_by_id_not_found(mock_expend_type_dao, test_expend_type_data):
    """
    测试根据ID查询消费类型时消费类型不存在
    """
    # 配置模拟DAO返回值 - 消费类型不存在
    mock_expend_type_dao.get_expend_type_by_id.return_value = None
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, expend_type = expend_type_service.get_expend_type_by_id(test_expend_type_data['id'])
    
    # 验证结果
    assert success is False
    assert "不存在" in message
    assert expend_type is None
    
    # 验证DAO调用
    mock_expend_type_dao.get_expend_type_by_id.assert_called_once_with(test_expend_type_data['id'])


def test_get_all_expend_types_success(mock_expend_type_dao, test_expend_type_data):
    """
    测试查询所有消费类型业务逻辑成功
    """
    # 配置模拟DAO返回值
    mock_expend_type_dao.get_all_expend_types.return_value = [
        (test_expend_type_data['id'], test_expend_type_data['expend_type_name'], test_expend_type_data['enable'], test_expend_type_data['create_time']),
        (2, "交通", True, '2023-01-01 00:00:00')
    ]
    
    # 创建Service实例
    expend_type_service = ExpendTypeService()
    
    # 执行测试
    success, message, expend_types = expend_type_service.get_all_expend_types()
    
    # 验证结果
    assert success is True
    assert "成功" in message
    assert expend_types is not None
    assert len(expend_types) == 2
    
    # 验证DAO调用
    mock_expend_type_dao.get_all_expend_types.assert_called_once()