#!/bin/bash
# 启动 ProjFlow 项目管理平台全部服务
# 端口分配：后端=8809  前端=3210

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
if ! check_port_conflict 8809 "Backend" || ! check_port_conflict 3210 "Frontend"; then
  echo ""
  echo "Port conflict detected. Stop the conflicting processes and retry."
  exit 1
fi

# --- 1. Backend (port 8809) ---
echo "Starting Backend (8809)..."
cd "$BASE_DIR"
nohup python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8809 </dev/null > /tmp/projflow-backend.log 2>&1 & disown
sleep 2

# --- 2. Frontend (port 3210) ---
echo "Starting Frontend (3210)..."
cd "$BASE_DIR/web"
nohup npx vite --port 3210 --strict-port </dev/null > /tmp/projflow-frontend.log 2>&1 & disown
sleep 3

# --- 验证 ---
echo ""
echo "=== Service Status ==="
echo "Backend   (8809): $(curl -s --max-time 3 http://localhost:8809/api/health | head -c 60)"
echo "Frontend  (3210): $(curl -s --max-time 3 http://localhost:3210 | head -c 40)"
