from flask import Flask, jsonify
from mcp.server.fastmcp import FastMCP
import platform
import psutil
import subprocess
import json

# 创建 Flask 应用
app = Flask(__name__)

# MCP 服务
mcp = FastMCP("host info mcp")

# 工具函数：获取主机信息



@app.route('/mcp', methods=['GET'])
def get_host_info() -> dict:
    """获取主机信息并返回字典"""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": str(round(psutil.virtual_memory().total / (1024**3), 2)),
    }

    cpu_count = psutil.cpu_count(logical=True)
    if cpu_count is None:
        info["cpu_count"] = "-1"
    else:
        info["cpu_count"] = str(cpu_count)
    
    try:
        cpu_model = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        ).decode().strip()
        info["cpu_model"] = cpu_model
    except Exception:
        info["cpu_model"] = "Unknown"

    return info  # 返回字典而不是 JSON 字符串

# 注册工具函数
mcp.add_tool(get_host_info)

def main():
    """启动 Flask 服务器"""
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
