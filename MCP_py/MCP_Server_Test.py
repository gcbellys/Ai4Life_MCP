from mcp.server.fastmcp import FastMCP
import logging
import sys
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 创建 MCP 服务器实例
logger.info("正在初始化 MCP 服务器...")
mcp = FastMCP("math_calculator")
logger.info("MCP 服务器初始化完成")

@mcp.tool("add")
def add(a: int, b: int) -> int:
    """计算两个数的和，适用于需要精确加法运算的场景。示例：输入3和5返回8"""
    logger.info(f"执行加法运算: {a} + {b}")
    result = a + b
    logger.info(f"加法运算结果: {result}")
    return result

@mcp.tool("multiply")
def multiply(a: int, b: int) -> int:
    """计算两个数的乘积，适用于需要精确乘法运算的场景。示例：输入2和5返回10"""
    logger.info(f"执行乘法运算: {a} × {b}")
    result = a * b
    logger.info(f"乘法运算结果: {result}")
    return result

if __name__ == "__main__":
    try:
        logger.info("正在启动 MCP 服务器...")
        logger.info("可用工具:")
        logger.info("1. add: 计算两个整数的和")
        logger.info("2. multiply: 计算两个整数的乘积")
        logger.info("服务器正在运行，等待客户端连接...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("服务器正在关闭...")
    except Exception as e:
        logger.error(f"服务器发生错误: {str(e)}")
    finally:
        logger.info("服务器已关闭")