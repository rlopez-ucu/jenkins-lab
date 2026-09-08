# Entregable

**Fecha límite:** una semana después de la clase.

**Qué entregar:** un mensaje en el canal del curso con:

1. Link al repositorio propio `libreria-api` en GitHub.
2. Captura de pantalla de un PR mergeado donde se vea el check de Jenkins en verde.
3. Link a la imagen propia en Docker Hub.

## Rúbrica (10 puntos)

| Criterio | Puntos | Cómo se verifica |
|----------|--------|------------------|
| El repo tiene un Jenkinsfile declarativo con stages de lint y tests, y publica resultados JUnit | 2 | Lectura del Jenkinsfile |
| Existe un pipeline multibranch que construye ramas y PRs | 2 | Captura del PR con el check de Jenkins |
| El pipeline tiene al menos un parámetro y un stage condicionado con `when` | 2 | Lectura del Jenkinsfile |
| Un push dispara el build por webhook, o el scan periódico está configurado | 1 | Captura de Recent Deliveries o de la config del job |
| La imagen se construye, pasa un smoke test y se publica solo desde `main` | 2 | Link a Docker Hub con tag numérico y `when { branch 'main' }` en el push |
| Ningún secreto aparece en el repo ni en los logs | 1 | Búsqueda de tokens en el repo y en el Console Output |

## Para nota extra (hasta 2 puntos)

Uno de estos, a elección:

- Stage de tests corriendo en `agent { docker { image 'python:3.12-slim' } }` (módulo 10).
- Notificación a Discord o Slack en `post { failure }` con la URL como credencial (módulo 13).
- El `00-setup` del Jenkins propio reproducible con JCasC, incluyendo la credencial de GitHub por variable de entorno (módulo 12).
- Shared library con al menos un step propio usado desde `libreria-api` (módulo 14).

## Preguntas para el informe (opcional, 5 líneas cada una)

1. ¿Qué pasa si dos personas hacen push a `main` al mismo tiempo? ¿Cómo lo maneja Jenkins? (Pista: `disableConcurrentBuilds`.)
2. ¿Por qué el `docker push` corre solo en `main` y no en los PRs?
3. Si el token de Docker Hub se filtra, ¿qué se debe hacer y en qué orden?
