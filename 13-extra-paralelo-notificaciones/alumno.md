# Módulo 13 (extra): Stages en paralelo y notificaciones (alumno)

**Objetivo:** correr lint y tests al mismo tiempo, no bloquear executors mientras alguien aprueba, y avisar por Discord al terminar.

## 1. Webhook de Discord

1. En un servidor de Discord donde se tenga rol de admin (crear uno de prueba si hace falta): **Server Settings > Integrations > Webhooks > New Webhook**.
2. Elegir un canal, **Copy Webhook URL**.
3. En Jenkins: **Manage Jenkins > Credentials > System > Global > Add Credentials**. Kind: `Secret text`. Secret: la URL. ID: `discord-webhook`. **Create**.

Si no se usa Discord, Slack tiene lo mismo (Incoming Webhooks) con el mismo formato de JSON salvo que el campo se llama `text` en vez de `content`.

## 2. Jenkinsfile

Reemplazar el archivo entero:

```groovy
pipeline {
    agent none

    options {
        timestamps()
    }

    stages {
        stage('Verificar') {
            failFast true
            parallel {
                stage('Lint') {
                    agent any
                    steps {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --quiet -r requirements.txt
                            ruff check .
                        '''
                    }
                }
                stage('Tests') {
                    agent any
                    steps {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --quiet -r requirements.txt
                            pytest --junitxml=reports/junit.xml
                        '''
                        junit 'reports/junit.xml'
                    }
                }
            }
        }

        stage('Aprobar deploy') {
            when {
                branch 'main'
            }
            // Sin agent: no ocupa un executor mientras espera.
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    input message: 'Desplegar a produccion?', ok: 'Desplegar'
                }
            }
        }

        stage('Deploy') {
            agent any
            when {
                branch 'main'
            }
            steps {
                echo 'Desplegando...'
            }
        }
    }

    post {
        success {
            notificar('Build OK', 3066993)
        }
        failure {
            notificar('Build FALLO', 15158332)
        }
        aborted {
            notificar('Build cancelado', 9807270)
        }
    }
}

def notificar(String titulo, int color) {
    node {
        withCredentials([string(credentialsId: 'discord-webhook', variable: 'WEBHOOK')]) {
            sh """
                curl -s -H 'Content-Type: application/json' -d @- "\$WEBHOOK" <<'JSON'
                {
                  "embeds": [{
                    "title": "${titulo}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    "description": "Rama: ${env.BRANCH_NAME ?: '-'}\\nDuracion: ${currentBuild.durationString}",
                    "url": "${env.BUILD_URL}",
                    "color": ${color}
                  }]
                }
JSON
            """
        }
    }
}
```

Qué hay de nuevo:

- `parallel { }`: Lint y Tests corren a la vez, cada uno en un executor. `failFast` cancela el otro si uno falla.
- Cada rama paralela instala sus dependencias. Jenkins les da workspaces distintos (`libreria-api` y `libreria-api@2`), así que no comparten el `.venv`. Para pasar archivos chicos entre stages existe `stash`/`unstash` (ver cheatsheet); un venv no es buen candidato porque tiene symlinks.
- `agent none` arriba y `agent any` por stage: el stage `Aprobar deploy` no tiene agent, así que mientras espera no ocupa un executor.
- `timeout` alrededor de `input`: si nadie aprueba en 10 minutos, el build se cancela.
- `notificar(...)`: una función Groovy al final del archivo. `post` la llama con distinto título y color. Usa `withCredentials` con `string` para un `Secret text`. El `\$WEBHOOK` con barra evita que Groovy interpole el secreto; lo resuelve el shell.

## 3. Push y revisión

```bash
git commit -am "Paralelo y notificaciones"
git push
```

- Abrir el build > **Pipeline Overview**: se ve la bifurcación de Lint y Tests.
- En Discord llega un mensaje con link al build.
- Romper un test, hacer push: mensaje rojo. Arreglarlo: mensaje verde.

## Checkpoint

Lint y Tests en paralelo en la vista de grafo, y un mensaje en Discord por cada build.
