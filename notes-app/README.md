# notes-app

API de notas en Flask, con tests unitarios y un Jenkinsfile que los ejecuta y
construye la imagen Docker.

## Estructura

- `notes.py`: la lógica (`NoteStore`), sin dependencias.
- `app.py`: la API HTTP.
- `tests/test_notes.py`: tests unitarios de `NoteStore`.
- `tests/test_api.py`: tests de la API con el cliente de pruebas de Flask.
- `Jenkinsfile`: instala dependencias, corre pytest, construye la imagen.

## Ejecución local

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
python app.py
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado y versión |
| GET | `/notes` | Lista de notas. Con `?q=texto` busca en título y cuerpo |
| POST | `/notes` | Crea una nota. JSON: `{"title": "...", "body": "..."}` |
| GET | `/notes/<id>` | Una nota |
| DELETE | `/notes/<id>` | Borra una nota |

## Docker

```bash
docker build -t notes-app .
docker run --rm -p 5000:5000 notes-app
curl -X POST http://localhost:5000/notes -H "Content-Type: application/json" -d '{"title":"Hola"}'
curl http://localhost:5000/notes
```

## Jenkins

Crear un job de tipo Pipeline con **Pipeline script from SCM** apuntando a este
repo y Script Path `notes-app/Jenkinsfile`.
