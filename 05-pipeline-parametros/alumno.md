# Módulo 5: Parámetros, condiciones y aprobación manual (alumno)

**Objetivo:** que el pipeline reciba parámetros, salte stages según condiciones y pida aprobación antes de "ir a prod".

Se sigue trabajando en el repositorio propio `libreria-api` y en el job `04-libreria-scm`.

## 1. Agregado de parámetros y nuevos stages

Editar el `Jenkinsfile`. Agregar el bloque `parameters` después de `options`, y dos stages nuevos después de `Test`. El archivo completo queda así:

```groovy
pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        choice(name: 'ENTORNO', choices: ['dev', 'qa', 'prod'], description: 'Ambiente destino')
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version a desplegar')
        booleanParam(name: 'EJECUTAR_TESTS', defaultValue: true, description: 'Correr los tests')
    }

    stages {
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

        stage('Aprobacion') {
            when {
                expression { params.ENTORNO == 'prod' }
            }
            steps {
                input message: "Desplegar la version ${params.VERSION} a PRODUCCION?", ok: 'Si, desplegar'
            }
        }

        stage('Deploy') {
            steps {
                echo "Desplegando ${params.VERSION} al ambiente ${params.ENTORNO}"
                sh 'echo "Entorno desde el shell: $ENTORNO, version $VERSION"'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
    }
}
```

Qué cambió:

- `parameters { }`: define el formulario. Mismos tipos que en el módulo 2, pero en código.
- `params.ENTORNO`: así se leen en Groovy. En `sh` también existen como `$ENTORNO`.
- `when { expression { ... } }`: si da falso, el stage se salta y el pipeline sigue.
- `input`: frena el pipeline y espera que alguien apruebe en la UI.
- `junit allowEmptyResults: true`: si se saltan los tests no hay XML, y sin esto el `post` fallaría.

## 2. Subida y primera ejecución

```bash
git commit -am "Parametros, when e input"
git push
```

En Jenkins, **Build Now** en `04-libreria-scm`.

Este primer build corre con los valores por defecto y **no** solicita nada. Jenkins recién se entera de que el pipeline tiene parámetros al leer el nuevo Jenkinsfile. A partir de ahora el botón dice **Build with Parameters**.

Observar el Console Output de este primer build: `params.ENTORNO` imprime `dev` (el default), pero la línea `Entorno desde el shell:` sale vacía. Como el build no se lanzó con parámetros, Jenkins no creó las variables de entorno. A partir del segundo build van a estar.

## 3. Prueba de las combinaciones

**Build with Parameters** tres veces:

1. `ENTORNO=dev`: el stage Aprobacion aparece gris (omitido) y Deploy corre.
2. `ENTORNO=prod`, `VERSION=2.0.0`: el pipeline se queda esperando en Aprobacion. Entrar al build en curso; en la Stage View aparece un cuadro con el mensaje y los botones **Si, desplegar** / **Abort**. También hay un link en el Console Output. Aprobar. Deploy corre con 2.0.0.
3. `ENTORNO=qa` y `EJECUTAR_TESTS` desmarcado: Test se salta.

Abrir **Parameters** en cada build para ver con qué corrió.

## 4. Para saber

Mientras `input` espera, el build ocupa un executor (la instancia tiene 2). Si dos builds quedan esperando aprobación, nada más corre. La solución es poner `agent none` arriba y `agent any` dentro de cada stage que necesite ejecutar comandos; el stage de `input` queda sin agent. Se ve en el módulo 13 si hay tiempo.

## Checkpoint

Cuatro builds: uno con defaults, uno a dev, uno a prod aprobado a mano, uno sin tests. Se sabe qué hacen `parameters`, `when` e `input`.
