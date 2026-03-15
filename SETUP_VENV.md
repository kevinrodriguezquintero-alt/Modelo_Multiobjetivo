# Configuración del entorno virtual

## 0. Requisitos previos

### Python 3.10 o superior

**Linux / macOS**
```bash
python3 --version
```
Si no está instalado:
- **Ubuntu/Debian:** `sudo apt install python3 python3-venv python3-pip`
- **macOS:** `brew install python3` (requiere [Homebrew](https://brew.sh))

**Windows**
Descargar e instalar desde [python.org](https://www.python.org/downloads/).
Durante la instalación marcar **"Add Python to PATH"**.
```cmd
python --version
```

### Solver HiGHS (recomendado)

HiGHS se instala automáticamente como dependencia de Python vía `pip` (`highspy`), no requiere instalación separada.

Si se usa **GLPK** en lugar de HiGHS:
- **Ubuntu/Debian:** `sudo apt install glpk-utils`
- **macOS:** `brew install glpk`
- **Windows:** descargar desde [winglpk.sourceforge.net](https://winglpk.sourceforge.net)

---

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
