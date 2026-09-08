# Módulo 10 (extra): Agentes Docker por stage (docente)

**Tiempo:** 15 min. Requiere el plugin Docker Pipeline (módulo 8).

## Conceptos a enseñar

- **El problema:** hoy Python está instalado en la imagen de Jenkins porque se agregó a mano. Un equipo con Java, Node y Go necesitaría todo en el controller. No escala.
- **`agent { docker { image '...' } }`:** Jenkins levanta un contenedor de esa imagen, monta el workspace adentro y corre los `steps` ahí. Al terminar lo borra. Cada stage puede usar una imagen distinta. El controller solo necesita Docker.
- **Docker outside of Docker, otra vez:** Jenkins corre en un contenedor y pide al daemon de la máquina local que levante otro contenedor con el workspace montado. Pero la ruta del workspace existe dentro del contenedor de Jenkins, no en la máquina local. El plugin detecta esto y usa `--volumes-from` para compartir el volumen. Cuando la detección falla, se fuerza con `args '--volumes-from jenkins'`. Se indica de forma explícita para que funcione en todas las máquinas.
- **`reuseNode true`:** hace que el contenedor use el mismo workspace del stage anterior en vez de uno nuevo. Necesario para que el `.venv` o los reportes pasen de un stage a otro.
- **`agent none` arriba + agent por stage:** el patrón para pipelines que mezclan imágenes.

## Qué mostrar

1. Cambiar el Jenkinsfile a la versión de este módulo: `agent none` arriba, los stages de Python con `agent { docker { image 'python:3.12-slim' } }`, los de Docker con `agent any`.
2. Hacer push. En el log, mostrar `docker pull python:3.12-slim`, el `docker run` largo que arma el plugin (con `--volumes-from`), y que `python3 --version` indica 3.12 en vez de 3.13 (la del controller).
3. Cambiar a `python:3.11-slim`. Hacer push. Ahora es 3.11. "Cambiar de versión de Python es cambiar una línea".

## Dónde suelen atascarse

- `pip install` falla con permisos: la imagen `python:*-slim` corre como root, no debería. Si pasa, `args '-u root'`.
- El workspace aparece vacío dentro del contenedor: falta `--volumes-from jenkins`. Es el error clásico de este setup.
- Tarda mucho la primera vez: es el `docker pull`. Las siguientes usan caché.
- `reports/junit.xml` no se encuentra en el `post`: el `post` corre en el controller, y sin `reuseNode` el workspace del stage era otro.

## Checkpoint

El stage Test corre dentro de `python:3.12-slim` y el número de versión en el log lo demuestra.
