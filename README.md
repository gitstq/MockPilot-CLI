<div align="center">

# 🚀 MockPilot-CLI

**Lightweight Terminal API Mock Server Intelligent Engine**

**轻量级终端API Mock服务器智能引擎**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**MockPilot-CLI** is a lightweight, zero-dependency Python CLI tool that enables rapid API mocking for development and testing. With built-in templates, hot-reload configuration, and request recording capabilities, it's the perfect companion for frontend developers, QA engineers, and API designers.

**Key Problems Solved:**
- 🚫 Backend API not ready? Mock it instantly!
- 🔄 Tired of manually creating mock servers? Use our templates!
- 📝 Need to capture and replay API interactions? We've got you covered!
- 🌐 Cross-origin issues during development? Built-in CORS support!

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🎯 **Zero Dependencies** | Pure Python standard library, no pip install hell |
| 📦 **10+ Built-in Templates** | REST API, Auth, E-commerce, Social Media, Weather, and more |
| ⚡ **Hot Reload** | Auto-reload configuration without restarting server |
| 🎙️ **Request Recording** | Capture and replay API interactions |
| 🌐 **CORS Support** | Built-in cross-origin headers for frontend development |
| ⏱️ **Artificial Delays** | Simulate network latency for realistic testing |
| 🛣️ **Path Parameters** | Dynamic routes like `/users/{id}` |
| 📄 **JSON/YAML Config** | Flexible configuration formats |

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/MockPilot-CLI.git
cd MockPilot-CLI

# Install (optional - can also run directly)
pip install -e .
```

#### Basic Usage

```bash
# Initialize a new configuration
mockpilot init

# Start with default config (mockpilot.json)
mockpilot start

# Start with specific config
mockpilot start -c my-config.json

# Start with a template
mockpilot start -t rest-api

# Start with recording enabled
mockpilot record
```

### 📖 Detailed Usage

#### Available Templates

```bash
# List all templates
mockpilot templates
```

| Template | Description | Routes |
|----------|-------------|--------|
| `rest-api` | Standard RESTful CRUD operations | 5 |
| `auth-api` | Authentication & authorization | 5 |
| `ecommerce` | Online store API | 6 |
| `social-media` | Social platform API | 5 |
| `weather` | Weather data API | 2 |
| `health-check` | Health & status endpoints | 3 |
| `error-simulation` | Error scenario testing | 6 |
| `webhook` | Webhook receiver | 2 |
| `graphql` | GraphQL mock endpoint | 2 |
| `file-upload` | File upload/download | 3 |

#### Configuration Example

```json
{
  "server": {
    "host": "localhost",
    "port": 8080
  },
  "settings": {
    "cors": true,
    "delay": 0.5,
    "recording": false
  },
  "routes": [
    {
      "path": "/api/users",
      "method": "GET",
      "status": 200,
      "response": {
        "users": [
          {"id": 1, "name": "Alice"},
          {"id": 2, "name": "Bob"}
        ]
      }
    },
    {
      "path": "/api/users/{id}",
      "method": "GET",
      "status": 200,
      "response": {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
      }
    }
  ]
}
```

#### Command Options

```bash
# Start with custom host and port
mockpilot start -H 0.0.0.0 -p 3000

# Add artificial delay (seconds)
mockpilot start -d 1.5

# Disable CORS
mockpilot start --no-cors

# Watch config file for changes
mockpilot start -w

# Export recordings
mockpilot export -o my-recordings.json
```

### 💡 Design Philosophy

MockPilot-CLI was designed with these principles:

1. **Simplicity First** - Get a mock server running in seconds, not minutes
2. **Zero Dependencies** - No dependency conflicts or security vulnerabilities
3. **Developer Experience** - Intuitive commands, helpful error messages, hot reload
4. **Production-Ready** - CORS, delay simulation, request recording for realistic testing

### 📦 Deployment

Since MockPilot-CLI is pure Python, deployment is straightforward:

```bash
# Direct execution
python -m mockpilot.cli start

# Or after installation
mockpilot start

# Background execution
nohup mockpilot start > mockpilot.log 2>&1 &
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**MockPilot-CLI** 是一个轻量级、零依赖的 Python CLI 工具，专为快速 API Mock 而设计。内置丰富的模板、热重载配置和请求录制功能，是前端开发者、QA 工程师和 API 设计师的完美助手。

**解决的核心痛点：**
- 🚫 后端 API 还没准备好？立即 Mock！
- 🔄 厌倦了手动创建 Mock 服务器？使用我们的模板！
- 📝 需要捕获和回放 API 交互？我们已为你准备好！
- 🌐 开发中的跨域问题？内置 CORS 支持！

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **零依赖** | 纯 Python 标准库，无需 pip 安装地狱 |
| 📦 **10+ 内置模板** | REST API、认证、电商、社交媒体、天气等 |
| ⚡ **热重载** | 配置变更自动重载，无需重启服务 |
| 🎙️ **请求录制** | 捕获和回放 API 交互 |
| 🌐 **CORS 支持** | 内置跨域头，方便前端开发 |
| ⏱️ **人工延迟** | 模拟网络延迟，进行真实测试 |
| 🛣️ **路径参数** | 动态路由如 `/users/{id}` |
| 📄 **JSON/YAML 配置** | 灵活的配置格式 |

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/MockPilot-CLI.git
cd MockPilot-CLI

# 安装（可选 - 也可以直接运行）
pip install -e .
```

#### 基本用法

```bash
# 初始化配置
mockpilot init

# 使用默认配置启动（mockpilot.json）
mockpilot start

# 使用指定配置启动
mockpilot start -c my-config.json

# 使用模板启动
mockpilot start -t rest-api

# 启用录制模式启动
mockpilot record
```

### 📖 详细使用指南

#### 可用模板

```bash
# 列出所有模板
mockpilot templates
```

| 模板 | 描述 | 路由数 |
|------|------|--------|
| `rest-api` | 标准 RESTful CRUD 操作 | 5 |
| `auth-api` | 认证与授权 | 5 |
| `ecommerce` | 电商 API | 6 |
| `social-media` | 社交平台 API | 5 |
| `weather` | 天气数据 API | 2 |
| `health-check` | 健康检查端点 | 3 |
| `error-simulation` | 错误场景测试 | 6 |
| `webhook` | Webhook 接收器 | 2 |
| `graphql` | GraphQL Mock 端点 | 2 |
| `file-upload` | 文件上传/下载 | 3 |

#### 配置示例

```json
{
  "server": {
    "host": "localhost",
    "port": 8080
  },
  "settings": {
    "cors": true,
    "delay": 0.5,
    "recording": false
  },
  "routes": [
    {
      "path": "/api/users",
      "method": "GET",
      "status": 200,
      "response": {
        "users": [
          {"id": 1, "name": "Alice"},
          {"id": 2, "name": "Bob"}
        ]
      }
    },
    {
      "path": "/api/users/{id}",
      "method": "GET",
      "status": 200,
      "response": {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
      }
    }
  ]
}
```

#### 命令选项

```bash
# 使用自定义主机和端口启动
mockpilot start -H 0.0.0.0 -p 3000

# 添加人工延迟（秒）
mockpilot start -d 1.5

# 禁用 CORS
mockpilot start --no-cors

# 监视配置文件变更
mockpilot start -w

# 导出录制数据
mockpilot export -o my-recordings.json
```

### 💡 设计思路

MockPilot-CLI 遵循以下设计原则：

1. **极简优先** - 秒级启动 Mock 服务器，而非分钟级
2. **零依赖** - 无依赖冲突或安全漏洞
3. **开发者体验** - 直观的命令、友好的错误提示、热重载
4. **生产就绪** - CORS、延迟模拟、请求录制，支持真实测试场景

### 📦 打包与部署

由于 MockPilot-CLI 是纯 Python 实现，部署非常简单：

```bash
# 直接执行
python -m mockpilot.cli start

# 或安装后执行
mockpilot start

# 后台运行
nohup mockpilot start > mockpilot.log 2>&1 &
```

### 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---
<a name="繁體中文"></a>
## 🇹