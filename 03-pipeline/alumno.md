# Módulo 3: Pipeline declarativo en la UI (alumno)

**Objetivo:** escribir el primer Jenkinsfile, entender sus bloques, y usar las herramientas para descubrir sintaxis.

Todo en el navegador.

## 1. Creación del job

1. **New Item**, nombre `03-pipeline-ui`, tipo **Pipeline**, **OK**.
2. Bajar hasta la sección **Pipeline**. En **Definition** dejar **Pipeline script**.
3. Pegar este script:

```groovy
pipeline {
    agent any

    environment {
        APP = 'libreria-api'
        SALUDO = 'Hola'
    }

    stages {
        stage('Preparar') {
            steps {
                echo "${SALUDO}, construyendo ${APP} build #${BUILD_NUMBER}"
                sh 'python3 --version'
                sh 'docker version --format "{{.Server.Version}}"'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "Corriendo tests..."
                    sleep 2
                    echo "Tests OK"
                    exit 0
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Desplegando ${APP}"
            }
        }
    }

    post {
        always {
            echo 'Esto corre siempre, pase lo que pase'
        }
        success {
            echo 'Build verde'
        }
        failure {
            echo 'Build rojo: aca iria un aviso a Slack o Discord'
        }
    }
}
```

4. **Save** y **Build Now**.

## 2. Revisión del resultado

En la página del job aparece la **Stage View**: una columna por stage con su tiempo. Hacer clic en el build `#1` y después en **Console Output**. Observar que cada stage aparece marcado en la salida.

## 3. Comprensión de los bloques

| Bloque | Para qué |
|--------|----------|
| `agent any` | Dónde corre: cualquier executor libre |
| `environment { }` | Variables para todo el pipeline |
| `stages { stage('X') { steps { } } }` | La secuencia de trabajo |
| `echo` | Imprime |
| `sh` | Ejecuta un comando de shell (Linux, porque Jenkins corre en un contenedor Linux) |
| `sh ''' ... '''` | Varias líneas de shell |
| `post { }` | Qué hacer al terminar: `always`, `success`, `failure` |

Sobre comillas en Groovy:

- `'texto'` (simple): Groovy no toca el texto. `$VAR` lo resuelve el shell.
- `"texto ${VAR}"` (doble): Groovy reemplaza `${VAR}` antes de ejecutar.

Regla práctica: usar comilla simple salvo que se necesite una variable de Groovy.

## 4. Provocar un fallo

1. **Configure**. En el stage Test cambiar `exit 0` por `exit 1`. **Save**, **Build Now**.
2. Revisar la Stage View: Test en rojo, Deploy ni corrió. En el Console Output, el mensaje de `post { failure }` sí apareció.
3. Volver a poner `exit 0`.

## 5. Descubrir sintaxis con el Snippet Generator

1. En la página del job, hacer clic en **Pipeline Syntax** (menú izquierdo).
2. En **Sample Step** elegir `archiveArtifacts: Archive the artifacts`.
3. En **Files to archive** indicar `resultado.txt`. Hacer clic en **Generate Pipeline Script**.
4. Copiar el resultado. Volver al job, **Configure**, y modificar el stage Deploy:

```groovy
        stage('Deploy') {
            steps {
                echo "Desplegando ${APP}"
                sh 'echo "Desplegado build ${BUILD_NUMBER} el $(date)" > resultado.txt'
                archiveArtifacts artifacts: 'resultado.txt'
            }
        }
```

5. **Save**, **Build Now**. El build tiene un artefacto.

## 6. Probar sin guardar: Replay

1. Abrir el último build. En el menú izquierdo, **Replay**.
2. Cambiar algo en el script (un `echo`). **Run**.
3. Corre con el cambio, pero la config del job no cambió. Sirve para experimentar.

## Checkpoint

Un build verde de 3 stages con artefacto, un build rojo donde Deploy no corrió, y se sabe usar Pipeline Syntax y Replay.

**Pausa 10 min.**
