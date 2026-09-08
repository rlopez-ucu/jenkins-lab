# Módulo 1: La UI y el primer job freestyle (docente)

**Tiempo:** 15 min. **Hora:** 18:30 a 18:45.

## Conceptos a enseñar

- **Job freestyle:** el tipo de job original de Jenkins. Se configura entero con formularios en la UI. Sirve para entender los bloques: SCM (de dónde se saca el código), triggers (cuándo se corre), build steps (qué se hace), post-build actions (qué se hace con el resultado).
- **Build:** una ejecución. Tiene número, estado (azul/verde, rojo, gris, amarillo), duración, y un **console output**. El console output es la primera herramienta de debug de Jenkins.
- **Workspace:** la carpeta del disco donde corre el build. Un job tiene un workspace; los builds lo reutilizan (por eso "Wipe out workspace" existe).
- **Artefacto:** un archivo que el build produce y que Jenkins guarda asociado al build, aunque el workspace se pise después.
- **Lo que le falta al freestyle** (y por eso existe Pipeline, módulo 3): la config vive en la base de datos de Jenkins, no en el repo. No se versiona, no se revisa en PR, no se copia fácil.

## Qué mostrar

Recorrer la UI en el proyector antes de que los alumnos toquen nada (3 min):

- Barra izquierda: New Item, Build History, Manage Jenkins.
- Manage Jenkins: mostrar System, Plugins, Nodes, Credentials sin entrar. "Volvemos a cada uno".
- Build Queue y Build Executor Status abajo a la izquierda. Explicar executor: "cuántos builds a la vez". El controller trae 2.

Después, el docente crea el job en vivo, con los alumnos siguiendo `alumno.md`. Al correr el
build por primera vez, abrir el console output y leerlo línea por línea: qué
usuario lo lanzó, en qué workspace corre, cada comando y su salida, y el `Finished: SUCCESS`.

## Momentos clave

- Cuando `python3 --version` y `docker version` responden dentro del build: "esto no es su computadora, es el contenedor de Jenkins. Tiene lo que le pusimos en el Dockerfile". Vincular con la clase de Docker.
- Al archivar `build-info.txt`: mostrar que el artefacto queda en la página del build y que el workspace se puede borrar sin perderlo.
- Romper algo a propósito: agregar `exit 1` al final del shell y correrlo. Build rojo. "Un comando que devuelve distinto de 0 falla el build. Eso es todo el secreto de CI".

## Dónde suelen atascarse

- "Execute shell" no aparece: están en la sección equivocada. Está en **Build Steps > Add build step**.
- Ven `sh: python3: not found`: su imagen es vieja (construida antes de que se agregara Python). `docker compose build && docker compose up -d`.
- Windows: el navegador a veces bloquea el popup del console output. No es popup, es una página; que hagan clic en el número del build y después en Console Output.

## Checkpoint (18:45)

Cada alumno tiene un job `01-hola-freestyle` con dos builds: uno verde y uno rojo, y un artefacto descargable en el verde.
