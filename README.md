# AITASystem后端

## 项目概述

```
本项目是一个基于 Flask 的后端服务，为应用提供 RESTful API 接口。
```
## 技术栈

```
- 框架: Flask
- 数据库: MySQL
- 容器化: Docker
```


## 环境配置

### 环境依赖
```
- Python 3.9.21
- Pip 25.1
```

### 安装步骤

1. **克隆项目**  
```
git clone https://github.com/mosyman/aitabackend.git  
cd aitabackend  
```
2. **安装依赖（在根目录的file目录下执行命令）**  
```
cd file  
pip install -r requirements.txt  
```
3. **配置环境变量**

在项目根目录下创建 `.env` 文件，并填入以下内容：  
```
session的密钥  
SECRET_KEY=你的密钥

# 数据库配置（示例为 MySQL，根据实际数据库类型修改）
DB_URL=数据库类型+驱动程序名：//数据库用户名:密码@主机地址:端口号/连接的数据库名

```
4. **初始化数据库**
```
执行 /file/sql/create.sql脚本
```

## 部署
```
暂时未部署上线
```
## 许可证

本项目采用 MIT 许可证，详情见 LICENSE 文件。
    