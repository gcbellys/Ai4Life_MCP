import OpenAI from 'openai';
import { EventSource } from 'eventsource';
 
const openai = new OpenAI({ apiKey: 'your-api-key' });
 
// MCP工具描述转换器
function convertToOpenAITool(mcpTool) {
return {
    type: "function",
    function: {
      name: `tool.${mcpTool.name}`,
      description: mcpTool.description,
      parameters: mcpTool.parameters
    }
  };
}
 
// 获取MCP工具列表
async functiongetMCPTools() {
  const response = await fetch('http://localhost:3000/mcp/discover', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jsonrpc: "2.0", method: "discover", id: 1 })
  });
  const { result } = await response.json();
return result.tools.map(convertToOpenAITool);
}
 
// 执行MCP调用
async function callMCPTool(method, params) {
  const response = await fetch('http://localhost:3000/mcp/invoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method,
      params,
      id: Math.floor(Math.random() * 1000)
    })
  });
return (await response.json()).result;
}
 
// 主对话流程
async functionmain() {
  // 1. 动态获取工具列表
  const tools = await getMCPTools();
 
  // 2. 发起对话请求
  const chatCompletion = await openai.chat.completions.create({
    model: "gpt-4-turbo",
    messages: [{ role: "user", content: "AAPL当前股价是多少？" }],
    tools
  });
 
  // 3. 处理工具调用
  const toolCall = chatCompletion.choices[0].message.tool_calls?.[0];
if (toolCall) {
    const result = await callMCPTool(
      toolCall.function.name,
      JSON.parse(toolCall.function.arguments)
    );
 
    // 4. 将结果返回给OpenAI
    const finalCompletion = await openai.chat.completions.create({
      model: "gpt-4-turbo",
      messages: [
        { role: "user", content: "AAPL当前股价是多少？" },
        chatCompletion.choices[0].message,
        {
          role: "tool",
          name: toolCall.function.name,
          content: JSON.stringify(result)
        }
      ]
    });
 
    console.log(finalCompletion.choices[0].message.content);
  }
}
 
main();langchain_mcp_adapters