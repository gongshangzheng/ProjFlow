#!/bin/bash
# 启动 ProjFlow 项目管理平台全部服务
# 端口分配：后端=8090  前端=3002

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 检查端口是否被占用，如果是则报告冲突并退出
check_port_conflict() {
  local port=$1
  local service_name=$2

  if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
    local pid=$(lsof -ti :$port -sTCP:LISTEN | head -1)
    local proc_info=$(ps -p $pid -o args= 2>/dev/null || echo "unknown")
    echo "ERROR: $service_name ($port) already occupied by PID $pid"
    echo "  Process: $proc_info"
    echo "  Stop it first: kill $pid"
    return 1
  fi
  return 0
}

# --- 检查端口冲突 ---
if ! check_port_conflict 8090 "Backend" || ! check_port_conflict 3002 "Frontend"; then
  echo ""
  echo "Port conflict detected. Stop the conflicting processes and retry."
  exit 1
fi

# --- 1. Backend (port 8090) ---
echo "Starting Backend (8090)..."
cd "$BASE_DIR"
nohup python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8090 </dev/null > /tmp/projflow-backend.log 2>&1 & disown
sleep 2

# --- 2. Frontend (port 3002) ---
echo "Starting Frontend (3002)..."
cd "$BASE_DIR/web"
nohup npx vite --port 3002 --strict-port </dev/null > /tmp/projflow-frontend.log 2>&1 & disown
sleep 3

# --- 验证 ---
echo ""
echo "=== Service Status ==="
echo "Backend   (8090): $(curl -s --max-time 3 http://localhost:8090/api/health | head -c 60)"
echo "Frontend  (3002): $(curl -s --max-time 3 http://localhost:3002 | head -c 40)"
