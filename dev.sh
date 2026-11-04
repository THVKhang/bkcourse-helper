#!/usr/bin/env bash
# BKCourse Helper — Dev Launcher (macOS/Linux)
# Chạy cả Backend (FastAPI) + Frontend (Next.js) bằng 1 lệnh: ./dev.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

PY="python3"
[ -x "$ROOT/backend/venv/bin/python" ] && PY="$ROOT/backend/venv/bin/python"

echo "🎓 BKCourse Helper — Starting..."
(cd "$ROOT/backend" && "$PY" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload) &
BACKEND_PID=$!
(cd "$ROOT/frontend" && npm run dev) &
FRONTEND_PID=$!

trap 'kill $BACKEND_PID $FRONTEND_PID 2>/dev/null' INT TERM EXIT
echo "🌐 Mở http://localhost:3000 — nhấn Ctrl+C để dừng."
wait
