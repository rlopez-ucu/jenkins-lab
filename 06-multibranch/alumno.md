# Módulo 6: Credenciales de GitHub y pipeline multibranch (alumno)

**Objetivo:** que Jenkins descubra solo todas las ramas y PRs del repositorio propio, corra el pipeline en cada una, y muestre el resultado dentro de GitHub.

## 1. Creación de un token de GitHub (PAT)

1. Entrar a https://github.com/settings/personal-access-tokens/new
2. **Token name:** `jenkins-clase`. **Expiration:** 30 días.
3. **Repository access:** `Only select repositories` y elegir `libreria-api`.
4. **Permissions > Repository permissions**, indicar:
   - Contents: `Read-only`
   - Pull requests: `Read-only`
   - Commit statuses: `Read and write`
   - Metadata: `Read-only` (se marca solo)
5. **Generate token**. Copiarlo en ese momento: no se podrá ver de nuevo.

Este token es una contraseña. No se debe pegar en el Jenkinsfile, en un chat ni en un commit.

## 2. Guardar el token en Jenkins como credencial

1. **Manage Jenkins > Credentials**.
2. Hacer clic en **System** (en la tabla, columna Store) y después en **Global credentials (unrestricted)**.
3. **Add Credentials**:
   - Kind: `Username with password`
   - Username: el nombre de usuario de GitHub
   - Password: el token
   - ID: `github-pat`
   - Description: `PAT de GitHub para la clase`
4. **Create**.

A partir de ahora los jobs usan el ID `github-pat`. El token queda cifrado en disco y Jenkins lo tapa con `****` en los logs.

## 3. Actualización del Jenkinsfile

Agregar un stage `Info` al principio y cambiar el stage `Deploy` para que corra solo en `main`. Reemplazar el archivo entero por esto:

```groovy
pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version a desplegar')
        booleanParam(name: 'EJECUTAR_TESTS', defaultValue: true, description: 'Correr los tests')
    }

    stages {
        stage('Info') {
            steps {
                echo "Rama: ${env.BRANCH_NAME}"
                echo "PR: ${env.CHANGE_ID ?: 'no es un PR'}"
                echo "Rama destino del PR: ${env.CHANGE_TARGET ?: '-'}"
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

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Desplegando ${params.VERSION} desde main"
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

Se quitan `ENTORNO` y la aprobación manual: en un flujo multibranch, la rama decide el destino. `main` despliega, el resto solo prueba.

Subir los cambios:

```bash
git commit -am "Stage Info y deploy solo en main"
git push
```

## 4. Creación del job multibranch

1. **New Item**, nombre `06-libreria-mb`, tipo **Multibranch Pipeline**, **OK**.
2. **Branch Sources > Add source > GitHub**.
   - Credentials: `github-pat`
   - Repository HTTPS URL: `https://github.com/<usuario>/libreria-api`
   - Hacer clic en **Validate**. Debe decir "Credentials ok. Connected to ...".
3. En **Behaviours** dejar los tres que vienen: Discover branches, Discover pull requests from origin, Discover pull requests from forks. En "Discover pull requests from origin" elegir **Merging the pull request with the current target branch revision**.
4. **Scan Repository Triggers**: marcar **Periodically if not otherwise run** e indicar **1 minute**.
5. **Save**.

Jenkins escanea el repositorio. Revisar el **Scan Repository Log**: encontró `main`, vio que tiene Jenkinsfile, y creó un sub-job. Al entrar a `06-libreria-mb` se ve `main` como un job adentro, corriendo.

## 5. Trabajo como en un equipo: rama, PR, merge

### Crear una rama y cambiar algo

Mismos comandos en todos los sistemas:

```bash
git checkout -b feature/saludo
```

Editar `app.py`: en la función `health`, cambiar `"status": "ok"` por `"status": "ok", "saludo": "hola"`.

Editar `tests/test_app.py`: en `test_health` agregar una línea al final:

```python
    assert response.get_json()["saludo"] == "hola"
```

Push de la rama:

```bash
git add .
git commit -m "Agrego saludo al health"
git push -u origin feature/saludo
```

### Abrir el PR

1. En GitHub, en el repositorio propio, aparece un aviso "feature/saludo had recent pushes". Hacer clic en **Compare & pull request**.
2. Título cualquiera, **Create pull request**.

### Revisar lo que hizo Jenkins

1. En Jenkins, entrar a `06-libreria-mb` y hacer clic en **Scan Repository Now** (o esperar 1 minuto).
2. Aparecen dos jobs nuevos: `feature/saludo` y `PR-1`. Entrar a cada uno y revisar el stage `Info`: el PR tiene `CHANGE_ID=1` y `CHANGE_TARGET=main`. En ninguno corrió `Deploy`.
3. Volver al PR en GitHub y bajar hasta el final. Hay un check con el ícono de Jenkins: "continuous-integration/jenkins/pr-merge". Hacer clic en **Details** lleva al build. Eso es lo que ve quien revisa el PR.

### Hacer el merge

1. En GitHub, **Merge pull request**, **Confirm merge**. Se puede borrar la rama.
2. En Jenkins, **Scan Repository Now**. El job `main` corre de nuevo, y esta vez `Deploy` sí corre.
3. Los jobs `feature/saludo` y `PR-1` desaparecen (o quedan tachados) porque ya no existen en GitHub.

Traer main a la máquina local:

```bash
git checkout main
git pull
```

## 6. Variables que da el multibranch

| Variable | En una rama | En un PR |
|----------|-------------|----------|
| `BRANCH_NAME` | `main`, `feature/x` | `PR-1` |
| `CHANGE_ID` | vacía | número del PR |
| `CHANGE_TARGET` | vacía | rama destino |
| `CHANGE_AUTHOR` | vacía | quien abrió el PR |

Y condiciones para `when`:

```groovy
when { branch 'main' }
when { branch pattern: 'release/.*', comparator: 'REGEXP' }
when { changeRequest() }
when { not { changeRequest() } }
```

## Checkpoint

El job `06-libreria-mb` tiene el sub-job `main` verde con `Deploy` ejecutado, y el PR mergeado en GitHub muestra el check de Jenkins.
