import os
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nasa-rosa-termux-bridge")

# Set ROBOT_SSH_HOST (e.g., "ubuntu@192.168.1.50") to control a remote ROS robot from Termux.
# Leave empty if running directly inside a ROS-enabled Linux/proot environment.
ROBOT_HOST = os.getenv("ROBOT_SSH_HOST", "")
ROS_SETUP = os.getenv("ROS_SETUP_PATH", "/opt/ros/humble/setup.bash")
ROSA_MODEL = os.getenv("ROSA_MODEL", "llama3.1")

def run_rosa_query(instruction: str) -> str:
    py_code = (
        f"import os; from langchain_ollama import ChatOllama; from rosa import ROSA; "
        f"llm = ChatOllama(model='{ROSA_MODEL}', temperature=0); "
        f"agent = ROSA(ros_version=2, llm=llm); "
        f"print(agent.invoke({instruction!r}))"
    )
    cmd = f"source {ROS_SETUP} && python3 -c \"{py_code}\""
    
    if ROBOT_HOST:
        full_cmd = ["ssh", "-o", "BatchMode=yes", ROBOT_HOST, cmd]
    else:
        full_cmd = ["bash", "-c", cmd]

    result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return f"Error executing ROSA: {result.stderr.strip()}"
    return result.stdout.strip()

@mcp.tool()
def control_robot(instruction: str) -> str:
    """
    Send a natural language instruction to inspect or move a ROS 2 robot via NASA-JPL ROSA.
    """
    return run_rosa_query(instruction)

if __name__ == "__main__":
    mcp.run()
