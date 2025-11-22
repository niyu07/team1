#!/bin/bash
set -e

echo "===== Python: Black (自動フォーマット) ====="
docker compose exec backend black /backend/app/ || { echo "Black でのフォーマットに失敗"; exit 1; }

echo "===== Python: autopep8 (追加の自動修正) ====="
docker compose exec backend autopep8 --in-place --recursive --aggressive /backend/app/ || { echo "autopep8 での修正に失敗"; exit 1; }

echo "===== Frontend: ESLint & Prettier 自動修正 ====="
docker compose exec frontend npx eslint "src/**/*.{ts,tsx,js,jsx}" --fix || true
docker compose exec frontend npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,scss,md}" || { echo "Prettier での修正に失敗"; exit 1; }

echo "✅ フォーマット完了"
