#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "[1/4] Updating Termux packages..."
pkg update -y && pkg install -y python git openssh

echo "[2/4] Installing MCP Python SDK..."
pip install --upgrade pip mcp

echo "[3/4] Cloning Golden-Agent core..."
if [ ! -d "Golden-Agent" ]; then
  git clone https://github.com
fi

echo "[4/4] Linking ROSA MCP bridge into Golden-Agent..."
mkdir -p Golden-Agent/scripts
cp scripts/rosa_mcp_server.py Golden-Agent/scripts/
cp mcp_servers.json Golden-Agent/mcp_servers.json

echo "Setup complete! Configure ROBOT_SSH_HOST in Golden-Agent/mcp_servers.json and run Golden-Agent."
