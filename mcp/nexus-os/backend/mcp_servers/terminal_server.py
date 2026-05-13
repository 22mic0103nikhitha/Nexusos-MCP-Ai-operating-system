from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("terminal")

@mcp.tool()
def run_command(command: str):
    """Run a terminal command."""
    # Phase 11: Security Layer - Dangerous Command Detection
    blocked = ["rm -rf", "shutdown", "format", "del /s"]
    if any(x in command for x in blocked):
        return f"Security Blocked: Dangerous command detected: {command}"
        
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30 # Add a timeout to prevent hanging commands
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

if __name__ == "__main__":
    mcp.run()
