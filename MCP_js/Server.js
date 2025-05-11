// 导入所需的模块
const { FastMCP } = require('@modelcontextprotocol/sdk'); // MCP 协议的 SDK，用于创建服务器
const fs = require('fs'); // 文件系统模块，用于读写文件
const path = require('path'); // 路径模块，用于处理文件路径
const { promisify } = require('util'); // 用于将回调函数转换为 Promise
const readFileAsync = promisify(fs.readFile); // 异步读取文件
const writeFileAsync = promisify(fs.writeFile); // 异步写入文件

// 配置日志记录器，使用控制台输出日志
const logger = {
  info: console.log, // 信息日志
  error: console.error, // 错误日志
  warn: console.warn // 警告日志
};

// 加载系统提示词，从 restaurant_prompt.txt 文件读取
async function loadPrompt() {
  try {
    const promptPath = path.join(__dirname, 'restaurant_prompt.txt'); // 构建提示词文件路径
    const prompt = await readFileAsync(promptPath, 'utf-8'); // 异步读取文件内容
    return prompt; // 返回提示词内容
  } catch (e) {
    logger.error(`加载提示词文件失败: ${e.message}`); // 记录错误
    return "你是一个餐厅AI助手。"; // 返回默认提示词
  }
}

// 启动 MCP 服务器的主函数
async function startServer() {
  const systemPrompt = await loadPrompt(); // 加载系统提示词
  // 创建 MCP 服务器实例，名称为 'restaurant_assistant'，并传入系统提示词
  const mcp = new FastMCP('restaurant_assistant', { systemPrompt });

  // 定义 'order' 工具，用于处理点单请求
  mcp.tool('order', async (item) => {
    logger.info(`收到点单请求: ${item}`); // 记录点单请求
    try {
      const menuFilePath = path.join(__dirname, 'menu.txt'); // 构建菜单文件路径
      const menuData = await readFileAsync(menuFilePath, 'utf-8'); // 读取菜单文件
      // 解析菜单数据，每行一个 JSON 对象
      const menuItems = menuData.split('\n')
        .filter(line => line.trim()) // 过滤空行
        .map(line => JSON.parse(line.trim())); // 解析为 JSON 对象
      // 创建菜品名称到描述的映射
      const menuMap = new Map(menuItems.map(item => [item.item, item.describe]));

      let outputMessage; // 响应消息
      // 检查点单是否在菜单中
      if (menuMap.has(item)) {
        outputMessage = `【点单成功】\n菜品: ${item}\n描述: ${menuMap.get(item)}`; // 成功点单
      } else {
        outputMessage = "【点单失败】\n抱歉，本店没有此菜品。如有疑问，请联系服务员。"; // 点单失败
        logger.warn(`用户点单 ${item} 不在菜单中`); // 记录警告
      }

      // 构建响应对象
      const response = {
        output: outputMessage,
        item,
        in_menu: menuMap.has(item)
      };

      await logConversation(item, 'order', { item }, response); // 记录对话
      return response; // 返回响应
    } catch (e) {
      logger.error(`处理点单时出错: ${e.message}`); // 记录错误
      // 构建错误响应
      const response = {
        output: "【系统错误】\n抱歉，系统发生错误，请联系服务员。",
        item,
        error: e.message
      };
      await logConversation(item, 'order', { item }, response); // 记录错误对话
      return response; // 返回错误响应
    }
  });

  // 定义 'call' 工具，用于处理呼叫服务员请求
  mcp.tool('call', async (reason) => {
    logger.info(`收到呼叫请求: ${reason}`); // 记录呼叫请求
    let callContent = "call.txt 文件为空或无法读取"; // 默认文件内容
    try {
      const callFilePath = path.join(__dirname, 'call.txt'); // 构建 call.txt 路径
      callContent = await readFileAsync(callFilePath, 'utf-8') || "call.txt 文件为空"; // 读取文件
      logger.info(`\n=== call.txt 内容 ===\n${callContent}\n=====================`); // 记录文件内容
    } catch (e) {
      logger.error(`读取 call.txt 失败: ${e.message}`); // 记录错误
    }

    // 构建响应对象
    const response = {
      output: `好的，已通知服务员，原因: ${reason}\n文件内容:\n${callContent}`,
      reason,
      file_content: callContent
    };

    await logConversation(reason, 'call', { reason }, response); // 记录对话
    return response; // 返回响应
  });

  // 定义 'else' 工具，用于处理其他请求
  mcp.tool('else', async () => {
    const currentTime = new Date().toLocaleString(); // 获取当前时间
    const randomNum = Math.floor(Math.random() * 100) + 1; // 生成随机数
    const videoUrl = " "; // 视频链接，当前为空
    const outputMessage = `【其他对话】\n当前时间: ${currentTime}\n随机数字: ${randomNum}\n详情: ${videoUrl}`; // 响应消息

    // 构建响应对象
    const response = {
      output: outputMessage,
      time: currentTime,
      random_number: randomNum,
      video_url: videoUrl
    };

    await logConversation("其他对话", 'else', {}, response); // 记录对话
    return response; // 返回响应
  });

  // 记录服务器启动信息
  logger.info("启动餐厅AI助手...");
  logger.info("可用工具:");
  logger.info("1. order: 处理点单请求");
  logger.info("2. call: 处理服务员呼叫请求");
  logger.info("3. else: 处理其他请求");
  logger.info("\n系统提示词:");
  logger.info(systemPrompt);
  logger.info("\n助手正在运行，等待用户输入...");

  // 记录文件路径以便调试
  logger.info(`order.txt 路径: ${path.join(__dirname, 'order.txt')}`);
  logger.info(`call.txt 路径: ${path.join(__dirname, 'call.txt')}`);

  // 启动服务器，使用 stdio 传输
  mcp.run({ transport: 'stdio' });
}

// 记录对话到 call.txt
async function logConversation(userInput, toolName, toolParams, response) {
  try {
    const currentTime = new Date().toLocaleString(); // 获取当前时间
    // 构建日志条目
    const logEntry = `
=== 对话记录 ===
时间: ${currentTime}
用户输入: ${userInput}
调用工具: ${toolName}
工具参数: ${JSON.stringify(toolParams)}
系统响应: ${JSON.stringify(response)}
=====================
`;
    const logFilePath = path.join(__dirname, 'call.txt'); // 日志文件路径
    await writeFileAsync(logFilePath, logEntry, { flag: 'a' }); // 追加写入
  } catch (e) {
    logger.error(`记录对话失败: ${e.message}`); // 记录错误
  }
}

// 启动服务器并捕获错误
startServer().catch(e => {
  logger.error(`助手发生错误: ${e.message}`); // 记录启动错误
});