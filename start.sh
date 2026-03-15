#\!/bin/bash
# Inicia la API (puerto 8000) y el frontend (puerto 3000)

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Iniciando API en http://localhost:8000 ..."
cd "$ROOT/02-api-model"
venv/bin/uvicorn api.main:app --reload --port 8000 &
API_PID=$\!

echo "Iniciando frontend en http://localhost:3000 ..."
cd "$ROOT/03-web-model"
python3 -m http.server 3000 &
WEB_PID=$\!

echo ""
echo "API PID:      $API_PID"
echo "Frontend PID: $WEB_PID"
echo ""
echo "Presiona Ctrl+C para detener ambos servidores."

trap "kill $API_PID $WEB_PID 2>/dev/null; echo Servidores detenidos." INT TERM
wait
