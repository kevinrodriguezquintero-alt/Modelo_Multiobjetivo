# Configuración del entorno virtual

## 1. Crear el entorno virtual

**Linux / macOS**
```bash
python3 -m venv venv
```

**Windows**
```cmd
python -m venv venv
```

---

## 2. Activar el entorno virtual

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows (CMD)**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
venv\Scripts\Activate.ps1
```

> En PowerShell puede ser necesario permitir la ejecución de scripts:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## 3. Instalar dependencias

Con el entorno activado:

```bash
pip install -r requirements.txt
```

---

## 4. Desactivar el entorno virtual

```bash
deactivate
```
