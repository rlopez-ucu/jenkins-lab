# Antes de la clase (docente)

## Una semana antes

1. Enviar a los alumnos [prework/alumno.md](alumno.md). Insistir: sin la imagen construida, el módulo 0 no entra en el tiempo.
2. Publicar el proyecto de ejemplo como **template repository** en GitHub:

```bash
cd sample-app
git init
git add .
git commit -m "libreria-api: proyecto de ejemplo para la clase de Jenkins"
gh repo create <USUARIO_DOCENTE>/libreria-api --public --source=. --push
gh repo edit <USUARIO_DOCENTE>/libreria-api --template
```

   Sin `gh`: crear el repositorio en la web, hacer push, y en Settings marcar "Template repository".

3. Reemplazar los placeholders `<ORG_O_USUARIO>`, `<REPO_DE_LA_CLASE>` y `<USUARIO_DOCENTE>` en todas las guías:

```bash
grep -rl '<USUARIO_DOCENTE>\|<ORG_O_USUARIO>\|<REPO_DE_LA_CLASE>' . | xargs sed -i 's|<USUARIO_DOCENTE>|tuusuario|g; s|<ORG_O_USUARIO>|tuusuario|g; s|<REPO_DE_LA_CLASE>|devops-ucu|g'
```

4. Hacer la clase entera, de principio a fin, en una máquina limpia (o borrando el volumen `jenkins_home`). Anotar los tiempos.

## El día anterior

- Tener el Jenkins del docente ya levantado y con el wizard hecho, en una pestaña. Desde ahí se demuestra, y se ahorra tiempo si a alguien le falla el setup.
- Tener a mano el token de ngrok, el PAT de GitHub y el token de Docker Hub.
- Verificar que la última versión `jenkins/jenkins:lts-jdk21` no cambió nada de la UI que muestran las guías (los menús de Manage Jenkins cambian de nombre cada tanto).
- Abrir `troubleshooting.md` en una pestaña.

## Antes de arrancar (17:45)

- Pedir que todos abran Docker Desktop (Windows y macOS) ahora. Tarda un minuto en arrancar.
- Pedir que corran `docker images | grep ucu-devops` (Windows: `docker images | Select-String ucu-devops`). Quien no lo tenga, que ejecute `docker compose build` ya mismo, mientras el docente hace la intro.
