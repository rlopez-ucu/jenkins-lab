# Módulo 4: Repositorio propio en GitHub y pipeline desde SCM (alumno)

**Objetivo:** tener el Jenkinsfile en el repositorio propio de GitHub y que Jenkins lo ejecute desde ahí, corriendo lint y tests reales.

## 1. Creación del repositorio propio desde el template

1. Entrar a https://github.com/<USUARIO_DOCENTE>/libreria-api (el link que pasó el docente).
2. Hacer clic en el botón verde **Use this template > Create a new repository**.
3. Owner: el usuario propio. Repository name: `libreria-api`. Dejarlo **Public**.
4. **Create repository**.

Ahora existe `https://github.com/<usuario>/libreria-api`, y pertenece al alumno.

## 2. Clonación en la máquina local

Se debe salir de la carpeta del repo de la clase y clonar el repositorio propio. Reemplazar `<usuario>`.

### Linux / macOS

```bash
cd ~
git clone https://github.com/<usuario>/libreria-api.git
cd libreria-api
ls
```

### Windows (PowerShell)

```powershell
cd ~
git clone https://github.com/<usuario>/libreria-api.git
cd libreria-api
dir
```

## 3. Reemplazo del Jenkinsfile

Abrir `Jenkinsfile` con el editor (VS Code: `code Jenkinsfile`, en cualquier sistema). Borrar todo y pegar:

```groovy
pipeline {
    agent any

    options {
        timestamps()
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
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
        }
    }
}
```

Qué hace:

- `options { timestamps() }`: cada línea del log lleva hora.
- **Instalar dependencias:** crea un entorno virtual de Python e instala lo de `requirements.txt`. Cada `sh` arranca un shell nuevo, por eso cada stage vuelve a hacer `. .venv/bin/activate`.
- **Lint:** `ruff` revisa el estilo del código. Si encuentra problemas, devuelve distinto de 0 y el build falla.
- **Test:** `pytest` corre los tests y escribe un XML en formato JUnit.
- `post { always { junit ... } }`: Jenkins lee ese XML y arma la pestaña de resultados, pasen o fallen los tests.

## 4. Subida del cambio

Mismo comando en todos los sistemas:

```bash
git add Jenkinsfile
git commit -m "Pipeline con lint y tests"
git push
```

Si `git push` solicita usuario y contraseña: GitHub no acepta contraseñas. En Windows suele abrirse el navegador para iniciar sesión; hacerlo. En Linux/macOS, usar un token: crearlo en https://github.com/settings/tokens/new con el scope `repo` y pegarlo como contraseña. Guardarlo, se vuelve a usar en el módulo 6.

## 5. Creación del job desde SCM

1. En Jenkins: **New Item**, nombre `04-libreria-scm`, tipo **Pipeline**, **OK**.
2. Sección **Pipeline**:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/<usuario>/libreria-api.git`
   - **Credentials:** `- none -` (el repo es público)
   - **Branch Specifier:** `*/main`
   - **Script Path:** `Jenkinsfile`
3. **Save** y **Build Now**.

## 6. Revisión del resultado

- En el Console Output se ve el `git clone`, después `pip install`, `ruff`, `pytest`.
- En la página del build, hacer clic en **Test Result**: 5 tests pasaron. Volver a la página del job: apareció un gráfico de tendencia de tests.

## 7. Ruptura de un test

1. Abrir `tests/test_app.py`. En `test_health` cambiar `"ok"` por `"roto"`.
2. Commit y push:

```bash
git commit -am "Rompo un test a proposito"
git push
```

3. En Jenkins, **Build Now**. El build queda rojo (o amarillo "unstable"). Entrar a **Test Result**: indica qué test falló y muestra el traceback.
4. Arreglarlo (`"roto"` → `"ok"`), commit y push, **Build Now**. Verde.

## Checkpoint

El repositorio propio tiene un Jenkinsfile con tres stages, el job `04-libreria-scm` está verde, y la pestaña Test Result muestra 5 tests.
