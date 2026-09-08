# Jenkinsfile: resumen de sintaxis

## Esqueleto

```groovy
pipeline {
    agent any                         // o: agent none, agent { label 'x' }, agent { docker { image 'x' } }
    options { timestamps(); timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds() }
    environment { APP = 'libreria-api'; TAG = "${BUILD_NUMBER}" }
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: '')
        choice(name: 'ENTORNO', choices: ['dev', 'qa', 'prod'], description: '')
        booleanParam(name: 'TESTS', defaultValue: true, description: '')
    }
    triggers { cron('H 2 * * *') }   // o pollSCM('H/5 * * * *')
    stages {
        stage('Nombre') {
            when { branch 'main' }
            steps { sh 'comando' }
            post { always { echo 'fin del stage' } }
        }
    }
    post { always { } success { } failure { } unstable { } aborted { } changed { } }
}
```

## Steps utilizados

| Step | Ejemplo |
|------|---------|
| Imprimir | `echo "texto ${VAR}"` |
| Shell | `sh 'cmd'`, `sh '''multi\nlinea'''`, `def out = sh(script: 'cmd', returnStdout: true).trim()` |
| Artefactos | `archiveArtifacts artifacts: 'dist/**', fingerprint: true` |
| Tests | `junit 'reports/*.xml'`, `junit allowEmptyResults: true, testResults: '...'` |
| Aprobación | `input message: '?', ok: 'Si'`, `input(message: '?', submitter: 'admin,lider')` |
| Timeout | `timeout(time: 5, unit: 'MINUTES') { ... }` |
| Reintento | `retry(3) { sh 'cmd inestable' }` |
| Secretos | `withCredentials([usernamePassword(credentialsId: 'id', usernameVariable: 'U', passwordVariable: 'P')]) { }` |
| | `withCredentials([string(credentialsId: 'id', variable: 'TOKEN')]) { }` |
| | `withCredentials([file(credentialsId: 'id', variable: 'RUTA')]) { }` |
| Carpeta | `dir('sub') { sh 'pwd' }` |
| Pasar archivos entre stages | `stash name: 'x', includes: '**'` / `unstash 'x'` |
| Limpiar | `cleanWs()` |
| Checkout explícito | `checkout scm` |

## Condiciones `when`

```groovy
when { branch 'main' }
when { branch pattern: 'release/.*', comparator: 'REGEXP' }
when { changeRequest() }                       // es un PR
when { changeRequest target: 'main' }
when { not { branch 'main' } }
when { expression { params.ENTORNO == 'prod' } }
when { environment name: 'DEPLOY', value: 'true' }
when { allOf { branch 'main'; expression { params.TESTS } } }
when { anyOf { branch 'main'; branch 'develop' } }
when { beforeAgent true; branch 'main' }       // evalúa antes de pedir agente
```

## Paralelo

```groovy
stage('Verificar') {
    failFast true
    parallel {
        stage('Lint') { steps { sh 'ruff check .' } }
        stage('Test') { steps { sh 'pytest' } }
    }
}
```

## Variables de entorno

| Variable | Contenido |
|----------|-----------|
| `BUILD_NUMBER`, `BUILD_ID` | Número del build |
| `JOB_NAME` | `carpeta/job` |
| `BUILD_URL`, `JOB_URL`, `JENKINS_URL` | Links |
| `WORKSPACE` | Ruta del workspace |
| `NODE_NAME` | Agente donde corre |
| `BRANCH_NAME` | Rama (multibranch) |
| `CHANGE_ID`, `CHANGE_TARGET`, `CHANGE_AUTHOR`, `CHANGE_URL` | Datos del PR (multibranch) |
| `GIT_COMMIT`, `GIT_BRANCH`, `GIT_URL` | Datos del checkout |

Acceso: `env.BRANCH_NAME` en Groovy, `$BRANCH_NAME` en `sh`, `params.X` para parámetros.

## Comillas

- `'simple'`: Groovy no interpola. `$VAR` lo resuelve el shell. Usar por defecto y siempre con secretos.
- `"doble ${x}"`: Groovy interpola antes. Para `params.X`, `env.X`, variables Groovy.
- `"""triple doble"""`: multilínea con interpolación. Se escapa con `\$` lo que deba resolver el shell.

## `currentBuild`

`currentBuild.result`, `currentBuild.currentResult`, `currentBuild.durationString`, `currentBuild.displayName = "#${BUILD_NUMBER} v${params.VERSION}"`, `currentBuild.description = 'texto'`.

## Herramientas

- **Pipeline Syntax** (en cada job): Snippet Generator, Declarative Directive Generator, lista de variables.
- **Replay** (en cada build): editar y re-ejecutar sin guardar.
- **Scan Repository Now** (multibranch): forzar detección de ramas y PRs.
- Validar sintaxis desde la terminal:

```bash
curl -s -u usuario:password -X POST -F "jenkinsfile=<Jenkinsfile" http://localhost:8080/pipeline-model-converter/validate
```

En PowerShell: `curl.exe` en vez de `curl`.
