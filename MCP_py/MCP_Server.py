from mcp.server.fastmcp import FastMCP
import logging
import sys
import os
import random
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_prompt():
    """加载系统提示词"""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), 'restaurant_prompt.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"加载提示词文件失败: {str(e)}")
        return "你是一个餐厅AI助手。"

# 加载系统提示词
system_prompt = load_prompt()

# 创建 MCP 服务器实例
logger.info("正在初始化外婆家AI助手...")
mcp = FastMCP("restaurant_assistant", system_prompt=system_prompt)
logger.info("外婆家AI助手初始化完成")

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_conversation(user_input: str, tool_name: str, tool_params: dict, response: dict):
    """记录对话到 call.txt"""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n=== 对话记录 ===\n"
        log_entry += f"时间：{current_time}\n"
        log_entry += f"用户输入：{user_input}\n"
        log_entry += f"调用工具：{tool_name}\n"
        log_entry += f"工具参数：{tool_params}\n"
        log_entry += f"系统响应：{response}\n"
        log_entry += "="*20 + "\n"
        
        with open(os.path.join(BASE_DIR, 'call.txt'), 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        logger.error(f"记录对话失败: {str(e)}")

@mcp.tool("order")
def order(item: str) -> str:
    """处理用户点单请求，返回订单确认信息"""
    logger.info(f"收到点单请求: {item}")
    
    # 读取菜单文件
    try:
        menu_file_path = os.path.join(BASE_DIR, 'menu.txt')
        logger.info(f"正在读取菜单文件: {menu_file_path}")
        
        # 读取并解析菜单
        menu_items = {}
        with open(menu_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    menu_item = eval(line.strip())
                    menu_items[menu_item['item']] = menu_item['describe']
                except Exception as e:
                    logger.error(f"解析菜单项失败: {str(e)}")
        
        # 检查点单是否在菜单中
        if item in menu_items:
            output_message = f"【点单yes】\n菜品：{item}\n描述：{menu_items[item]}"
        else:
            output_message = "【点单失败】\n抱歉本店没有这个菜品，若有疑问请联系服务员"
            logger.warning(f"用户点单 {item} 不在菜单中")
        
        response = {
            "output": output_message,
            "item": item,
            "in_menu": item in menu_items
        }
        
        # 记录对话
        log_conversation(item, "order", {"item": item}, response)
        
        return response
        
    except Exception as e:
        logger.error(f"处理点单时发生错误: {str(e)}")
        logger.error(f"当前工作目录: {os.getcwd()}")
        response = {
            "output": "【系统错误】\n抱歉，系统出现错误，请联系服务员",
            "item": item,
            "error": str(e)
        }
        # 记录错误对话
        log_conversation(item, "order", {"item": item}, response)
        return response

@mcp.tool("call")
def call(reason: str) -> dict:
    """处理用户呼叫服务员的请求，返回确认信息和文件内容"""
    logger.info(f"收到呼叫请求: {reason}")
    call_content = "call.txt 文件为空或无法读取"
    try:
        call_file_path = os.path.join(BASE_DIR, 'call.txt')
        logger.info(f"正在读取文件: {call_file_path}")
        with open(call_file_path, 'r', encoding='utf-8') as f:
            call_content = f.read().strip() or "call.txt 文件为空"
            logger.info("\n=== call.txt 内容 ===\n%s\n=====================", call_content)
    except Exception as e:
        logger.error(f"读取 call.txt 失败: {str(e)}")
        logger.error(f"当前工作目录: {os.getcwd()}")
    
    response = {
        "output": f"好的，已通知服务员，原因：{reason}\n文件内容：\n{call_content}",
        "reason": reason,
        "file_content": call_content
    }
    
    # 记录对话
    log_conversation(reason, "call", {"reason": reason}, response)
    
    return response

@mcp.tool("else")
def else_tool() -> str:
    """处理非点单和非呼叫的请求"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_num = random.randint(1, 100)
    #video_url = "https://www.bilibili.com/video/BV1UT42167xb/?spm_id_from=333.337.search-card.all.click&vd_source=4cb6bb76376bc11e046debd6a7ddc6ee"
    video_url = " "
    output_message = f"【其他对话】\n当前时间：{current_time}\n随机数字：{random_num}\n详情见：{video_url}"
    #output_message = f"欢迎光临外婆家\n当前时间：{current_time}\n随机数字：{random_num}\n详情见：{video_url}"
    
    response = {
        "output": output_message,
        "time": current_time,
        "random_number": random_num,
        "video_url": video_url
    }
    
    # 记录对话
    log_conversation("其他对话", "else", {}, response)
    
    return response

if __name__ == "__main__":
    try:
        logger.info("正在启动餐厅AI助手...")
        logger.info("可用工具:")
        logger.info("1. order: 处理点单请求")
        logger.info("2. call: 处理呼叫服务员请求")
        logger.info("3. else: 处理其他请求")
        logger.info("\n系统提示词:")
        logger.info(system_prompt)
        logger.info("\n助手正在运行，等待用户输入...")
        
        # 打印文件路径以便调试
        logger.info(f"order.txt 路径: {os.path.join(BASE_DIR, 'order.txt')}")
        logger.info(f"call.txt 路径: {os.path.join(BASE_DIR, 'call.txt')}")
        
        # 启动服务器
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("助手正在关闭...")
    except Exception as e:
        logger.error(f"助手发生错误: {str(e)}")
    finally:
        logger.info("助手已关闭")