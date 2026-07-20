#!/bin/bash
# 启动 ProjFlow 项目管理平台全部服务
# 端口分配：后端=8090  前端=3002

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 检查端口是否被占用，如果是则停止占用进程
check_and_free_port() {
  local port=$1
  local service_name=$2

  if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
    local pid=$(lsof -ti :$port -sTCP:LISTEN | head -1)
    if [ -n "$pid" ]; then
      echo "$service_name ($port) already in use by PID $pid, stopping..."
      kill $pid 2>/dev/null
      sleep 1
      # 如果还没死，强制杀
      if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
        kill -9 $pid 2>/dev/null
        sleep 0.5
      fi
    fi
  fi
}

# --- 1. Backend (port 8090) ---
check_and_free_port 8090 "Backend"
echo "Starting Backend (8090)..."
cd "$BASE_DIR"
nohup python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8090 </dev/null > /tmp/projflow-backend.log 2>&1 & disown
sleep 2

# --- 2. Frontend (port 3002) ---
check_and_free_port 3002 "Frontend"
echo "Starting Frontend (3002)..."
cd "$BASE_DIR/web"
nohup npx vite --port 3002 --strict-port </dev/null > /tmp/projflow-frontend.log 2>&1 & disown
sleep 3

# --- 验证 ---
echo ""
echo "=== Service Status ==="
echo "Backend   (8090): $(curl -s --max-time 3 http://localhost:8090/api/health | head -c 60)"
echo "Frontend  (3002): $(curl -s --max-time 3 http://localhost:3002 | head -c 40)"
