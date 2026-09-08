# Módulo 13 (extra): Stages en paralelo y notificaciones (docente)

**Tiempo:** 15 min.

## Conceptos a enseñar

- **`parallel`:** stages que corren al mismo tiempo, cada uno en su executor. Sirve para lint + tests, o tests en varias versiones. El pipeline espera a todos. Con 2 executors, 3 ramas en paralelo hacen cola.
- **`failFast true`:** si una rama falla, cancela las otras.
- **Workspaces separados:** cada rama paralela corre en su propio workspace (`job` y `job@2`). Por eso cada una instala sus dependencias. `stash`/`unstash` sirve para archivos chicos (reportes, binarios); un venv con symlinks rompe el `unstash`. Probado.
- **`agent none` + `input` sin agent:** el patrón para no bloquear un executor mientras alguien aprueba. Se mencionó en el módulo 5; aquí se pone en práctica.
- **Notificaciones:** `post { failure }` + un webhook de Discord (o Slack). El webhook es una URL secreta: va como credencial `Secret text`, y se usa con `withCredentials([string(...)])`. Refuerza el módulo 9 con otro tipo de credencial.
- **`currentBuild`:** objeto con `result`, `durationString`, `displayName`. Útil en mensajes.

## Qué mostrar

1. Pipeline Overview (Graph View) con un `parallel`: se ve la bifurcación. La Stage View clásica no lo muestra bien; por eso se instaló el plugin.
2. Crear un webhook en un servidor de Discord de prueba (Server Settings > Integrations > Webhooks). Cargarlo como Secret text `discord-webhook`.
3. Romper un test, hacer push, y mostrar el mensaje en Discord con link al build. Arreglarlo y mostrar el de éxito.

## Dónde suelen atascarse

- `parallel` dentro de `steps`: no. Va directo dentro de `stage { parallel { stage {} stage {} } }`.
- Un stage con `parallel` no puede tener `steps` propios.
- El JSON del mensaje con comillas dentro de comillas: usar el heredoc como en `alumno.md`.
- Discord devuelve 400 si el `content` está vacío o el JSON está mal.

## Checkpoint

Pipeline con Lint y Test en paralelo visible en Graph View, y un mensaje en Discord por cada build.
