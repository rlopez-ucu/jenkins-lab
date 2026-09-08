# Clase de Jenkins: de cero a CI/CD

Material para una sesión de 3 horas (18:00 a 21:00). Cada módulo tiene dos guías:

- `docente.md`: qué conceptos se enseñan, qué mostrar, dónde suelen atascarse los alumnos, y cómo verificar que todos llegaron.
- `alumno.md`: pasos a seguir, con comandos para Linux/macOS y para Windows (PowerShell).

Jenkins corre en Docker en la máquina de cada alumno. Por eso los pasos de un
pipeline (`sh`) son siempre Linux, sin importar el sistema operativo del alumno.
Las diferencias entre sistemas aparecen solo en los comandos que se corren en la
terminal del host, y las guías las muestran una al lado de la otra.

## Antes de la clase

Los alumnos deben completar [prework/alumno.md](prework/alumno.md). Lleva 20 a 30
minutos y descarga varios GB. Sin esto, el módulo 0 no entra en 20 minutos.

## Cronograma

| Hora | Módulo | Carpeta | Min |
|------|--------|---------|-----|
| 18:00 | Intro: qué es CI, qué es Jenkins, agenda | [00-setup](00-setup/docente.md) | 10 |
| 18:10 | 0. Levantar Jenkins y completar el wizard | [00-setup](00-setup/alumno.md) | 20 |
| 18:30 | 1. Recorrida por la UI y primer job freestyle | [01-freestyle](01-freestyle/alumno.md) | 15 |
| 18:45 | 2. Job freestyle con parámetros | [02-freestyle-parametros](02-freestyle-parametros/alumno.md) | 10 |
| 18:55 | 3. Pipeline declarativo escrito en la UI | [03-pipeline](03-pipeline/alumno.md) | 20 |
| 19:15 | Pausa | | 10 |
| 19:25 | 4. Repo propio en GitHub y pipeline desde SCM | [04-pipeline-scm](04-pipeline-scm/alumno.md) | 15 |
| 19:40 | 5. Parámetros, `when` y aprobación manual en pipeline | [05-pipeline-parametros](05-pipeline-parametros/alumno.md) | 15 |
| 19:55 | 6. Credenciales de GitHub y pipeline multibranch con PRs | [06-multibranch](06-multibranch/alumno.md) | 20 |
| 20:15 | 7. Webhooks: GitHub dispara el build | [07-webhooks](07-webhooks/alumno.md) | 15 |
| 20:30 | 8. Instalar y administrar plugins | [08-plugins](08-plugins/alumno.md) | 10 |
| 20:40 | 9. Credenciales en pipelines: build y push de imagen Docker | [09-credenciales-docker](09-credenciales-docker/alumno.md) | 15 |
| 20:55 | Cierre y tarea | | 5 |

## Módulos extra (si el grupo va rápido, o como tarea)

| Módulo | Carpeta | Min |
|--------|---------|-----|
| 10. Agentes Docker por stage | [10-extra-docker-agents](10-extra-docker-agents/alumno.md) | 15 |
| 11. Agente inbound en otro contenedor y labels | [11-extra-agente-inbound](11-extra-agente-inbound/alumno.md) | 15 |
| 12. Jenkins como código (JCasC) | [12-extra-jcasc](12-extra-jcasc/alumno.md) | 15 |
| 13. Stages en paralelo y notificaciones a Discord | [13-extra-paralelo-notificaciones](13-extra-paralelo-notificaciones/alumno.md) | 15 |
| 14. Shared libraries | [14-extra-shared-library](14-extra-shared-library/alumno.md) | 20 |

## Otros archivos

- [sample-app](sample-app/): el proyecto de ejemplo `libreria-api` (Flask). El docente lo publica como template en GitHub antes de la clase.
- [troubleshooting.md](troubleshooting.md): errores frecuentes y cómo salir.
- [cheatsheet.md](cheatsheet.md): resumen de sintaxis del Jenkinsfile.
- [entregable.md](entregable.md): tarea y rúbrica.
