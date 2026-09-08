# Módulo 10 (extra): Agentes Docker por stage (alumno)

**Objetivo:** que cada stage corra dentro de la imagen Docker que necesita, sin instalar nada en Jenkins.

Requiere el plugin **Docker Pipeline** (módulo 8).

## 1. El problema

Python está en Jenkins porque se agregó al Dockerfile. Si el equipo tiene proyectos en Java, Node y Go, habría que incluir todo. En vez de eso, cada stage puede correr en un contenedor con la imagen que le sirva.

## 2. Cambiar el Jenkinsfile

Reemplazar el archivo entero. Los cambios están marcados con comentarios `// NUEVO`:

```groovy
pipeline {
    agent none   // NUEVO: cada stage elige su agente

    options {
        timestamps()
    }

    environment {
        IMAGE = "<usuario-dockerhub>/libreria-api"
        SMOKE = "smoke-${BUILD_NUMBER}"
    }

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'       // NUEVO: corre en este contenedor
                    args '--volumes-from jenkins'  // NUEVO: comparte el workspace
                    reuseNode true
                }
            }
            steps {
                sh '''
                    python3 --version
                    pip install --quiet -r requirements.txt
                    ruff check .
                    pytest --junitxml=reports/junit.xml
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('Build imagen') {
            agent any   // NUEVO: este necesita el docker del controller
            steps {
                sh 'docker build --build-arg APP_VERSION=${BUILD_NUMBER} -t ${IMAGE}:${BUILD_NUMBER} .'
            }
        }

        stage('Smoke test') {
            agent any
            steps {
                sh '''
                    docker run -d --rm --name ${SMOKE} --network jenkins_net ${IMAGE}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://${SMOKE}:5000/health
                    echo
                    docker rm -f ${SMOKE}
                '''
            }
        }

        stage('Push imagen') {
            agent any
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                    sh '''
                        echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
                        docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:latest
                        docker push ${IMAGE}:${BUILD_NUMBER}
                        docker push ${IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }
    }
}
```

Qué cambió:

- `agent none` arriba: ningún stage corre hasta que se indique dónde.
- `agent { docker { image 'python:3.12-slim' } }`: Jenkins descarga la imagen, levanta un contenedor, monta el workspace y corre los `steps` adentro. Al terminar lo borra.
- `args '--volumes-from jenkins'`: como Jenkins también está en un contenedor, el workspace no existe en la máquina local sino en el volumen de Jenkins. Con esto el contenedor de Python lo ve.
- `reuseNode true`: usa el mismo workspace, así el `post` encuentra `reports/junit.xml`.
- Ya no hace falta el venv: el contenedor es descartable.

## 3. Push y revisión

```bash
git commit -am "Agente docker para tests"
git push
```

En el Console Output del stage Test:

- `docker pull python:3.12-slim` (solo la primera vez).
- Un `docker run` largo que armó el plugin. Ahí está el `--volumes-from jenkins`.
- `python3 --version` indica `3.12.x`. En el controller es 3.13. Los tests corrieron en otro Python.

## 4. Cambiar la versión

Cambiar `python:3.12-slim` por `python:3.11-slim`. Hacer push. El log indica 3.11. Cambiar de versión de lenguaje es cambiar una línea.

## Checkpoint

El stage Test corre dentro de un contenedor de Python distinto al de Jenkins, y se puede cambiar sin tocar el Dockerfile de Jenkins.
