# AI4Life - 多语言 MCP 实现项目

本项目是一个基于 Model Context Protocol (MCP) 的多语言实现，包含 Python 和 JavaScript 两个版本的实现。项目主要用于展示和测试 MCP 协议在不同编程语言中的应用。

## 项目结构

```
.
├── MCP_js/                # JavaScript 实现
│   ├── Client.js         # MCP 客户端实现
│   ├── Server.js         # MCP 服务器实现
│   ├── Client_Test.js    # 客户端测试
│   ├── Server_Test.js    # 服务器测试
│   ├── menu.txt         # 菜单数据
│   ├── order.txt        # 订单数据
│   └── restaurant_prompt.txt  # 餐厅提示词
│
└── MCP_py/               # Python 实现
    ├── MCP_Client.py     # MCP 客户端实现
    ├── MCP_Server.py     # MCP 服务器实现
    ├── MCP_Client_2.py   # 客户端替代实现
    ├── MCP_Client_testlocal.py  # 本地测试客户端
    ├── MCP_Server_Test.py  # 服务器测试
    ├── response_test.py  # 响应测试
    └── mcp_explanation.ipynb  # MCP 说明文档
```

## 技术栈

### JavaScript 版本
- Node.js
- @langchain/langgraph
- @langchain/mcp-adapters
- @langchain/openai
- @modelcontextprotocol/sdk
- dotenv

### Python 版本
- Python 3.x
- 相关依赖见 requirements.txt（待添加）

## 快速开始

### JavaScript 版本

1. 进入 MCP_js 目录：
```bash
cd MCP_js
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量：
创建 `.env` 文件并设置必要的环境变量（如 API 密钥等）

4. 运行服务器：
```bash
node Server.js
```

5. 运行客户端：
```bash
node Client.js
```

### Python 版本

1. 进入 MCP_py 目录：
```bash
cd MCP_py
```

2. 安装依赖：
```bash
pip install -r requirements.txt  # 待添加
```

3. 运行服务器：
```bash
python MCP_Server.py
```

4. 运行客户端：
```bash
python MCP_Client.py
```

## 测试

### JavaScript 测试
```bash
node Client_Test.js
node Server_Test.js
```

### Python 测试
```bash
python MCP_Server_Test.py
python response_test.py
```

## 项目说明

本项目实现了 Model Context Protocol (MCP) 的客户端和服务器端，支持：
- 多语言实现（Python 和 JavaScript）
- 客户端-服务器通信
- 本地测试环境
- 完整的测试套件

## 注意事项

1. 运行前请确保已正确配置所有必要的环境变量
2. 建议先运行测试用例确保环境配置正确
3. 服务器和客户端需要分别启动

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

ISC License
