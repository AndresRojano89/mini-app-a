# Clave Clara

Aplicación web en español para generar contraseñas seguras con FastAPI.

## Requisitos

- Python 3.10 o posterior

## Iniciar la aplicación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre <http://127.0.0.1:8000>. La documentación de la API está disponible en
<http://127.0.0.1:8000/docs>.

La API acepta `POST /api/generate` con un objeto JSON; por ejemplo:

```json
{
  "length": 20,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true,
  "exclude_similar": false
}
```

La longitud permitida es de 8 a 64 caracteres. La generación usa el módulo
criptográfico `secrets` de Python y no almacena las contraseñas.

## Pruebas

```powershell
pytest
```
