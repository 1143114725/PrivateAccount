# 个人财务管理系统API

个人财务管理系统API是一个基于Flask框架开发的轻量级财务工具，帮助个人用户和小型家庭便捷地管理收支记录、跟踪消费习惯、分析财务状况。系统提供完整的用户认证、账户管理、收支记录管理和消费/收入类型管理功能，采用统一的API响应模型和错误码系统，确保接口的一致性和易用性。

## 功能特性

- ✅ 用户注册功能
- ✅ 用户登录功能（支持用户名或手机号登录）
- ✅ 用户账号注销功能
- ✅ JWT Token认证机制（已抽离为独立模块）
- ✅ 统一的API响应模型
- ✅ 错误码系统（200-成功，201-token过期，400-请求错误，401-未授权等）
- ✅ 完善的日志系统（无print语句，统一使用日志记录）
- ✅ 数据库连接池管理
- ✅ 账户管理（添加、修改余额、删除、查询）
- ✅ 消费类型管理（新增、修改、删除、查询）
- ✅ 收入类型管理（新增、修改、删除、查询）
- ✅ 支出记录管理（新增、修改、删除、查询）
- ✅ 收入记录管理（新增、修改、删除、查询）
- ✅ 余额支持两位小数精度，自动截断处理
- ✅ 单元测试和集成测试（所有测试文件统一放在test目录）
- ✅ 支出记录与账户余额的事务一致性
- ✅ 收入记录与账户余额的事务一致性
- ✅ RESTful API设计（所有接口参数通过请求体或查询字符串传递，不在URL路径中包含参数）
- ✅ 支持重复内容更新（更新操作时，即使新内容与原内容相同也会返回成功）

## 技术栈

- **框架**: Flask
- **数据库**: MySQL
- **ORM**: 原生SQL（使用自定义数据库连接池）
- **日志**: 自定义日志工具
- **认证**: JWT Token
- **测试**: Pytest
- **部署**: 支持Docker容器化部署

### 技术栈选择理由

1. **Flask框架**：选择Flask是因为它轻量级、灵活且易于学习，适合快速开发RESTful API。Flask的扩展性强，可以根据需要添加各种插件，同时它的路由系统非常适合构建API接口。

2. **MySQL数据库**：选择MySQL是因为它是一个成熟、稳定且广泛使用的关系型数据库，支持复杂的查询和事务处理，适合存储结构化的财务数据。MySQL的性能稳定，社区支持丰富，适合中小型应用使用。

3. **原生SQL**：虽然ORM框架可以提高开发效率，但原生SQL可以更好地控制查询性能，尤其是对于复杂的财务数据查询和分析。自定义的数据库连接池可以有效管理数据库连接资源，提高系统性能。

4. **自定义日志工具**：自定义日志工具可以根据项目需求灵活配置日志格式、级别和输出方式，满足不同环境下的日志管理需求。相比第三方日志库，自定义工具可以更好地集成到项目架构中。

5. **JWT Token认证**：JWT Token是一种轻量级的认证机制，适合前后端分离的API架构。它可以在客户端存储认证信息，减少服务器端的会话管理压力，同时支持跨域认证。

6. **Pytest测试框架**：Pytest是一个功能强大、灵活的测试框架，支持单元测试、集成测试和功能测试。它的插件生态丰富，可以方便地实现测试覆盖率统计、测试报告生成等功能。

7. **Docker容器化部署**：Docker可以将应用程序及其依赖打包成一个容器，确保应用在不同环境中的一致性运行。容器化部署简化了应用的部署和管理流程，提高了开发和运维的效率。

## 项目结构

```
PrivateAccount/
├── app.py                 # 项目入口文件
├── api/                   # API路由层
│   ├── user.py            # 用户相关路由配置文件
│   ├── account.py         # 账户管理路由配置文件
│   ├── expendtype.py      # 消费类型路由配置文件
│   ├── incometype.py      # 收入类型路由配置文件
│   ├── expend.py          # 支出记录路由配置文件
│   └── income.py          # 收入记录路由配置文件
├── config/                # 配置文件
│   ├── DateBaseConfig.ini # 数据库配置
│   └── LogConfig.ini      # 日志配置
├── dao/                   # 数据访问层
│   ├── UserDAO.py         # 用户数据访问对象
│   ├── AccountDAO.py      # 账户数据访问对象
│   ├── ExpendTypeDAO.py   # 消费类型数据访问对象
│   ├── IncomeTypeDAO.py   # 收入类型数据访问对象
│   ├── ExpendDAO.py       # 支出记录数据访问对象
│   └── IncomeDAO.py       # 收入记录数据访问对象
├── db/                    # 数据库连接管理
│   └── Database.py        # 数据库连接管理
├── logs/                  # 日志文件目录
├── models/                # 数据模型层
│   ├── BaseModel.py       # 基础模型类
│   ├── UserModel.py       # 用户相关模型
│   ├── AccountModel.py    # 账户相关模型
│   ├── expendtypemodel.py # 消费类型相关模型
│   ├── incometypemodel.py # 收入类型相关模型
│   ├── Expend.py          # 支出记录相关模型
│   └── Income.py          # 收入记录相关模型
├── services/              # 业务逻辑层
│   ├── UserService.py     # 用户服务类
│   ├── AccountService.py  # 账户服务类
│   ├── ExpendTypeService.py # 消费类型服务类
│   ├── IncomeTypeService.py # 收入类型服务类
│   ├── ExpendService.py   # 支出记录服务类
│   └── IncomeService.py   # 收入记录服务类
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

### 项目结构详细说明

| 目录/文件 | 说明 |
|----------|------|
| `app.py` | 项目入口文件，负责初始化Flask应用、注册路由和启动服务 |
| `api/` | API路由层，包含所有API接口的路由配置和请求处理 |
| `api/user.py` | 用户相关接口配置，包含登录、注册、注销等接口 |
| `api/account.py` | 账户管理接口配置，包含账户的增删改查接口 |
| `api/expendtype.py` | 消费类型接口配置，包含消费类型的增删改查接口 |
| `api/incometype.py` | 收入类型接口配置，包含收入类型的增删改查接口 |
| `api/expend.py` | 支出记录接口配置，包含支出记录的增删改查接口 |
| `api/income.py` | 收入记录接口配置，包含收入记录的增删改查接口 |
| `config/` | 配置文件目录，包含数据库、日志等系统配置 |
| `config/DateBaseConfig.ini` | 数据库连接配置文件，包含数据库地址、端口、用户名、密码等信息 |
| `config/LogConfig.ini` | 日志配置文件，包含日志级别、格式、输出路径等信息 |
| `dao/` | 数据访问层，负责与数据库交互，实现数据的增删改查操作 |
| `db/` | 数据库连接管理目录，包含数据库连接池的实现 |
| `logs/` | 日志文件存储目录，系统运行产生的日志文件将保存在此目录 |
| `models/` | 数据模型层，包含API响应模型和业务数据模型的定义 |
| `services/` | 业务逻辑层，封装核心业务逻辑，实现服务间的解耦 |
| `sql/` | SQL脚本目录，包含数据库表结构创建和初始化脚本 |
| `test/` | 测试代码目录，包含API、服务层、DAO层等模块的测试用例 |
| `utils/` | 工具函数目录，包含配置管理、日志工具、加密工具等通用工具 |
| `.coverage` | 测试覆盖率文件，记录测试用例的代码覆盖率信息 |
| `.gitignore` | Git忽略文件配置，指定不需要纳入版本控制的文件和目录 |
| `LICENSE` | 项目许可证文件，说明项目的开源协议 |
| `pytest.ini` | Pytest测试框架配置文件，包含测试相关的配置项 |
| `requirements.txt` | 项目依赖文件，列出项目所需的Python包及其版本 |

## 安装和运行

### 1. 环境要求

- Python 3.7+
- MySQL 5.7+
- Git

### 2. 安装依赖

```bash
# 克隆项目
git clone <项目地址>
cd PrivateAccount

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置数据库

1. **创建数据库**
   ```sql
   CREATE DATABASE private_account CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **执行表结构脚本**
   ```bash
   mysql -u root -p private_account < sql/create_tables.sql
   ```

3. **配置数据库连接**
   编辑 `config/DateBaseConfig.ini` 文件，设置数据库连接信息：
   ```ini
   [mysql]
   host=localhost
   port=3306
   user=root
   password=your_password
   database=private_account
   charset=utf8mb4
   mincached=5
   maxcached=20
   maxconnections=20
   blocking=True
   ```

### 4. 配置日志

编辑 `config/LogConfig.ini` 文件，设置日志配置：
```ini
[logging]
level=INFO
log_file=logs/app.log
max_bytes=10485760
backup_count=5
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 5. 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:8080` 启动

## API文档

### API版本

当前API版本：v1

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

### 5. 支出记录管理模块

#### 5.1 新增支出记录接口

**URL**: `/api/expend`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `money` (必须): 支出金额
- `account_id` (必须): 账户ID
- `expend_type_id` (必须): 支出类型ID
- `remark` (可选): 支出备注
- `expend_time` (可选): 支出时间（格式：YYYY-MM-DD HH:MM:SS 或毫秒级时间戳）
- `enable` (可选): 是否启用，默认为True

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "支出记录新增成功",
  "data": {
    "id": 1,
    "money": 50.50,
    "remark": "午餐",
    "expend_time": "2024-01-01 12:00:00",
    "account_id": 1,
    "expend_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 5.2 修改支出记录接口

**URL**: `/api/expend`
**方法**: `PUT`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 支出记录ID
- `money` (可选): 支出金额
- `account_id` (可选): 账户ID
- `expend_type_id` (可选): 支出类型ID
- `remark` (可选): 支出备注
- `expend_time` (可选): 支出时间（格式：YYYY-MM-DD HH:MM:SS 或毫秒级时间戳）
- `enable` (可选): 是否启用

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "支出记录修改成功",
  "data": {
    "id": 1,
    "money": 60.00,
    "remark": "午餐",
    "expend_time": "2024-01-01 12:00:00",
    "account_id": 1,
    "expend_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 5.3 删除支出记录接口

**URL**: `/api/expend`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 支出记录ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "支出记录删除成功",
  "data": null
}
```

#### 5.4 查询支出记录接口

**URL**: `/api/expend`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**查询参数**:
- `id` (可选): 支出记录ID，提供id则获取单个记录，不提供则获取所有记录

**返回格式**:

查询单个支出记录：
```json
{
  "errorcode": 200,
  "message": "查询支出记录成功",
  "data": {
    "id": 1,
    "money": 50.50,
    "remark": "午餐",
    "expend_time": "2024-01-01 12:00:00",
    "account_id": 1,
    "expend_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

查询所有支出记录：
```json
{
  "errorcode": 200,
  "message": "查询支出记录成功",
  "data": [
    {
      "id": 1,
      "money": 50.50,
      "remark": "午餐",
      "expend_time": "2024-01-01 12:00:00",
      "account_id": 1,
      "expend_type_id": 1,
      "create_time": "2024-01-01T00:00:00",
      "enable": true
    },
    {
      "id": 2,
      "money": 100.00,
      "remark": "购物",
      "expend_time": "2024-01-02 14:00:00",
      "account_id": 1,
      "expend_type_id": 2,
      "create_time": "2024-01-02T00:00:00",
      "enable": true
    }
  ]
}
```

### 6. 收入记录管理模块

#### 6.1 新增收入记录接口

**URL**: `/api/income`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `money` (必须): 收入金额
- `account_id` (必须): 账户ID
- `income_type_id` (必须): 收入类型ID
- `remark` (可选): 收入备注
- `income_time` (可选): 收入时间（格式：YYYY-MM-DD HH:MM:SS 或毫秒级时间戳）
- `enable` (可选): 是否启用，默认为True

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入记录新增成功",
  "data": {
    "id": 1,
    "money": 5000.00,
    "remark": "工资收入",
    "income_time": "2024-01-01 09:00:00",
    "account_id": 1,
    "income_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 6.2 修改收入记录接口

**URL**: `/api/income`
**方法**: `PUT`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 收入记录ID
- `money` (可选): 收入金额
- `account_id` (可选): 账户ID
- `income_type_id` (可选): 收入类型ID
- `remark` (可选): 收入备注
- `income_time` (可选): 收入时间（格式：YYYY-MM-DD HH:MM:SS 或毫秒级时间戳）
- `enable` (可选): 是否启用

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入记录修改成功",
  "data": {
    "id": 1,
    "money": 6000.00,
    "remark": "工资收入（含奖金）",
    "income_time": "2024-01-01 09:00:00",
    "account_id": 1,
    "income_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

#### 6.3 删除收入记录接口

**URL**: `/api/income`
**方法**: `DELETE`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `id` (必须): 收入记录ID

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "收入记录删除成功",
  "data": null
}
```

#### 6.4 查询收入记录接口

**URL**: `/api/income`
**方法**: `GET`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**查询参数**:
- `id` (可选): 收入记录ID，提供id则获取单个记录，不提供则获取所有记录

**返回格式**:

查询单个收入记录：
```json
{
  "errorcode": 200,
  "message": "查询收入记录成功",
  "data": {
    "id": 1,
    "money": 5000.00,
    "remark": "工资收入",
    "income_time": "2024-01-01 09:00:00",
    "account_id": 1,
    "income_type_id": 1,
    "create_time": "2024-01-01T00:00:00",
    "enable": true
  }
}
```

查询所有收入记录：
```json
{
  "errorcode": 200,
  "message": "查询收入记录成功",
  "data": [
    {
      "id": 1,
      "money": 5000.00,
      "remark": "工资收入",
      "income_time": "2024-01-01 09:00:00",
      "account_id": 1,
      "income_type_id": 1,
      "create_time": "2024-01-01T00:00:00",
      "enable": true
    },
    {
      "id": 2,
      "money": 1000.00,
      "remark": "奖金收入",
      "income_time": "2024-01-02 10:00:00",
      "account_id": 1,
      "income_type_id": 2,
      "create_time": "2024-01-02T00:00:00",
      "enable": true
    }
  ]
}
```

## 错误码说明

| 错误码 | 描述 |
|-------|------|
| 200 | 操作成功 |
| 201 | Token已过期或无效 |
| 400 | 请求错误（参数错误、格式错误、参数为空等） |
| 401 | 未授权（用户名/密码错误、未提供token、token验证失败等） |
| 403 | 无权操作（尝试访问不属于自己的资源） |
| 404 | 资源不存在（请求的资源不存在） |
| 500 | 服务器内部错误（数据库错误、代码异常等） |

## 响应格式

所有API响应都使用统一的格式：

```json
{
  "errorcode": 200,      // 错误码
  "message": "操作成功", // 响应消息
  "data": null           // 响应数据
}
```

## 安全措施

### 1. 数据加密
- **密码加密**：用户密码使用MD5算法加密后存储在数据库中，确保密码安全
- **数据传输**：建议在生产环境中使用HTTPS协议，确保数据在传输过程中的安全性

### 2. 认证与授权
- **JWT Token认证**：采用JWT Token机制进行用户认证，Token具有有效期，过期后需要重新登录
- **接口权限控制**：所有需要用户身份的接口都通过`@token_required`装饰器进行保护
- **用户权限验证**：确保用户只能访问和操作自己的资源，防止越权操作

### 3. 输入验证
- **参数验证**：所有API接口对输入参数进行严格验证，包括非空检查、格式验证等
- **SQL注入防护**：使用参数化查询，防止SQL注入攻击
- **XSS防护**：对用户输入的内容进行适当过滤和转义，防止XSS攻击

### 4. 日志与监控
- **操作日志**：记录用户的关键操作，便于审计和故障排查
- **错误日志**：详细记录系统错误信息，包括错误类型、错误位置等
- **数据库连接池**：使用数据库连接池管理数据库连接，避免资源泄露和连接数过多

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

### 查看测试覆盖率

```bash
python -m pytest --cov=. --cov-report=html
```

## 开发流程与最佳实践

### 1. 开发流程

1. **需求分析**：明确功能需求，制定开发计划
2. **数据库设计**：根据需求设计数据库表结构，添加必要的索引
3. **代码实现**：按照分层架构实现功能
   - 数据模型层（models）：定义数据结构
   - 数据访问层（dao）：实现数据库操作
   - 业务逻辑层（services）：封装业务逻辑
   - API路由层（api）：处理HTTP请求和响应
4. **单元测试**：为每个模块编写单元测试，确保代码质量
5. **集成测试**：测试模块间的协作
6. **代码审查**：提交代码前进行代码审查
7. **部署测试**：在测试环境中验证功能

### 2. 最佳实践

1. **代码风格**：
   - 遵循PEP 8编码规范
   - 使用清晰的变量名和函数名
   - 添加适当的注释，说明复杂逻辑

2. **错误处理**：
   - 使用统一的错误码系统
   - 捕获并记录所有异常
   - 向用户返回友好的错误信息

3. **日志记录**：
   - 使用统一的日志工具（LogUtils）
   - 记录关键操作和错误信息
   - 避免使用print语句

4. **性能优化**：
   - 使用数据库连接池
   - 优化SQL查询
   - 合理使用缓存

5. **安全考虑**：
   - 验证所有用户输入
   - 保护敏感数据
   - 实现适当的访问控制

## 开发说明

### 模型设计

项目使用统一的基础模型类`BaseModel`，所有API响应模型都继承自该类，确保响应格式的一致性。

### 服务层设计

业务逻辑封装在服务层，遵循单一职责原则：
- `UserService` 负责用户相关的业务逻辑
- `AccountService` 负责账户相关的业务逻辑
- `ExpendTypeService` 负责消费类型相关的业务逻辑
- `IncomeTypeService` 负责收入类型相关的业务逻辑
- `ExpendService` 负责支出记录相关的业务逻辑
- `IncomeService` 负责收入记录相关的业务逻辑

### 日志系统

使用自定义的日志工具`LogUtils`，支持不同模块的日志记录和配置：
- 支持日志分级（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 支持文件和控制台输出
- 支持日志文件轮转
- 在日志器初始化失败时提供基本的错误记录功能

### 数据库连接管理

使用自定义的数据库连接池管理数据库连接：
- 支持连接池配置（最小连接数、最大连接数等）
- 自动处理连接的获取和释放
- 支持事务管理

## 安全考虑

- **密码安全**: 使用MD5加密存储用户密码
- **身份认证**: 使用JWT Token进行身份认证
- **Token过期**: 实现Token过期机制，默认过期时间为7天
- **敏感操作保护**: 所有敏感操作都需要Token验证
- **SQL注入防护**: 使用参数化查询，避免SQL注入攻击
- **输入验证**: 对所有用户输入进行严格验证

## 部署指南

### 开发环境部署

1. 按照「安装和运行」部分的步骤配置开发环境
2. 启动服务：`python app.py`

### 生产环境部署

#### 1. 环境变量配置

在生产环境中，建议使用环境变量配置敏感信息，避免硬编码到配置文件中：

```bash
# 数据库连接信息
export DB_HOST="localhost"
export DB_PORT="3306"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
export DB_NAME="private_account"

# JWT配置
export JWT_SECRET_KEY="your_jwt_secret_key"
export JWT_EXPIRATION_DAYS="7"

# 日志配置
export LOG_LEVEL="INFO"
export LOG_FILE="/var/log/private_account/app.log"
```

#### 2. 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:8080 --timeout 120 --log-file /var/log/private_account/gunicorn.log --access-logfile /var/log/private_account/access.log app:app
```

#### 3. 使用Docker

1. 创建Dockerfile：
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8080
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--timeout", "120", "app:app"]
   ```

2. 创建docker-compose.yml：
   ```yaml
   version: '3.8'
   
   services:
     api:
       build: .
       ports:
         - "8080:8080"
       environment:
         - DB_HOST=db
         - DB_PORT=3306
         - DB_USER=root
         - DB_PASSWORD=your_db_password
         - DB_NAME=private_account
       depends_on:
         - db
       restart: always
     
     db:
       image: mysql:5.7
       ports:
         - "3306:3306"
       environment:
         - MYSQL_ROOT_PASSWORD=your_db_password
         - MYSQL_DATABASE=private_account
       volumes:
         - mysql_data:/var/lib/mysql
         - ./sql/create_tables.sql:/docker-entrypoint-initdb.d/01_create_tables.sql
       restart: always
   
   volumes:
     mysql_data:
   ```

3. 构建和运行Docker容器：
   ```bash
   docker-compose up -d
   ```

#### 4. 反向代理配置（Nginx）

为了提高安全性和性能，建议在生产环境中使用Nginx作为反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    # SSL配置
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    
    # 代理配置
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 静态文件（如果有）
    location /static {
        alias /path/to/your/static/files;
        expires 30d;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://localhost:8080/health;
        access_log off;
    }
}
```

### 监控与维护

#### 1. 日志监控

- **应用日志**：定期检查应用日志文件（默认：`logs/app.log`）
- **Web服务器日志**：监控Nginx访问日志和错误日志
- **Gunicorn日志**：监控Gunicorn进程日志

推荐使用ELK Stack或Graylog等工具进行集中式日志管理和分析。

#### 2. 性能监控

- **系统资源监控**：使用Prometheus + Grafana监控服务器CPU、内存、磁盘和网络使用情况
- **应用性能监控**：使用New Relic或APM工具监控应用响应时间、吞吐量和错误率
- **数据库监控**：监控MySQL查询性能、连接数和慢查询日志

#### 3. 健康检查

系统提供健康检查端点，可用于监控服务状态：

**URL**: `/health`
**方法**: `GET`

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "服务正常",
  "data": {
    "status": "ok",
    "timestamp": "2024-01-01T00:00:00",
    "version": "1.0.0"
  }
}
```

#### 4. 定期维护

- **数据库备份**：定期备份MySQL数据库，建议使用自动化工具如mysqldump
- **日志轮转**：配置日志轮转，避免日志文件过大
- **安全更新**：定期更新Python依赖和系统软件包
- **性能优化**：分析慢查询日志，优化数据库索引和查询语句

#### 5. 灾难恢复

- 制定数据库恢复计划，定期测试备份恢复流程
- 考虑使用多可用区部署，提高系统可用性
- 实现自动故障转移机制（如使用MySQL主从复制）

## 更新日志

### 最近更新

1. **日志系统优化**
   - 将所有模块中的print语句替换为统一的LogUtils日志记录
   - 确保在日志器初始化失败时仍能提供基本的错误记录功能

2. **Token验证功能重构**
   - 将token验证功能从各个API模块中提取到独立的AuthUtils工具模块
   - 使用统一的@token_required装饰器实现认证

3. **API接口优化**
   - 确保所有expend和income接口的ID参数通过请求参数传递，不在URL路径中包含参数

4. **测试框架完善**
   - 实现服务层的依赖注入，提高测试可维护性
   - 修复测试用例中的mock路径问题
   - 确保所有测试文件集中存放在test文件夹中

5. **代码质量提升**
   - 遵循PEP 8编码规范
   - 减少代码重复，提高模块独立性
   - 增强错误处理和日志记录

## 贡献指南

欢迎您为个人财务管理系统API项目做出贡献！以下是贡献指南，帮助您顺利参与项目开发。

### 1. 贡献流程

1. **Fork 项目**
   - 点击GitHub项目页面右上角的"Fork"按钮，创建您自己的项目副本

2. **克隆项目**
   ```bash
   git clone https://github.com/your-username/PrivateAccount.git
   cd PrivateAccount
   ```

3. **创建分支**
   - 使用清晰的分支命名，遵循以下格式：
     - 功能开发：`feature/功能名称`（如 `feature/user-authentication`）
     - 错误修复：`fix/错误描述`（如 `fix/login-error-handling`）
     - 性能优化：`perf/优化内容`（如 `perf/database-query-optimization`）
     - 文档更新：`docs/文档内容`（如 `docs/update-api-documentation`）
   
   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **编写代码**
   - 遵循项目的代码规范（见下文）
   - 为新增功能编写单元测试
   - 确保所有现有测试通过

6. **运行测试**
   ```bash
   # 运行所有测试
   python -m pytest
   
   # 运行特定模块测试
   python -m pytest test/api/
   
   # 检查测试覆盖率
   python -m pytest --cov=. --cov-report=html
   ```

7. **提交更改**
   - 编写清晰的提交信息，遵循以下格式：
     ```
     <类型>: <描述>
     
     <详细说明（可选）>
     ```
   - 类型包括：feat（新功能）、fix（错误修复）、docs（文档）、style（格式）、refactor（重构）、test（测试）、chore（构建/工具）
   - 描述要简洁明了，不超过50个字符
   
   示例：
   ```
   feat: 添加用户注册接口
   
   实现了用户注册功能，包括参数验证、密码加密和数据库存储
   ```

8. **推送到分支**
   ```bash
   git push origin feature/AmazingFeature
   ```

9. **开启 Pull Request**
   - 登录GitHub，切换到您的分支
   - 点击"New Pull Request"按钮
   - 填写PR标题和详细描述，说明您的更改内容和目的
   - 等待项目维护者审核您的PR

### 2. 代码规范

#### 2.1 Python编码规范

- 遵循**PEP 8**编码规范
- 使用4个空格缩进，不使用制表符
- 每行不超过80个字符
- 函数和方法之间空2行，类之间空3行
- 类名使用**大驼峰命名法**（如 `UserService`）
- 函数名、方法名和变量名使用**小写加下划线**（如 `get_user_info`）
- 常量使用**全大写加下划线**（如 `MAX_CONNECTIONS`）
- 使用类型注解提高代码可读性

#### 2.2 命名约定

| 元素类型 | 命名风格 | 示例 |
|---------|---------|------|
| 类名 | 大驼峰命名法 | `AccountDAO`, `TokenUtils` |
| 函数/方法名 | 小写加下划线 | `get_account_by_id`, `generate_token` |
| 变量名 | 小写加下划线 | `user_id`, `account_balance` |
| 常量 | 全大写加下划线 | `DB_HOST`, `JWT_SECRET_KEY` |
| 模块名 | 小写加下划线 | `user.py`, `log_utils.py` |
| 包名 | 小写 | `api`, `utils` |

#### 2.3 注释规范

- 为复杂的代码块添加注释，说明其功能和逻辑
- 为公共函数和方法添加文档字符串（docstring），使用Google风格
- 文档字符串应包含：功能描述、参数说明、返回值说明和异常说明

示例：
```python
def get_user_by_id(user_id: int) -> Optional[User]:
    """根据用户ID获取用户信息
    
    Args:
        user_id: 用户ID
    
    Returns:
        User对象，如果用户不存在则返回None
    
    Raises:
        DatabaseError: 数据库操作失败时抛出
    """
    pass
```

#### 2.4 错误处理

- 使用统一的错误码系统
- 捕获并记录所有异常
- 向用户返回友好的错误信息
- 避免使用裸露的except语句

#### 2.5 日志记录

- 使用项目提供的`LogUtils`工具记录日志
- 避免使用print语句
- 根据日志级别记录适当的信息：
  - DEBUG：调试信息，开发时使用
  - INFO：普通信息，记录正常操作
  - WARNING：警告信息，记录潜在问题
  - ERROR：错误信息，记录错误事件
  - CRITICAL：严重错误，记录可能导致系统崩溃的问题

### 3. 代码审查标准

在提交PR前，请确保您的代码符合以下标准：

1. **功能完整性**：实现了所有需求功能
2. **代码质量**：
   - 遵循项目代码规范
   - 代码结构清晰，模块化程度高
   - 避免代码重复
   - 函数和方法职责单一
3. **测试覆盖率**：
   - 为新增功能编写了单元测试
   - 所有测试通过
   - 测试覆盖率不低于80%
4. **文档完善**：
   - 更新了相关文档
   - 为公共API添加了文档字符串
5. **性能考虑**：
   - 代码性能良好，没有明显的性能瓶颈
   - 数据库查询经过优化
6. **安全性**：
   - 没有安全漏洞
   - 敏感数据得到适当保护
   - 输入验证完整

### 4. 沟通与反馈

- 如果您有任何问题或建议，可以通过GitHub Issues与项目维护者沟通
- 对于较大的功能变更，建议先创建Issue讨论，获得确认后再开始编码
- 在PR中清晰描述您的更改，便于维护者审核

### 5. 贡献者行为准则

- 尊重其他贡献者和维护者
- 保持专业和礼貌的沟通
- 接受建设性的反馈
- 关注项目的整体利益

感谢您的贡献，使个人财务管理系统API变得更好！

## 许可证

MIT License

## 作者

个人财务管理系统开发团队

## 联系方式

如有问题或建议，请通过以下方式联系项目维护者：

- **邮箱**：privateaccount-api@example.com
- **GitHub Issues**：https://github.com/example/PrivateAccount/issues
- **GitHub Discussions**：https://github.com/example/PrivateAccount/discussions

> 注意：以上为示例联系方式，请根据实际项目情况修改为真实的联系方式。