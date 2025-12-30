import pytest
from dao.ExpendTypeDAO import ExpendTypeDAO
from unittest.mock import patch
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def test_create_expend_type_success(mock_database, test_expend_type_data):
    """
    测试创建消费类型成功
    """
    # 配置模拟
    mock_cursor = mock_database.cur
    mock_cursor.lastrowid = test_expend_type_data['id']
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success, expend_type_id = expend_type_dao.create_expend_type(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 验证结果
    assert success is True
    assert expend_type_id == test_expend_type_data['id']
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.commit.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_create_expend_type_failure(mock_database, test_expend_type_data):
    """
    测试创建消费类型失败
    """
    # 配置模拟 - 执行失败
    mock_database.execute.return_value = False
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success, expend_type_id = expend_type_dao.create_expend_type(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 验证结果
    assert success is False
    assert expend_type_id == 0
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.rollback.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_create_expend_type_exception(mock_database, test_expend_type_data):
    """
    测试创建消费类型时发生异常
    """
    # 配置模拟 - 抛出异常
    mock_database.connect.side_effect = Exception("Database connection error")
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success, expend_type_id = expend_type_dao.create_expend_type(
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 验证结果
    assert success is False
    assert expend_type_id == 0
    
    # 验证调用
    mock_database.disconnect.assert_called_once()


def test_update_expend_type_success(mock_database, test_expend_type_data):
    """
    测试更新消费类型成功
    """
    # 配置模拟 - 影响行数为1
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 1
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success = expend_type_dao.update_expend_type(
        test_expend_type_data['id'],
        "更新后的餐饮",
        False
    )
    
    # 验证结果
    assert success is True
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.commit.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_update_expend_type_not_found(mock_database, test_expend_type_data):
    """
    测试更新消费类型时未找到记录
    """
    # 配置模拟 - 影响行数为0
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 0
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success = expend_type_dao.update_expend_type(
        test_expend_type_data['id'],
        "更新后的餐饮",
        False
    )
    
    # 验证结果
    assert success is False
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.rollback.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_delete_expend_type_success(mock_database, test_expend_type_data):
    """
    测试删除消费类型成功
    """
    # 配置模拟 - 影响行数为1
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 1
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success = expend_type_dao.delete_expend_type(test_expend_type_data['id'])
    
    # 验证结果
    assert success is True
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.commit.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_delete_expend_type_not_found(mock_database, test_expend_type_data):
    """
    测试删除消费类型时未找到记录
    """
    # 配置模拟 - 影响行数为0
    mock_cursor = mock_database.cur
    mock_cursor.rowcount = 0
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    success = expend_type_dao.delete_expend_type(test_expend_type_data['id'])
    
    # 验证结果
    assert success is False
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.rollback.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_get_expend_type_by_id_found(mock_database, test_expend_type_data):
    """
    测试根据ID查询消费类型成功
    """
    # 配置模拟 - 返回测试数据
    mock_cursor = mock_database.cur
    mock_cursor.fetchone.return_value = (
        test_expend_type_data['id'],
        test_expend_type_data['expend_type_name'],
        test_expend_type_data['enable']
    )
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    expend_type = expend_type_dao.get_expend_type_by_id(test_expend_type_data['id'])
    
    # 验证结果
    assert expend_type is not None
    assert expend_type[0] == test_expend_type_data['id']
    assert expend_type[1] == test_expend_type_data['expend_type_name']
    assert expend_type[2] == test_expend_type_data['enable']
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_get_expend_type_by_id_not_found(mock_database, test_expend_type_data):
    """
    测试根据ID查询消费类型未找到
    """
    # 配置模拟 - 返回None
    mock_cursor = mock_database.cur
    mock_cursor.fetchone.return_value = None
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    expend_type = expend_type_dao.get_expend_type_by_id(test_expend_type_data['id'])
    
    # 验证结果
    assert expend_type is None
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_get_all_expend_types(mock_database, test_expend_type_data):
    """
    测试查询所有消费类型
    """
    # 配置模拟 - 返回多条测试数据
    mock_cursor = mock_database.cur
    mock_cursor.fetchall.return_value = [
        (test_expend_type_data['id'], test_expend_type_data['expend_type_name'], test_expend_type_data['enable']),
        (2, "交通", True),
        (3, "购物", True)
    ]
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    expend_types = expend_type_dao.get_all_expend_types()
    
    # 验证结果
    assert len(expend_types) == 3
    assert expend_types[0][0] == test_expend_type_data['id']
    assert expend_types[1][1] == "交通"
    assert expend_types[2][2] == True
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.disconnect.assert_called_once()


def test_get_all_expend_types_empty(mock_database):
    """
    测试查询所有消费类型时返回空列表
    """
    # 配置模拟 - 返回空列表
    mock_cursor = mock_database.cur
    mock_cursor.fetchall.return_value = None
    
    # 创建DAO实例
    expend_type_dao = ExpendTypeDAO()
    
    # 执行测试
    expend_types = expend_type_dao.get_all_expend_types()
    
    # 验证结果
    assert expend_types == []
    
    # 验证调用
    mock_database.connect.assert_called_once()
    mock_database.execute.assert_called_once()
    mock_database.disconnect.assert_called_once()
