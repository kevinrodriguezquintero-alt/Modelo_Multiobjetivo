# Cómo levantar el frontend

## 1. Levantar la API (puerto 8000)

```bash
cd ../02-api-model
venv/bin/uvicorn api.main:app --reload --port 8000
```

## 2. Levantar el servidor estático (puerto 3000)

```bash
cd 03-web-model
python3 -m http.server 3000
```

Luego abrir: **http://localhost:3000**

---

> Ambos procesos deben estar corriendo al mismo tiempo.
> El frontend llama a `http://localhost:8000` — asegurarse de que la API esté activa antes de ejecutar LGP o ER.
