# Módulo 9: Credenciales en pipelines, build y push de imagen (alumno)

**Objetivo:** que el pipeline construya la imagen Docker de la app, la pruebe, y la suba a Docker Hub usando un secreto sin exponerlo.

## 1. Token de Docker Hub

1. Entrar a https://hub.docker.com/settings/security
2. **New Access Token**. Description: `jenkins-clase`. Permissions: `Read & Write`. **Generate**.
3. Copiarlo.

## 2. Guardar el token en Jenkins

1. **Manage Jenkins > Credentials > System > Global credentials > Add Credentials**.
2. Kind: `Username with password`. Username: el nombre de usuario de Docker Hub. Password: el token. ID: `dockerhub`. **Create**.

## 3. Agregar los stages al Jenkinsfile

Agregar un bloque `environment` y tres stages después de `Test`. Reemplazar `<usuario-dockerhub>` por el usuario propio. El archivo completo:

```groovy
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE = "<usuario-dockerhub>/libreria-api"
        SMOKE = "smoke-${BUILD_NUMBER}"
    }

    parameters {
        booleanParam(name: 'EJECUTAR_TESTS', defaultValue: true, description: 'Correr los tests')
    }

    stages {
        stage('Info') {
            steps {
                echo "Rama: ${env.BRANCH_NAME}"
                echo "PR: ${env.CHANGE_ID ?: 'no es un PR'}"
                sh 'git log -1 --oneline'
            }
        }

        stage('Instalar dependencias') {
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
                sh '''
                    . .venv/bin/activate
                    ruff check .
                '''
            }
        }

        stage('Test') {
            when {
                expression { params.EJECUTAR_TESTS }
            }
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/junit.xml
                '''
            }
        }

        stage('Build imagen') {
            steps {
                sh 'docker build --build-arg APP_VERSION=${BUILD_NUMBER} -t ${IMAGE}:${BUILD_NUMBER} .'
            }
        }

        stage('Smoke test') {
            steps {
                sh '''
                    docker run -d --rm --name ${SMOKE} --network jenkins_net ${IMAGE}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://${SMOKE}:5000/health
                    echo
                '''
            }
        }

        stage('Push imagen') {
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

    post {
        always {
            sh 'docker rm -f ${SMOKE} 2>/dev/null || true'
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
    }
}
```

Qué hace cada parte nueva:

- `environment { IMAGE, SMOKE }`: nombre de la imagen y del contenedor de prueba. El nombre de la imagen tiene que empezar con el usuario propio de Docker Hub.
- **Build imagen:** construye con el número de build como versión y como tag. La imagen queda en el Docker de la máquina local (Jenkins usa el daemon local por el socket).
- **Smoke test:** levanta la imagen en la red `jenkins_net` (la misma de Jenkins) y le pega a `/health`. Si no responde, `curl -f` falla y el build también. Observar que el JSON dice `"version": "<número de build>"`.
- **Push imagen:** solo en `main`. `withCredentials` expone el usuario y el token como variables de entorno solo dentro de ese bloque. `--password-stdin` evita que el token quede en la línea de comando.
- `post { always }`: borra el contenedor de prueba pase lo que pase.

Sobre comillas: dentro de `withCredentials` usar `sh '''...'''` con comilla simple. Si se usa comilla doble de Groovy, el secreto se pega en el script antes de ejecutar y Jenkins avisa con un warning.

## 4. Subir los cambios y revisar

```bash
git commit -am "Build, smoke test y push de imagen"
git push
```

El webhook dispara el build de `main`. En el Console Output:

- `docker build` construye la imagen.
- El `curl` devuelve `{"status":"ok","version":"<numero>"}`.
- `docker login` dice `Login Succeeded` y el token aparece como `****`.
- `docker push` sube las capas.

Verificar:

- En https://hub.docker.com/r/<usuario-dockerhub>/libreria-api/tags están los dos tags.
- En la terminal local, `docker images` muestra la imagen (mismo comando en todos los sistemas).

## 5. Intentar filtrar el secreto

Dentro del bloque `withCredentials` agregar `sh 'echo "El token es $DH_TOKEN"'`. Push. Revisar el log: `El token es ****`. Jenkins enmascara el valor de cualquier credencial. Sacar esa línea y volver a subir.

## 6. Probar el flujo completo con un PR

Crear una rama, cambiar algo, abrir un PR. El pipeline corre en el PR: build y smoke test sí, push no (no es `main`). Hacer merge: el build de `main` sube la imagen nueva.

## Checkpoint

La imagen está en Docker Hub con el tag del último build de `main`, y se vio el token enmascarado en el log.
