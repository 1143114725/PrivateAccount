# 个人财务管理系统API

一个基于Flask框架开发的个人财务管理系统API，提供用户认证、账户管理和消费类型管理等功能，使用统一的API响应模型和错误码系统。

## 功能特性

- ✅ 用户注册功能
- ✅ 用户登录功能（支持用户名或手机号登录）
- ✅ 用户账号注销功能
- ✅ JWT Token认证机制
- ✅ 统一的API响应模型
- ✅ 错误码系统（200-成功，201-token过期，400-请求错误，401-未授权等）
- ✅ 完善的日志系统
- ✅ 数据库连接池管理
- ✅ 账户管理（添加、修改余额、删除、查询）
- ✅ 消费类型管理（新增、修改、删除、查询）
- ✅ 收入类型管理（新增、修改、删除、查询）
- ✅ 余额支持两位小数精度，自动截断处理
- ✅ 单元测试和集成测试

## 技术栈

- **框架**: Flask
- **数据库**: MySQL
- **ORM**: 原生SQL（使用自定义数据库连接池）
- **日志**: 自定义日志工具
- **认证**: JWT Token
- **测试**: Pytest

## 项目结构

```
PrivateAccount/
├── app.py                 # 项目入口文件
├── api/                   # API路由层
│   ├── user.py            # 用户相关路由配置文件
│   ├── account.py         # 账户管理路由配置文件
│   ├── expendtype.py      # 消费类型路由配置文件
│   └── incometype.py      # 收入类型路由配置文件
├── config/                # 配置文件
│   ├── DateBaseConfig.ini # 数据库配置
│   └── LogConfig.ini      # 日志配置
├── dao/                   # 数据访问层
│   ├── UserDAO.py         # 用户数据访问对象
│   ├── AccountDAO.py      # 账户数据访问对象
│   ├── ExpendTypeDAO.py   # 消费类型数据访问对象
│   └── IncomeTypeDAO.py   # 收入类型数据访问对象
├── db/                    # 数据库连接管理
│   └── Database.py        # 数据库连接管理
├── logs/                  # 日志文件目录
├── models/                # 数据模型层
│   ├── BaseModel.py       # 基础模型类
│   ├── UserModel.py       # 用户相关模型
│   ├── AccountModel.py    # 账户相关模型
│   ├── expendtypemodel.py # 消费类型相关模型
│   └── incometypemodel.py # 收入类型相关模型
├── services/              # 业务逻辑层
│   ├── UserService.py     # 用户服务类
│   ├── AccountService.py  # 账户服务类
│   ├── ExpendTypeService.py # 消费类型服务类
│   └── IncomeTypeService.py # 收入类型服务类
├── sql/                   # SQL脚本文件
│   ├── create_tables.sql  # 创建表结构脚本
│   └── init_db.py         # 初始化数据库脚本
├── test/                  # 测试代码
│   ├── api/               # API测试
│   ├── dao/               # DAO层测试
│   ├── services/          # 服务层测试
│   ├── utils/             # 工具类测试
│   └── conftest.py        # 测试配置文件
├── utils/                 # 工具函数
│   ├── ConfigManager.py   # 配置管理工具
│   ├── LogUtils.py        # 日志工具类
│   ├── MD5Utils.py        # MD5加密工具
│   ├── TokenUtils.py      # Token生成与验证工具
│   └── db_pool.py         # 数据库连接池
├── .coverage              # 测试覆盖率文件
├── README.md              # 项目文档
├── app.py                 # 应用入口
├── pytest.ini             # Pytest配置文件
└── requirements.txt       # 项目依赖
```

## 安装和运行

### 1. 环境要求

- Python 3.7+
- MySQL 5.7+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

1. 创建MySQL数据库
2. 执行`sql/create_tables.sql`脚本创建表结构
3. 配置数据库连接信息（在`config/DateBaseConfig.ini`文件中）

### 4. 启动服务

```bash
python app.py
```

服务将在`http://127.0.0.1:8080`启动

## API文档

### 1. 用户认证模块

#### 1.1 登录接口

**URL**: `/login`
**方法**: `POST`
**参数**:
- `username` (可选): 用户名
- `phone` (可选): 手机号
- `password` (必须): 密码

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "登录成功",
  "data": {
    "id": 1,
    "username": "test_user",
    "phone": "13800138000",
    "enable": true,
    "token": "d0ec5125b5c858fe912dd48918585a49",
    "token_expiration_time": 1766750674874
  }
}
```

#### 1.2 注册接口

**URL**: `/register`
**方法**: `POST`
**参数**:
- `username` (必须): 用户名
- `phone` (必须): 手机号
- `password` (必须): 密码

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "test_user",
    "phone": "13800138000",
    "registration": 1766145874849
  }
}
```

#### 1.3 注销账号接口

**URL**: `/api/user/delete`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `user_id` (必须): 用户ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户注销成功",
  "data": null
}
```

### 2. 账户管理模块

#### 2.1 添加账户接口

**URL**: `/api/account`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `account_name` (必须): 账户名称
- `balance` (可选): 账户余额，默认为0。支持任意有效的数字输入，系统将自动截断到两位小数

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户添加成功",
  "data": {
    "id": 1,
    "name": "银行卡",
    "balance": 1000.00,
    "create_time": 1766145874849,
    "update_time": 1766145874849,
    "enable": true
  }
}
```

#### 2.2 修改账户余额接口

**URL**: `/api/account/balance`
**方法**: `PUT`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `account_id` (必须): 账户ID
- `new_balance` (必须): 新的账户余额。支持任意有效的数字输入，系统将自动截断到两位小数

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户余额修改成功",
  "data": {
    "id": 1,
    "name": "银行卡",
    "balance": 2000.50,
    "create_time": 1766145874849,
    "update_time": 1766146874849,
    "enable": true
  }
}
```

#### 2.3 删除账户接口

**URL**: `/api/account`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `account_id` (必须): 账户ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户删除成功",
  "data": null
}
```

#### 2.4 查询用户所有账户接口

**URL**: `/api/account`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "查询用户账户成功",
  "data": [
    {
      "id": 1,
      "name": "银行卡",
      "balance": 1000.25,
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    },
    {
      "id": 2,
      "name": "支付宝",
      "balance": 500.75,
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    }
  ]
}
```

#### 2.5 查询单个账户接口

**URL**: `/api/account/single`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**查询参数**:
- `account_id` (必须): 账户ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "查询账户成功",
  "data": {
    "id": 1,
    "name": "银行卡",
    "balance": 1000.00,
    "create_time": 1766145874849,
    "update_time": 1766145874849,
    "enable": true
  }
}
```

### 3. 消费类型模块

#### 3.1 新增消费类型接口

**URL**: `/api/expendtype`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `type_name` (必须): 消费类型名称
- `enable` (可选): 是否启用，默认为True

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "消费类型新增成功",
  "data": {
    "id": 1,
    "name": "餐饮",
    "create_time": 1766145874849,
    "update_time": 1766145874849,
    "enable": true
  }
}
```

#### 3.2 修改消费类型接口

**URL**: `/api/expendtype`
**方法**: `PUT`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 消费类型ID
- `type_name` (可选): 消费类型名称
- `enable` (可选): 是否启用

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "消费类型修改成功",
  "data": {
    "id": 1,
    "name": "餐饮美食",
    "create_time": 1766145874849,
    "update_time": 1766146874849,
    "enable": true
  }
}
```

#### 3.3 删除消费类型接口

**URL**: `/api/expendtype`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 消费类型ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "消费类型删除成功",
  "data": null
}
```

#### 3.4 查询消费类型接口

**URL**: `/api/expendtype`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**查询参数**:
- `id` (可选): 消费类型ID，如果不传id或id为空则查询所有消费类型

**返回格式**:

查询单个消费类型：
```json
{
  "errorcode": 200,
  "message": "查询消费类型成功",
  "data": [
    {
      "id": 1,
      "name": "餐饮",
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    }
  ]
}
```

查询所有消费类型：
```json
{
  "errorcode": 200,
  "message": "查询消费类型成功",
  "data": [
    {
      "id": 1,
      "name": "餐饮",
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    },
    {
      "id": 2,
      "name": "交通",
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    }
  ]
}
```

### 4. 收入类型模块

#### 4.1 新增收入类型接口

**URL**: `/api/incometype`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `income_type_name` (必须): 收入类型名称
- `enable` (可选): 是否启用，默认为True

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入类型新增成功",
  "data": {
    "id": 1,
    "income_type_name": "工资",
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 4.2 修改收入类型接口

**URL**: `/api/incometype`
**方法**: `PUT`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 收入类型ID
- `income_type_name` (可选): 收入类型名称
- `enable` (可选): 是否启用

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入类型修改成功",
  "data": {
    "id": 1,
    "income_type_name": "工资收入",
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 4.3 删除收入类型接口

**URL**: `/api/incometype`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 收入类型ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入类型删除成功",
  "data": null
}
```

#### 4.4 查询收入类型接口

**URL**: `/api/incometype`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**查询参数**:
- `id` (可选): 收入类型ID，如果不传id或id为空则查询所有收入类型

**返回格式**:

查询单个收入类型：
```json
{
  "errorcode": 200,
  "message": "查询收入类型成功",
  "data": [
    {
      "id": 1,
      "income_type_name": "工资",
      "create_time": "2024-01-01T00:00:00",
      "enable": true
    }
  ]
}
```

查询所有收入类型：
```json
{
  "errorcode": 200,
  "message": "查询收入类型成功",
  "data": [
    {
      "id": 1,
      "income_type_name": "工资",
      "create_time": "2024-01-01T00:00:00",
      "enable": true
    },
    {
      "id": 2,
      "income_type_name": "奖金",
      "create_time": "2024-01-01T00:00:00",
      "enable": true
    }
  ]
}
```


| 错误码 | 描述 |
|-------|------|
| 200 | 成功 |
| 201 | Token过期 |
| 400 | 请求错误 |
| 401 | 未授权（用户名或密码错误） |
| 500 | 服务器内部错误 |

## 响应格式

所有API响应都使用统一的格式：

```json
{
  "errorcode": 200,      // 错误码
  "message": "操作成功", // 响应消息
  "data": null           // 响应数据
}
```

## 测试

### 运行所有测试

```bash
python -m pytest
```

### 运行特定模块测试

```bash
# 运行API测试
python -m pytest test/api/

# 运行服务层测试
python -m pytest test/services/

# 运行DAO层测试
python -m pytest test/dao/
```

## 开发说明

### 模型设计

项目使用统一的基础模型类`BaseModel`，所有API响应模型都继承自该类。

### 服务层设计

业务逻辑封装在服务层，遵循单一职责原则，例如`UserService`负责用户相关的业务逻辑，`AccountService`负责账户相关的业务逻辑。

### 日志系统

使用自定义的日志工具`LogUtils`，支持不同模块的日志记录和配置。

## 安全考虑

- 密码使用MD5加密存储
- 登录接口使用POST方法，避免敏感信息暴露在URL中
- 使用JWT Token进行身份认证
- 实现了Token过期机制
- 敏感操作需要Token验证

## 许可证

MIT License
## 作者

个人财务管理系统开发团队



