# Módulo 1: Primer job freestyle (alumno)

**Objetivo:** crear un job desde la UI, correrlo, leer la salida, guardar un artefacto y ver un build fallar.

Todo este módulo se hace en el navegador. No hay diferencias entre Linux y Windows.

## 1. Recorrida rápida

En http://localhost:8080 ubicar:

- **New Item** (izquierda arriba): crear jobs.
- **Manage Jenkins**: la configuración de todo.
- **Build Executor Status** (izquierda abajo): cuántos builds pueden correr a la vez. Hoy son 2.

## 2. Crear el job

1. Clic en **New Item**.
2. Nombre: `01-hola-freestyle`.
3. Elegir **Freestyle project** y clic en **OK**.
4. En **Description** escribir: `Mi primer job`.
5. Bajar hasta **Build Steps** y clic en **Add build step > Execute shell**.
6. Pegar esto:

```bash
echo "Hola, soy un build de Jenkins"
echo "Usuario dentro del contenedor: $(whoami)"
echo "Carpeta de trabajo: $(pwd)"
echo "Build numero: $BUILD_NUMBER"
echo "Nombre del job: $JOB_NAME"
python3 --version
docker version --format 'Docker cliente {{.Client.Version}} / servidor {{.Server.Version}}'
date > build-info.txt
echo "Generado por $JOB_NAME #$BUILD_NUMBER" >> build-info.txt
```

7. Bajar a **Post-build Actions** y clic en **Add post-build action > Archive the artifacts**.
8. En **Files to archive** indicar `build-info.txt`.
9. Clic en **Save**.

## 3. Correr el build

1. En la página del job, clic en **Build Now**.
2. En **Build History** (izquierda) aparece `#1`. Clic en él.
3. Clic en **Console Output**. Leer toda la salida. Observar:
   - Qué usuario corre el build (`root`, porque así se configuró el contenedor).
   - El workspace: `/var/jenkins_home/workspace/01-hola-freestyle`.
   - `python3` y `docker` responden: están instalados en la imagen de Jenkins, no en la máquina local.
   - Termina con `Finished: SUCCESS`.
4. Volver a la página del build. Aparece **Build Artifacts** con `build-info.txt`. Hacer clic y revisar el contenido.

## 4. Revisar el workspace

En la página del job, clic en **Workspace**. Es la carpeta donde corrió el build. Ahí está `build-info.txt` también.

Se puede ver desde la terminal, entrando al contenedor:

```bash
docker exec jenkins ls -la /var/jenkins_home/workspace/01-hola-freestyle
```

(Mismo comando en Linux, macOS y PowerShell.)

## 5. Hacerlo fallar

1. En el job, clic en **Configure**.
2. Al final del shell agregar una línea:

```bash
exit 1
```

3. **Save** y **Build Now**.
4. El build `#2` sale rojo. Abrir su Console Output y revisar la última línea: `Finished: FAILURE`.

Un comando que termina con un código distinto de 0 hace fallar el build. Así es como Jenkins sabe si los tests pasaron.

5. Volver a **Configure**, borrar el `exit 1` y guardar.

## 6. Variables que Jenkins provee

Estas variables existen en todo build. Se usan en toda la clase:

| Variable | Qué tiene |
|----------|-----------|
| `BUILD_NUMBER` | Número del build (1, 2, 3...) |
| `JOB_NAME` | Nombre del job |
| `WORKSPACE` | Ruta del workspace |
| `BUILD_URL` | Link al build |
| `JENKINS_URL` | Link a Jenkins |

La lista completa está en http://localhost:8080/env-vars.html/

## Checkpoint

Debe haber un job con un build verde (con artefacto) y uno rojo, y debe quedar claro por qué cada uno terminó como terminó.
