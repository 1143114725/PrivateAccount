# Flask用户认证API服务

一个基于Flask框架开发的用户认证API服务，提供用户注册和登录功能，使用统一的API响应模型和错误码系统。

## 功能特性

- ✅ 用户注册功能
- ✅ 用户登录功能（支持用户名或手机号登录）
- ✅ JWT Token认证机制
- ✅ 统一的API响应模型
- ✅ 错误码系统（200-成功，201-token过期，400-请求错误，401-未授权等）
- ✅ 完善的日志系统
- ✅ 数据库连接池管理
- ✅ 单元测试和集成测试

## 技术栈

- **框架**: Flask
- **数据库**: MySQL
- **ORM**: 原生SQL（使用自定义数据库连接池）
- **日志**: 自定义日志工具
- **认证**: JWT Token
- **测试**: Python单元测试

## 项目结构

```
PyCharmMiscProject/
├── app.py                 # 项目入口文件
├── api/                   # API路由层
│   └── user.py            # 用户相关路由配置文件
├── config/                # 配置文件
├── dao/                   # 数据访问层
├── db/                    # 数据库连接管理
├── logs/                  # 日志文件目录
├── models/                # 数据模型层
│   ├── base_model.py      # 基础模型类
│   └── user_model.py      # 用户相关模型
├── services/              # 业务逻辑层
│   └── UserService.py     # 用户服务类
├── sql/                   # SQL脚本文件
├── test/                  # 测试代码
│   ├── test_models.py     # 模型测试
│   └── test_user_service.py # 用户服务测试
├── utils/                 # 工具函数
│   └── LogUtils.py        # 日志工具类
├── requirements.txt       # 项目依赖
└── README.md              # 项目文档
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
2. 执行`sql/`目录下的SQL脚本创建用户表
3. 配置数据库连接信息（在`db/`目录下的配置文件）

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

### 2. 账户管理模块

#### 2.1 添加账户接口

**URL**: `/api/account`
**方法**: `POST`
**请求头**:
- `token`: 用户认证令牌
- `userid`: 用户ID

**参数**:
- `account_name` (必须): 账户名称
- `balance` (可选): 账户余额，默认为0

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户添加成功",
  "data": {
    "id": 1,
    "name": "银行卡",
    "balance": 1000,
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
- `new_balance` (必须): 新的账户余额

**返回格式**:
```json
{
  "errorcode": 200,
  "message": "账户余额修改成功",
  "data": {
    "id": 1,
    "name": "银行卡",
    "balance": 2000,
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
      "balance": 1000,
      "create_time": 1766145874849,
      "update_time": 1766145874849,
      "enable": true
    },
    {
      "id": 2,
      "name": "支付宝",
      "balance": 500,
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
    "balance": 1000,
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
- `id` (可选): 消费类型ID，如果不传id则查询所有消费类型

**返回格式**:

查询单个消费类型：
```json
{
  "errorcode": 200,
  "message": "查询消费类型成功",
  "data": {
    "id": 1,
    "name": "餐饮",
    "create_time": 1766145874849,
    "update_time": 1766145874849,
    "enable": true
  }
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

## 错误码说明

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

### 运行模型测试

```bash
python test/test_models.py
```

### 运行用户服务测试

```bash
python test/test_user_service.py
```

## 开发说明

### 模型设计

项目使用统一的基础模型类`BaseModel`，所有API响应模型都继承自该类。

```python
class BaseModel:
    def __init__(self, errorcode: int, message: str = "", data: any = None):
        self.errorcode = errorcode
        self.message = message
        self.data = data
```

### 服务层设计

业务逻辑封装在服务层，遵循单一职责原则，例如`UserService`负责用户相关的业务逻辑。

### 日志系统

使用自定义的日志工具`LogUtils`，支持不同模块的日志记录和配置。

## 安全考虑

- 密码使用加密存储
- 登录接口使用POST方法，避免敏感信息暴露在URL中
- 使用JWT Token进行身份认证
- 实现了Token过期机制

## 许可证

MIT License
## 作者

Flask用户认证API服务开发团队



