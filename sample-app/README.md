# libreria-api

API mínima de libros hecha con Flask. Es el proyecto de ejemplo de la clase de Jenkins.

## Correr local

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Probar:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/books -H "Content-Type: application/json" -d '{"title":"Dune"}'
curl http://localhost:5000/books
```

## Tests y lint

```bash
pytest
ruff check .
```

## Docker

```bash
docker build -t libreria-api .
docker run --rm -p 5000:5000 libreria-api
```

## Jenkins

El archivo `Jenkinsfile` define el pipeline. Empieza con un solo stage y crece
durante la clase.
