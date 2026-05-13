from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("filesystem")

@mcp.tool()
def list_files(path: str):
    return os.listdir(path)

@mcp.tool()
def read_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def write_file(path: str, content: str):
    """Write content to a file at the given path."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"

if __name__ == "__main__":
    mcp.run()
