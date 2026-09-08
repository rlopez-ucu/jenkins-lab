# Módulo 14 (extra): Shared libraries (docente)

**Tiempo:** 20 min.

## Conceptos a enseñar

- **El problema:** la función `notificar` del módulo 13 la quieren 30 repos. Copiarla 30 veces es lo que CI vino a evitar.
- **Shared library:** un repo Git con código Groovy que Jenkins carga en cualquier pipeline con `@Library('nombre') _`. Estructura: `vars/` para steps globales (un archivo = un step), `src/` para clases, `resources/` para archivos.
- **Steps custom:** `vars/notificar.groovy` con un método `call(...)` se usa como `notificar('Build OK', 3066993)` en el Jenkinsfile. Parece un step nativo.
- **Versionado:** `@Library('ucu-lib@v1')`. Los pipelines fijan una versión y la librería puede evolucionar sin romperlos.
- **Configuración:** Manage Jenkins > System > Global Pipeline Libraries. Se define una vez.

## Qué mostrar

1. El docente crea el repo `jenkins-shared-lib` en su cuenta de GitHub con `vars/notificar.groovy` y `vars/pipelinePython.groovy` (están en esta carpeta).
2. Configurar la librería global: Name `ucu-lib`, Default version `main`, Retrieval method Modern SCM > Git > URL del repo.
3. Reducir el Jenkinsfile de la app a `@Library('ucu-lib') _` + la definición del pipeline sin la función `notificar`. Hacer push. Funciona igual.
4. Mostrar `pipelinePython`: un pipeline entero como step. El Jenkinsfile de la app queda en 3 líneas. Discutir el trade-off: menos duplicación, más magia.

## Dónde suelen atascarse

- El `_` después de `@Library('ucu-lib')`: es obligatorio si no hay `import` en esa línea. Es una rareza de Groovy.
- Cambios en la librería no se ven: Jenkins la cachea por build; con `main` como versión, cada build nuevo trae la última.
- `vars/x.groovy` sin método `call`: no se puede invocar como `x()`.

## Checkpoint

El Jenkinsfile de la app usa `notificar` desde la librería y ya no define la función.
