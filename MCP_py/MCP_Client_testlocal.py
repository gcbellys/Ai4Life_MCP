import asyncio
import sys
import logging
import traceback
import json
from datetime import datetime

from langchain_core.load import dumps
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def test_model_connectivity(model):
    """测试模型连通性"""
    try:
        logger.info("正在测试模型连通性...")
        response = await model.ainvoke([{"role": "user", "content": "你好！"}])
        logger.info("模型连通性测试成功")
        print("模型连通性测试成功，返回内容：")
        print(response)
    except Exception as e:
        logger.error(f"模型连通性测试失败: {str(e)}")
        print(f"模型连通性测试失败: {str(e)}")
        sys.exit(1)

def log_client_conversation(user_input: str, ai_response: str):
    """记录客户端对话到 call.txt"""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n=== 客户端对话记录 ===\n"
        log_entry += f"时间：{current_time}\n"
        log_entry += f"用户输入：{user_input}\n"
        log_entry += f"AI响应：{ai_response}\n"
        log_entry += "="*20 + "\n"
        
        with open('call.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        logger.error(f"记录客户端对话失败: {str(e)}")

async def main():
    """
    主函数，用于初始化模型、服务器参数，并通过异步会话与服务器进行交互，最终获取并打印代理的响应。
    """
    try:
        # 初始化ChatOpenAI模型，指定基础URL和模型名称
        logger.info("正在初始化ChatOpenAI模型...")
        model = ChatOpenAI(
            base_url='http://localhost:8000/v1',
            api_key='abcd1234',
            model='/root/autodl-tmp/AI4Life-Testing/Share/LLaMA-Factory/Hugging-Face/hub/models--deepseek-ai--DeepSeek-R1-Distill-Qwen-14B/snapshots/1df8507178afcc1bef68cd8c393f61a886323761'
        )
        logger.info("ChatOpenAI模型初始化完成")

        # 测试模型连通性
        await test_model_connectivity(model)
        
        # 配置服务器参数，指定命令和参数
        logger.info("正在配置服务器参数...")
        server_params = StdioServerParameters(
            command="python",
            args=["MCP_Server.py"],
        )
        logger.info("服务器参数配置完成")
     
        # 通过stdio_client与服务器建立连接，并创建会话
        logger.info("正在连接服务器...")
        async with stdio_client(server_params) as (read, write):
            logger.info("服务器连接成功")
            async with ClientSession(read, write) as session:
                # 初始化会话
                logger.info("正在初始化会话...")
                await session.initialize()
                logger.info("会话初始化完成")
                
                # 加载MCP工具并创建反应代理
                logger.info("正在加载MCP工具...")
                try:
                    tools = await load_mcp_tools(session)
                    logger.info(f"已加载 {len(tools)} 个工具")
                    
                    # 打印工具信息
                    for tool in tools:
                        logger.info(f"工具名称: {tool.name}")
                        logger.info(f"工具描述: {tool.description}")
                    
                    agent = create_react_agent(model, tools)
                    logger.info("反应代理创建完成")
                except Exception as e:
                    logger.error(f"加载工具或创建代理时发生错误: {str(e)}")
                    logger.error(f"错误详情: {traceback.format_exc()}")
                    raise
                
                print("\n=== 外婆家AI助手 ===")
                print("输入 'quit' 或 'exit' 退出程序")
                print("可用功能:")
                print("1. 点单 - 例如：'我要点一杯咖啡'")
                print("2. 呼叫服务员 - 例如：'请叫服务员过来'")
                print("3. 其他对话 - 例如：'你好'、'谢谢'等")
                print("========================\n")
     
                while True:
                    # 获取用户输入
                    user_input = input("\n请输入您的问题: ")
                    
                    # 检查是否退出
                    if user_input.lower() in ['quit', 'exit']:
                        print("\n感谢使用，再见！")
                        break
                    
                    try:
                        # 向代理发送消息并获取响应
                        logger.info(f"正在处理用户输入: {user_input}")
                        agent_response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
                        logger.info("收到代理响应")
                        
                        # 输出完整JSON（用于调试）
                        print("\n完整响应 (JSON):")
                        json_str = dumps(agent_response, pretty=True, ensure_ascii=False)
                        print(json_str)
                        
                        # 处理消息
                        ai_response = ""
                        for message in agent_response['messages']:
                            if message.type == 'tool':
                                # 解析工具返回的JSON
                                try:
                                    tool_content = json.loads(message.content)
                                    output = tool_content.get("output", "无输出")
                                    print("\n" + "="*50)
                                    print(output)
                                    print("="*50 + "\n")
                                    ai_response += output + "\n"
                                except json.JSONDecodeError:
                                    print("\n" + "="*50)
                                    print(message.content)
                                    print("="*50 + "\n")
                                    ai_response += message.content + "\n"
                            elif message.type == 'ai':
                                if message.content.strip():  # 只有当内容不为空时才显示
                                    print("\n" + "-"*50)
                                    print("AI助手：", message.content)
                                    print("-"*50 + "\n")
                                    ai_response += message.content + "\n"
                            elif message.type == 'human':
                                # 忽略人类消息，不需要显示
                                continue
                            else:
                                logger.warning(f"无法识别的消息类型: {message.type}")
                        
                        # 记录对话
                        log_client_conversation(user_input, ai_response)
                        
                    except Exception as e:
                        logger.error(f"处理用户输入时发生错误: {str(e)}")
                        logger.error(f"错误详情: {traceback.format_exc()}")
                        print(f"\n发生错误: {str(e)}")
    
    except Exception as e:
        logger.error(f"程序发生错误: {str(e)}")
        logger.error(f"错误详情: {traceback.format_exc()}")
        print(f"\n程序发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")
        print(f"错误详情: {traceback.format_exc()}")
        sys.exit(1)