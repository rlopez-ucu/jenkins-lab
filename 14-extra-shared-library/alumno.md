# Módulo 14 (extra): Shared libraries (alumno)

**Objetivo:** sacar código repetido de los Jenkinsfiles a una librería que todos los pipelines puedan usar.

## 1. Creación del repositorio de la librería

1. En GitHub: **New repository**, nombre `jenkins-shared-lib`, público, con README. **Create**.
2. Clonarlo y crear la carpeta `vars`:

### Linux / macOS

```bash
cd ~
git clone https://github.com/<usuario>/jenkins-shared-lib.git
cd jenkins-shared-lib
mkdir vars
```

### Windows (PowerShell)

```powershell
cd ~
git clone https://github.com/<usuario>/jenkins-shared-lib.git
cd jenkins-shared-lib
mkdir vars
```

3. Crear `vars/notificar.groovy` con este contenido (es la función del módulo 13, como step):

```groovy
// Uso en un Jenkinsfile: notificar('Build OK', 3066993)
def call(String titulo, int color) {
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

4. Crear `vars/pipelinePython.groovy`, un pipeline completo empaquetado:

```groovy
// Uso en un Jenkinsfile:
//   @Library('ucu-lib') _
//   pipelinePython(imagen: 'usuario/app')
def call(Map config = [:]) {
    pipeline {
        agent any

        options {
            timestamps()
        }

        stages {
            stage('Instalar') {
                steps {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --quiet -r requirements.txt
                    '''
                }
            }
            stage('Lint') {
                steps {
                    sh '. .venv/bin/activate && ruff check .'
                }
            }
            stage('Test') {
                steps {
                    sh '. .venv/bin/activate && pytest --junitxml=reports/junit.xml'
                }
            }
            stage('Build imagen') {
                when { expression { config.imagen } }
                steps {
                    sh "docker build -t ${config.imagen}:${BUILD_NUMBER} ."
                }
            }
        }

        post {
            always {
                junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            }
            success {
                notificar('Build OK', 3066993)
            }
            failure {
                notificar('Build FALLO', 15158332)
            }
        }
    }
}
```

5. Subir los cambios:

```bash
git add .
git commit -m "Steps notificar y pipelinePython"
git push
```

## 2. Registro de la librería en Jenkins

1. **Manage Jenkins > System**. Bajar hasta **Global Trusted Pipeline Libraries** (o **Global Pipeline Libraries** en versiones anteriores). **Add**.
2. Name: `ucu-lib`. Default version: `main`.
3. Retrieval method: **Modern SCM**. Source: **Git**. Project Repository: `https://github.com/<usuario>/jenkins-shared-lib.git`.
4. **Save**.

## 3. Uso de la librería desde la app

En el repositorio propio `libreria-api`, reemplazar el Jenkinsfile entero por:

```groovy
@Library('ucu-lib') _

pipelinePython(imagen: '<usuario-dockerhub>/libreria-api')
```

El `_` después de `@Library(...)` es obligatorio. Es una rareza de Groovy: la anotación necesita algo a lo que aplicarse.

Hacer push. El pipeline corre con todos los stages definidos en la librería, y notifica a Discord.

## 4. Versionado

Si mañana se cambia la librería y se rompe algo, todos los repos que usan `main` se rompen. Para evitarlo, en la librería se crea un tag (`git tag v1 && git push --tags`) y en los Jenkinsfiles se indica `@Library('ucu-lib@v1') _`.

## 5. Para pensar

Ventaja: 30 repos con un Jenkinsfile de 3 líneas y una sola librería que mantener. Desventaja: quien lee el Jenkinsfile no ve qué hace el pipeline sin abrir otro repo. En equipos grandes, la librería la mantiene el equipo de plataforma y los demás la consumen.

## Checkpoint

El Jenkinsfile de `libreria-api` tiene 3 líneas y el pipeline corre desde la librería.
