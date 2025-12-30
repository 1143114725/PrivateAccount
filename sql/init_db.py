#!/usr/bin/env python3
"""
数据库初始化脚本
用于执行SQL建表语句，初始化数据库表结构
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.Database import Database
from utils.LogUtils import LogUtils

def main():
    # 初始化日志
    logger = LogUtils.get_instance('DatabaseInit')
    logger.info("开始执行数据库初始化脚本")
    
    try:
        # 创建数据库连接
        db = Database()
        
        # 读取SQL文件
        sql_file_path = os.path.join(os.path.dirname(__file__), 'create_tables.sql')
        logger.info(f"读取SQL文件: {sql_file_path}")
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        logger.info("SQL文件读取完成")
        
        # 分割SQL语句（以分号分割）
        import re
        # 使用正则表达式分割SQL语句，处理可能存在的字符串内分号
        sql_statements = re.split(r';(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)', sql_content)
        logger.info(f"共解析到 {len(sql_statements)} 条SQL语句")
        
        # 执行每条SQL语句
        success_count = 0
        failed_count = 0
        
        for i, sql in enumerate(sql_statements):
            sql = sql.strip()
            if not sql:  # 跳过空语句
                continue
            
            logger.info(f"执行SQL语句 {i+1}: {sql[:50]}...")
            
            try:
                if db.connect():
                    if db.execute(sql):
                        db.commit()
                        logger.info(f"SQL语句 {i+1} 执行成功")
                        success_count += 1
                    else:
                        db.rollback()
                        logger.error(f"SQL语句 {i+1} 执行失败")
                        failed_count += 1
                else:
                    logger.error(f"SQL语句 {i+1} 执行失败: 无法连接数据库")
                    failed_count += 1
            except Exception as e:
                logger.error(f"SQL语句 {i+1} 执行异常: {e}")
                failed_count += 1
            finally:
                db.disconnect()
        
        # 输出执行结果
        logger.info("数据库初始化完成")
        logger.info(f"执行成功: {success_count} 条")
        logger.info(f"执行失败: {failed_count} 条")
        
        if failed_count > 0:
            logger.error("数据库初始化过程中存在失败的SQL语句")
            return 1
        else:
            logger.info("数据库初始化全部成功")
            return 0
            
    except Exception as e:
        logger.error(f"数据库初始化脚本执行异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())