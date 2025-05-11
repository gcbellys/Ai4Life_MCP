// 导入所需的模块
const { ClientSession, StdioServerParameters, stdioClient } = require('@modelcontextprotocol/sdk'); // MCP 客户端相关模块
const { ChatOpenAI } = require('@langchain/openai'); // LangChain 的 OpenAI 模型
const { createReactAgent } = require('langgraph/prebuilt'); // 创建反应代理
const { loadMcpTools } = require('langchain_mcp_adapters/tools'); // 加载 MCP 工具
const readline = require('readline'); // 命令行输入输出
const fs = require('fs').promises; // 异步文件操作
const path = require('path'); // 路径处理
const dotenv = require('dotenv'); // 环境变量管理

// 加载环境变量
dotenv.config();

// 配置日志记录器，使用控制台输出
const logger = {
  info: console.log, // 信息日志
  error: console.error, // 错误日志
  warn: console.warn // 警告日志
};

// 测试模型连通性
async function testModelConnectivity(model) {
  try {
    logger.info("正在测试模型连通性..."); // 记录测试开始
    // 发送测试消息
    const response = await model.invoke([{ role: "user", content: "你好！" }]);
    logger.info("模型连通性测试成功"); // 记录成功
    console.log("模型连通性测试成功，返回内容：");
    console.log(response); // 输出响应
  } catch (e) {
    logger.error(`模型连通性测试失败: ${e.message}`); // 记录错误
    console.error(`模型连通性测试失败: ${e.message}`); // 输出错误
    process.exit(1); // 退出程序
  }
}

// 记录客户端对话到 call.txt
async function logClientConversation(userInput, aiResponse) {
  try {
    const currentTime = new Date().toLocaleString(); // 获取当前时间
    // 构建日志条目
    const logEntry = `
=== 客户端对话记录 ===
时间: ${currentTime}
用户输入: ${userInput}
AI响应: ${aiResponse}
=====================
`;
    const logFilePath = path.join(__dirname, 'call.txt'); // 日志文件路径
    await fs.writeFile(logFilePath, logEntry, { flag: 'a' }); // 追加写入
  } catch (e) {
    logger.error(`记录客户端对话失败: ${e.message}`); // 记录错误
  }
}

// 主函数，初始化并运行客户端
async function main() {
  try {
    // 初始化 ChatOpenAI 模型
    logger.info("正在初始化ChatOpenAI模型...");
    const model = new ChatOpenAI({
      baseURL: 'https://api.deepseek.com/v1', // Deepseek API 地址
      apiKey: process.env.DEEPSEEK_API_KEY || 'sk-5c9f3347b1714a458fcbe81976bbcd72', // API 密钥
      modelName: 'deepseek-chat' // 模型名称
    });
    logger.info("ChatOpenAI模型初始化完成");

    // 测试模型连通性
    await testModelConnectivity(model);

    // 配置服务器参数，指定运行 MCP_Server.js
    logger.info("正在配置服务器参数...");
    const serverParams = new StdioServerParameters({
      command: 'node',
      args: ['MCP_Server.js'],
    });
    logger.info("服务器参数配置完成");

    // 连接到服务器
    logger.info("正在连接服务器...");
    const { read, write } = await stdioClient(serverParams); // 创建 stdio 客户端
    logger.info("服务器连接成功");

    const session = new ClientSession(read, write); // 创建会话
    await session.initialize(); // 初始化会话
    logger.info("会话初始化完成");

    // 加载 MCP 工具
    logger.info("正在加载MCP工具...");
    const tools = await loadMcpTools(session); // 从服务器加载工具
    logger.info(`已加载 ${tools.length} 个工具`);

    // 打印工具信息
    tools.forEach(tool => {
      logger.info(`工具名称: ${tool.name}`);
      logger.info(`工具描述: ${tool.description}`);
    });

    // 创建反应代理
    const agent = createReactAgent(model, tools); // 结合模型和工具创建代理
    logger.info("反应代理创建完成");

    // 显示欢迎信息和功能提示
    console.log("\n=== 外婆家AI助手 ===");
    console.log("输入 'quit' 或 'exit' 退出程序");
    console.log("可用功能:");
    console.log("1. 点单 - 例如：'我要点一杯咖啡'");
    console.log("2. 呼叫服务员 - 例如：'请叫服务员过来'");
    console.log("3. 其他对话 - 例如：'你好'、'谢谢'");
    console.log("========================\n");

    // 创建命令行接口
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    // 主循环，处理用户输入
    while (true) {
      // 获取用户输入
      const userInput = await new Promise(resolve => rl.question("\n请输入您的问题: ", resolve));

      // 检查是否退出
      if (userInput.toLowerCase() === 'quit' || userInput.toLowerCase() === 'exit') {
        console.log("\n感谢使用，再见！");
        break;
      }

      try {
        logger.info(`正在处理用户输入: ${userInput}`); // 记录用户输入
        // 调用代理处理输入
        const agentResponse = await agent.invoke({ messages: [{ role: "user", content: userInput }] });
        logger.info("收到代理响应"); // 记录响应

        let aiResponse = ""; // 收集响应内容
        // 处理代理返回的消息
        for (const message of agentResponse.messages) {
          if (message.type === 'tool') {
            try {
              const toolContent = JSON.parse(message.content); // 解析工具响应
              const output = toolContent.output || "无输出"; // 获取输出
              console.log("\n" + "=".repeat(50));
              console.log(output);
              console.log("=".repeat(50) + "\n");
              aiResponse += output + "\n"; // 添加到响应
            } catch (e) {
              console.log("\n" + "=".repeat(50));
              console.log(message.content); // 直接输出内容
              console.log("=".repeat(50) + "\n");
              aiResponse += message.content + "\n";
            }
          } else if (message.type === 'ai' && message.content.trim()) {
            console.log("\n" + "-".repeat(50));
            console.log("AI助手:", message.content); // 输出 AI 响应
            console.log("-".repeat(50) + "\n");
            aiResponse += message.content + "\n";
          }
        }

        // 记录对话
        await logClientConversation(userInput, aiResponse);
      } catch (e) {
        logger.error(`处理用户输入时出错: ${e.message}`); // 记录错误
        console.error(`\n发生错误: ${e.message}`); // 输出错误
      }
    }

    rl.close(); // 关闭命令行接口
  } catch (e) {
    logger.error(`程序出错: ${e.message}`); // 记录程序错误
    console.error(`\n程序出错: ${e.message}`);
    process.exit(1); // 退出程序
  }
}

// 运行主函数并捕获错误
main().catch(e => {
  console.error(`\n程序出错: ${e.message}`);
  process.exit(1);
});