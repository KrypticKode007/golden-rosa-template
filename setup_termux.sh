#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "[1/3] Updating Termux packages..."
pkg update -y && pkg install -y python git openssh gh

echo "[2/3] Cloning Golden-Agent core..."
if [ ! -d "Golden-Agent" ]; then
  gh repo clone KrypticKode007/Golden-Agent
fi

echo "[3/3] Linking zero-dependency ROSA MCP bridge into Golden-Agent..."
mkdir -p Golden-Agent/scripts
cp scripts/rosa_mcp_server.py Golden-Agent/scripts/
cp mcp_servers.json Golden-Agent/mcp_servers.json

echo "Setup complete! Configure ROBOT_SSH_HOST in Golden-Agent/mcp_servers.json and launch Golden-Agent."
