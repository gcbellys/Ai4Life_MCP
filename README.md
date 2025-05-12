Ai4Life_MCP README
 
简介
 
Ai4Life_MCP 是一款基于人工智能的助手，用于模拟餐厅的点单和服务系统。它通过模型上下文协议（MCP）集成外部工具和服务，并利用 LangChain 和 Deepseek API 进行自然语言处理。项目包含一个与用户交互的客户端（Client.js）和一个处理 MCP 工具的服务器（MCP_Server.js，未提供）。
 
功能
 
1. 点餐功能，例如：“我要点一杯咖啡”。
2. 呼叫服务员，例如：“请叫服务员过来”。
3. 支持通用对话，如问候、感谢等。
4. 将用户交互记录到 call.txt 文件中。
 
前置条件
 
在开始使用前，请确保已安装以下软件：
 
1. Node.js：版本 18.x 或更高。
2. npm：随 Node.js 一同安装。
3. Python：运行 MCP 服务器所需（建议使用 3.8+ 版本）。
4. uv：用于运行服务器的 Python 包管理器（可选，但推荐安装）。
5. Deepseek API 密钥：从 Deepseek 获取。
 
安装步骤
 
1. 克隆仓库：
 
git clone https://github.com/gcbellys/Ai4Life_MCP.git
cd Ai4Life_MCP
 
 
1. 安装 Node.js 依赖：
 
npm install
 
 
1. 安装 uv（可选，用于服务器）：
 
curl -LsSf https://astral.sh/uv/install.sh | sh
 
 
1. 验证 MCP 服务器脚本：
确保项目根目录中存在 MCP_Server.js。如果没有，可能需要单独实现或获取（参考 MCP 文档）。
 
配置说明
 
1. 设置环境变量：
在项目根目录中创建一个 .env 文件，并添加您的 Deepseek API 密钥：
 
DEEPSEEK_API_KEY=your-deepseek-api-key
 
 
注意：将  your-deepseek-api-key  替换为您的实际 API 密钥。请确保该文件的安全性，不要提交到版本控制系统。
2. 验证 MCP 服务器配置：
客户端（Client.js）期望通过 Node.js 运行 MCP_Server.js。确保服务器脚本已正确设置以处理 MCP 工具。Client.js 中的服务器参数示例：
 
const serverParams = new StdioServerParameters({
  command: 'node',
  args: ['MCP_Server.js'],
});
 
 
如果您使用不同的服务器设置（例如基于 Python），请相应地修改 command 和 args。例如，使用 uv：
 
const serverParams = new StdioServerParameters({
  command: 'uv',
  args: ['run', 'python', 'MCP_Server.py'],
});
 
 
1. 可选：配置日志：
默认情况下，对话日志会保存到 call.txt 文件中。如果要更改日志文件的位置，请修改 Client.js 中的 logFilePath：
 
const logFilePath = path.join(__dirname, 'custom_log.txt');
 
 
使用方法
 
1. 启动客户端：
 
node Client.js
 
 
1. 与助手交互：
客户端会显示欢迎消息和可用功能。您可以输入以下命令：
 
- “我要点一杯咖啡” 来点单。
- “请叫服务员过来” 来请求服务。
- “你好” 或 “谢谢” 进行一般对话。
输入  quit  或  exit  退出。
 
1. 检查日志：
对话日志会追加到项目根目录的 call.txt 文件中。每个条目包括时间戳、用户输入和 AI 响应。
 
故障排除
 
1. 错误：“模型连通性测试失败”：
确保 .env 文件中的 Deepseek API 密钥有效，并检查您的网络连接和 Deepseek API 端点（https://api.deepseek.com/v1）。
2. 错误：“无法找到 MCP_Server.js”：
确认项目根目录中存在 MCP_Server.js。如果使用自定义服务器，请更新 Client.js 中的 serverParams 以匹配您的设置。
3. 未加载工具：
确保 MCP 服务器正在运行，并已正确配置以暴露工具。检查服务器日志以查找错误（如果可用）。
4. 常见问题：
再次运行  npm install  以确保所有依赖项已安装。将 Node.js 更新到最新的稳定版本。如果需要帮助，请联系仓库维护者。
 
贡献指南
 
欢迎您为项目做出贡献，步骤如下：
 
1. Fork 该仓库。
2. 创建一个功能分支： git checkout -b feature/your-feature 。
3. 提交您的更改： git commit -m 'Add your feature' 。
4. 推送到分支： git push origin feature/your-feature 。
5. 提交 Pull Request。
 
许可证
 
本项目采用 MIT 许可证。详情请见 LICENSE 文件。
 
联系我们
 
如有问题或疑问，请在 GitHub 上提交 issue 或联系维护者。