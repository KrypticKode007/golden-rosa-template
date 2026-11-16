# Golden-ROSA Termux Template

Lightweight Termux starter template connecting **KrypticKode007/Golden-Agent** with **NASA-JPL ROSA** via the Model Context Protocol (MCP).

## Quick Start in Termux
1. Run `./setup_termux.sh`
2. Set `"ROBOT_SSH_HOST": "user@robot-ip"` in `Golden-Agent/mcp_servers.json` (or leave blank if running inside Ubuntu `proot-distro` with ROS 2 installed).
3. Start Golden-Agent and prompt: *"Check active ROS 2 nodes"*.
