import sys
import json
import os
import subprocess

ROBOT_HOST = os.getenv("ROBOT_SSH_HOST", "")
ROS_SETUP = os.getenv("ROS_SETUP_PATH", "/opt/ros/humble/setup.bash")
ROSA_MODEL = os.getenv("ROSA_MODEL", "llama3.1")

def run_rosa_query(instruction: str) -> str:
    py_code = (
        f"from langchain_ollama import ChatOllama; from rosa import ROSA; "
        f"llm = ChatOllama(model='{ROSA_MODEL}', temperature=0); "
        f"agent = ROSA(ros_version=2, llm=llm); "
        f"print(agent.invoke({instruction!r}))"
    )
    cmd = f"source {ROS_SETUP} && python3 -c \"{py_code}\""
    full_cmd = ["ssh", "-o", "BatchMode=yes", ROBOT_HOST, cmd] if ROBOT_HOST else ["bash", "-c", cmd]

    result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return f"Error executing ROSA: {result.stderr.strip()}"
    return result.stdout.strip()

def send_response(msg_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            send_response(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "nasa-rosa-termux-bridge", "version": "1.0.0"}
            })
        elif method == "tools/list":
            send_response(msg_id, {
                "tools": [{
                    "name": "control_robot",
                    "description": "Send a plain English command to inspect or move a ROS 2 robot via NASA-JPL ROSA.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "instruction": {"type": "string", "description": "Plain English robot command"}
                        },
                        "required": ["instruction"]
                    }
                }]
            })
        elif method == "tools/call":
            args = req.get("params", {}).get("arguments", {})
            output = run_rosa_query(args.get("instruction", ""))
            send_response(msg_id, {"content": [{"type": "text", "text": output}]})

if __name__ == "__main__":
    main()
