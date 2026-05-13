import os
import sys
import json
import asyncio
from openai import AsyncOpenAI
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

# We'll use the async OpenAI client for the loop
client = AsyncOpenAI(
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1"),
    api_key='ollama'
)

def mcp_to_openai_tool(mcp_tool):
    """Convert an MCP tool schema to OpenAI tool schema."""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema
        }
    }

async def process_query(query: str):
    """True Autonomous Agent with Tool Calling Loop"""
    
    # We will connect to both MCP servers
    fs_params = StdioServerParameters(command=sys.executable, args=["mcp_servers/filesystem_server.py"])
    term_params = StdioServerParameters(command=sys.executable, args=["mcp_servers/terminal_server.py"])

    # To avoid complex nested context managers, we handle them sequentially or wrap them
    # For simplicity, we can do it in one big block
    async with stdio_client(fs_params) as (fs_read, fs_write), \
               stdio_client(term_params) as (term_read, term_write):
               
        async with ClientSession(fs_read, fs_write) as fs_session, \
                   ClientSession(term_read, term_write) as term_session:
            
            await fs_session.initialize()
            await term_session.initialize()
            
            fs_tools = await fs_session.list_tools()
            term_tools = await term_session.list_tools()
            
            # Combine tools and create a lookup for routing
            mcp_tools_raw = fs_tools.tools + term_tools.tools
            openai_tools = [mcp_to_openai_tool(t) for t in mcp_tools_raw]
            
            # Identify which session owns which tool
            fs_tool_names = {t.name for t in fs_tools.tools}
            term_tool_names = {t.name for t in term_tools.tools}

            messages = [
                {
                    "role": "system", 
                    "content": (
                        "You are NexusOS, an advanced agentic OS running on Windows. "
                        "CRITICAL INSTRUCTIONS:\n"
                        "1. Use valid Windows paths (e.g., C:\\Users\\pc\\Desktop\\app.py or relative paths like .\\app.py).\n"
                        "2. The user's desktop path is exactly: C:\\Users\\pc\\Desktop\n"
                        "3. When asked to create a file or script, ALWAYS write meaningful, working code in the 'content' argument. Never leave it empty.\n"
                        "4. Always use your tools to fulfill the user's request."
                    )
                },
                {"role": "user", "content": query}
            ]

            # LLM Tool Calling Loop
            max_iterations = 5
            for _ in range(max_iterations):
                try:
                    response = await client.chat.completions.create(
                        model="llama3.1", # llama3.1 supports tools natively
                        messages=messages,
                        tools=openai_tools
                    )
                except Exception as e:
                    if "does not support tools" in str(e):
                        return "Error: The selected Ollama model does not support tool calling. Please run `ollama pull llama3.1` and make sure 'llama3.1' is set as the model in agent.py."
                    raise e
                
                message = response.choices[0].message
                
                # If no tools called, we are done
                if not message.tool_calls:
                    return message.content

                # The LLM wants to call tools!
                messages.append(message) # Add assistant's tool call message
                
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    print(f"[Agent] Calling tool: {func_name} with args {func_args}")
                    
                    # Route to the correct MCP session
                    try:
                        if func_name in fs_tool_names:
                            result = await fs_session.call_tool(func_name, arguments=func_args)
                        elif func_name in term_tool_names:
                            result = await term_session.call_tool(func_name, arguments=func_args)
                        else:
                            raise Exception(f"Unknown tool: {func_name}")
                        
                        # Extract result content
                        tool_result_str = "\n".join(
                            [content.text for content in result.content if content.type == 'text']
                        )
                    except Exception as e:
                        tool_result_str = f"Error: {str(e)}"
                        
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": tool_result_str
                    })
                    
            return "Task completed or max iterations reached. Check console logs for tool activity."
