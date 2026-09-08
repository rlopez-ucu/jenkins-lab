# Módulo 4: Repo propio en GitHub y pipeline desde SCM (docente)

**Tiempo:** 15 min. **Hora:** 19:25 a 19:40.

## Conceptos a enseñar

- **Pipeline as code, en serio:** el Jenkinsfile vive en el repo, junto al código. Se versiona, se revisa en PR, viaja con el proyecto. Si mañana se levanta otro Jenkins, se apunta al repo y listo.
- **"Pipeline script from SCM":** Jenkins clona el repo, busca el Jenkinsfile en la ruta indicada y lo ejecuta. Cada build clona de nuevo (o hace fetch), así que siempre corre la versión del Jenkinsfile que está en la rama.
- **Template repository de GitHub:** cada alumno crea SU repo a partir del template. Lo necesitan propio porque en el módulo 6 van a abrir PRs y en el 7 van a configurar webhooks; eso requiere ser admin del repo.
- **Un pipeline real:** venv, instalar dependencias, lint, tests con reporte JUnit. Es el esqueleto de cualquier pipeline de Python. En otros lenguajes cambian los comandos, no la estructura.
- **JUnit:** Jenkins entiende ese formato XML. Con el step `junit` aparece la pestaña **Test Result** con tests pasados, fallados, tendencia entre builds. Es la diferencia entre "falló" y "falló `test_add_book`, y es la tercera vez esta semana".

## Antes del módulo

El template `libreria-api` del docente tiene que estar publicado (ver `prework/docente.md`). Compartir el link en el chat de la clase.

## Qué mostrar

1. El docente crea su repo desde el template en vivo. Mostrar que queda en la cuenta del docente, con historia propia.
2. Clonarlo, abrir el Jenkinsfile, mostrar el de "Hola". Reemplazarlo por la versión de este módulo. Explicar cada stage en 30 segundos. Commit, push.
3. Crear el job Pipeline con **Pipeline script from SCM**. Mostrar los campos: SCM Git, Repository URL, Branch `*/main`, Script Path `Jenkinsfile`. Sin credenciales porque el repo es público.
4. Correr. Mostrar en el console output el `git clone` inicial, la instalación de dependencias, `ruff`, `pytest`. Y la pestaña **Test Result** con 5 tests.
5. Romper un test en vivo (cambiar un `assert`), push, build. Mostrar el test rojo con nombre y traceback en la UI. Arreglarlo y hacer push de nuevo.

## Sobre Windows y finales de línea

El repo trae `.gitattributes` con `eol=lf`. Sin eso, un alumno en Windows con `autocrlf=true` sube scripts con `\r\n` que en Linux fallan con errores raros (`$'\r': command not found`). Mencionarlo cuando aparezca o si alguien pregunta por qué está ese archivo.

## Dónde suelen atascarse

- Los alumnos ponen la URL del template en vez de la de su repo. El build corre igual pero después no pueden hacer push. Pedirles que verifiquen que la URL tiene su usuario.
- `git push` pide usuario y contraseña, y la contraseña no funciona: GitHub no acepta contraseñas desde 2021. Necesitan un PAT (se crea en el módulo 6) o GitHub CLI. Solución rápida en ese momento: `gh auth login`, o crear el PAT de inmediato con scope `repo`. Windows suele abrir un login de navegador (Git Credential Manager) y funciona solo.
- `pip install` lento o falla por red: el contenedor de Jenkins sale a Internet por Docker. Si la red del aula bloquea, probar con hotspot.
- Windows: editan con Notepad y guardan como `Jenkinsfile.txt`. Pedirles que usen VS Code o `notepad Jenkinsfile` desde PowerShell.

## Checkpoint (19:40)

Cada alumno tiene: un repo propio `libreria-api` en su GitHub, un job `04-libreria-scm` verde que corre lint y 5 tests, y la pestaña Test Result muestra esos tests.
