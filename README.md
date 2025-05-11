Ai4Life_MCP
English | 中文
Overview
Ai4Life_MCP is an AI-powered assistant designed to simulate a restaurant ordering and service system. It leverages the Model Context Protocol (MCP) to integrate with external tools and services, using LangChain and Deepseek APIs for natural language processing. The project includes a client (Client.js) that interacts with users and a server (MCP_Server.js, not provided) for handling MCP tools.
Features:

Order food and beverages (e.g., "I want to order a coffee").
Call a waiter (e.g., "Please call the waiter").
General conversation support (e.g., greetings, thanks).
Logs user interactions to call.txt.


概述
Ai4Life_MCP 是一个人工智能助手，旨在模拟餐厅点单和服务系统。它利用模型上下文协议（MCP）与外部工具和服务集成，使用 LangChain 和 Deepseek API 进行自然语言处理。该项目包括一个与用户交互的客户端（Client.js）和一个处理 MCP 工具的服务器（MCP_Server.js，未提供）。
功能：

点餐（例如：“我要点一杯咖啡”）。
呼叫服务员（例如：“请叫服务员过来”）。
支持通用对话（例如：问候、感谢）。
将用户交互记录到 call.txt 文件。


Prerequisites 前置条件
Before you begin, ensure you have the following installed:

Node.js: Version 18.x or higher.
npm: Comes with Node.js.
Python: Required for MCP server (version 3.8+ recommended).
uv: Python package manager for running the server (optional but recommended).
Deepseek API Key: Obtain from Deepseek.

在开始之前，请确保已安装以下内容：

Node.js：版本 18.x 或更高。
npm：随 Node.js 一起安装。
Python：MCP 服务器需要（建议使用 3.8+ 版本）。
uv：用于运行服务器的 Python 包管理器（可选但推荐）。
Deepseek API 密钥：从 Deepseek 获取。


Installation 安装

Clone the Repository 克隆仓库
git clone https://github.com/gcbellys/Ai4Life_MCP.git
cd Ai4Life_MCP


Install Node.js Dependencies 安装 Node.js 依赖
npm install


Install uv (Optional, for Server) 安装 uv（可选，用于服务器）
curl -LsSf https://astral.sh/uv/install.sh | sh


Verify MCP Server Script 验证 MCP 服务器脚本Ensure MCP_Server.js exists in the project root. If not, you may need to implement or obtain it separately (refer to MCP Documentation).
确保项目根目录中存在 MCP_Server.js。如果没有，您可能需要单独实现或获取（参考 MCP 文档）。



Configuration 配置
1. Set Up Environment Variables 配置环境变量
Create a .env file in the project root and add your Deepseek API key:
在项目根目录中创建 .env 文件，并添加您的 Deepseek API 密钥：
DEEPSEEK_API_KEY=your-deepseek-api-key

Example 示例:
DEEPSEEK_API_KEY= Your-API


Note: Replace your-deepseek-api-key with your actual API key. Keep this file secure and do not commit it to version control.


注意：将 your-deepseek-api-key 替换为您的实际 API 密钥。确保此文件安全，不要提交到版本控制。

2. Verify MCP Server Configuration 验证 MCP 服务器配置
The client (Client.js) expects MCP_Server.js to be runnable via Node.js. Ensure the server script is correctly set up to handle MCP tools. Example server parameters in Client.js:
客户端（Client.js）期望通过 Node.js 运行 MCP_Server.js。确保服务器脚本正确配置以处理 MCP 工具。Client.js 中的服务器参数示例：
const serverParams = new StdioServerParameters({
  command: 'node',
  args: ['MCP_Server.js'],
});

If you use a different server setup (e.g., Python-based), modify the command and args accordingly. For example, with uv:
如果您使用不同的服务器设置（例如基于 Python），请相应修改 command 和 args。例如，使用 uv：
const serverParams = new StdioServerParameters({
  command: 'uv',
  args: ['run', 'python', 'MCP_Server.py'],
});

3. Optional: Configure Logging 可选：配置日志
By default, conversation logs are saved to call.txt. To change the log file location, modify the logFilePath in Client.js:
默认情况下，对话日志保存到 call.txt。要更改日志文件位置，请修改 Client.js 中的 logFilePath：
const logFilePath = path.join(__dirname, 'custom_log.txt');


Usage 使用

Start the Client 启动客户端
node Client.js


Interact with the Assistant 与助手交互

The client displays a welcome message with available functions.
Input commands like:
"I want to order a coffee" to place an order.
"Please call the waiter" to request service.
"Hello" or "Thanks" for general conversation.


Type quit or exit to exit.

客户端会显示欢迎消息和可用功能。输入命令，例如：

“我要点一杯咖啡”来点单。
“请叫服务员过来”来请求服务。
“你好”或“谢谢”进行一般对话。
输入 quit 或 exit 退出。


Check Logs 检查日志Conversation logs are appended to call.txt in the project root. Each entry includes the timestamp, user input, and AI response.
对话日志会追加到项目根目录的 call.txt 中。每个条目包括时间戳、用户输入和 AI 响应。


Example Output 示例输出:
=== 客户端对话记录 ===
时间: 2025-05-11 12:00:00
用户输入: 我要点一杯咖啡
AI响应: 已为您记录订单：一杯咖啡。请稍候！
=====================


Troubleshooting 故障排除

Error: "模型连通性测试失败"

Ensure your Deepseek API key is valid and correctly set in .env.
Check your internet connection and the Deepseek API endpoint (https://api.deepseek.com/v1).


Error: "无法找到 MCP_Server.js"

Verify that MCP_Server.js exists in the project root.
If using a custom server, update the serverParams in Client.js to match your setup.


No Tools Loaded 未加载工具

Ensure the MCP server is running and properly configured to expose tools.
Check server logs for errors (if available).


General Issues 常见问题

Run npm install again to ensure all dependencies are installed.
Update Node.js to the latest stable version.
Contact the repository maintainers for support.


错误：“模型连通性测试失败”

确保 .env 中的 Deepseek API 密钥有效。
检查网络连接和 Deepseek API 端点（https://api.deepseek.com/v1）。


错误：“无法找到 MCP_Server.js”

确认项目根目录中存在 MCP_Server.js。
如果使用自定义服务器，请更新 Client.js 中的 serverParams 以匹配您的设置。


未加载工具

确保 MCP 服务器正在运行并正确配置以暴露工具。
检查服务器日志以查找错误（如果可用）。


常见问题

再次运行 npm install 以确保所有依赖项已安装。
将 Node.js 更新到最新的稳定版本。
联系仓库维护者寻求支持。




Contributing 贡献
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

欢迎贡献！贡献步骤：

叉取仓库。
创建功能分支（git checkout -b feature/your-feature）。
提交更改（git commit -m 'Add your feature'）。
推送分支（git push origin feature/your-feature）。
提交 Pull Request。


License 许可
This project is licensed under the MIT License. See the LICENSE file for details.
本项目采用 MIT 许可证。详情请见 LICENSE 文件。

Contact 联系
For issues or questions, open an issue on GitHub or contact the maintainers.
如有问题或疑问，请在 GitHub 上提交 issue 或联系维护者。
