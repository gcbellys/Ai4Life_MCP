import asyncio
import sys
import logging
import traceback

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

# 系统提示词（从 restaurant_prompt.txt 复制）
SYSTEM_PROMPT = """你是一个餐厅AI助手。你的任务是：
1. 判断用户输入的意图：'点单'、'呼叫服务员' 或 '其他'。
2. 如果是'点单'，使用 'order' 工具处理点单。
3. 如果是'呼叫服务员'，使用 'call' 工具通知服务员。
4. 如果是'其他'，直接回复。

工具使用说明：
- order 工具：用于处理所有点单请求，包括点菜、点饮品等。参数 item 应该是具体的菜品或饮品名称。
- call 工具：用于处理所有需要服务员帮助的请求。参数 reason 应该是具体的需求原因。

示例对话：
用户：我要点一杯咖啡
助手：好的，我来帮您点单。
[使用 order 工具，参数：{"item": "咖啡"}]

用户：请叫服务员过来
助手：好的，我这就帮您呼叫服务员。
[使用 call 工具，参数：{"reason": "顾客需要帮助"}]

用户：我要点一份茶香鸡
助手：好的，我来帮您点单。
[使用 order 工具，参数：{"item": "茶香鸡"}]

用户：服务员，这里需要加菜
助手：好的，我这就帮您呼叫服务员。
[使用 call 工具，参数：{"reason": "顾客需要加菜"}]

注意事项：
1. 点单时，必须使用 order 工具，并提取具体的菜品或饮品名称作为参数。
2. 呼叫服务员时，必须使用 call 工具，并说明具体原因。
3. 其他对话时，保持礼貌和专业的服务态度。
4. 所有工具调用必须返回 output 字段，包含对用户的回复。"""

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
            model='/root/autodl-tmp/AI4Life-Testing/Share/LLaMA-Factory/Hugging-Face/hub/models--deepseek-ai--DeepSeek-R1-Distill-Qwen-1.5B/snapshots/ad9f0ae0864d7fbcd1cd905e3c6c5b069cc8b562'
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
                    
                    # 创建系统提示词
                    system_prompt = """你是一个餐厅AI助手，可以帮助顾客点单和呼叫服务员。
                    当顾客要点单时，使用 order 工具。
                    当顾客要呼叫服务员时，使用 call 工具。
                    其他情况下，直接回答顾客的问题。"""
                    
                    # 创建代理，不包含 tool_choice 参数
                    agent = create_react_agent(model, tools)
                    logger.info("反应代理创建完成")
                except Exception as e:
                    logger.error(f"加载工具或创建代理时发生错误: {str(e)}")
                    logger.error(f"错误详情: {traceback.format_exc()}")
                    raise
                
                print("\n=== 餐厅AI助手 ===")
                print("输入 'quit' 或 'exit' 退出程序")
                print("可用功能:")
                print("1. 点单 - 例如：'我要点一杯咖啡'")
                print("2. 呼叫服务员 - 例如：'请叫服务员过来'")
                print("3. 其他对话")
                print("========================\n")
     
                while True:
                    # 获取用户输入
                    user_input = input("\n请输入您的问题: ")
                    
                    # 检查是否退出
                    if user_input.lower() in ['quit', 'exit']:
                        print("\n感谢使用，再见！")
                        break
                    
                    try:
                        # 向代理发送消息并获取响应，包含系统提示词
                        logger.info(f"正在处理用户输入: {user_input}")
                        request = {
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_input}
                            ]
                        }
                        logger.info(f"发送的请求: {dumps(request, pretty=True, ensure_ascii=False)}")
                        
                        agent_response = await agent.ainvoke(request)
                        logger.info("收到代理响应")
                        
                        # 先输出完整JSON
                        print("\n完整响应 (JSON):")
                        json_str = dumps(agent_response, pretty=True, ensure_ascii=False)
                        print(json_str)
                        
                        # 获取最后一条消息
                        last_message = agent_response['messages'][-1]
                        
                        # 检查消息类型并提取内容
                        if last_message.type == 'ai':
                            print("\n回答:", last_message.content)
                            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                                logger.info(f"工具调用: {last_message.tool_calls}")
                        elif last_message.type == 'tool':
                            print("\n工具返回:", last_message.content)
                        else:
                            logger.warning("无法识别的消息类型")
                            print("\n抱歉，我无法理解您的问题。")
                        
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