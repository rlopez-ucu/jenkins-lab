# Errores frecuentes y cómo salir

Ordenados por módulo. Buscar el texto del error con Ctrl+F.

## Setup (módulo 0)

**`Cannot connect to the Docker daemon` / `error during connect`**
Docker no está corriendo. Windows y macOS: abrir Docker Desktop y esperar el ícono verde. Linux: `sudo systemctl start docker`.

**`permission denied while trying to connect to the Docker daemon socket`** (Linux)
El usuario no pertenece al grupo docker. Ejecutar `sudo usermod -aG docker $USER`, cerrar sesión y volver a entrar. Mientras tanto, usar `sudo docker compose ...`.

**`Bind for 0.0.0.0:8080 failed: port is already allocated`**
Otro programa usa el 8080. En `docker-compose.yml` cambiar `"8080:8080"` por `"8081:8080"` y usar http://localhost:8081 en todo lo que sigue.

**`cat: /var/jenkins_home/secrets/initialAdminPassword: No such file or directory`**
Jenkins todavía está arrancando. Esperar 30 segundos. `docker compose logs -f jenkins` muestra el progreso; la contraseña también aparece ahí entre líneas de asteriscos.

**La página dice "Jenkins is getting ready to work"**
Esperar y refrescar. La primera vez tarda hasta 1 minuto.

**Contraseña del admin olvidada**
Opción rápida: `docker compose down -v` y rehacer el wizard (se pierde todo). Opción sin perder: editar `config.xml` en el volumen para desactivar la seguridad. Pedir ayuda al docente.

## Freestyle y pipeline (módulos 1 a 5)

**`sh: python3: not found` o `docker: not found` dentro de un build**
La imagen de Jenkins es vieja. Ejecutar `docker compose build && docker compose up -d`.

**`expecting '}', found ''`** en un pipeline
Falta una llave de cierre. Contar las llaves. El número de línea del error suele apuntar al final del archivo, no a la llave que falta.

**`No such DSL method 'X' found`**
El step no existe con ese nombre o está fuera del bloque correcto (por ejemplo `choice` fuera de `parameters`). Buscarlo en Pipeline Syntax.

**No aparece "Build with Parameters"**
El Jenkinsfile con `parameters` todavía no corrió ni una vez. Ejecutar Build Now una vez.

**El `input` no muestra botones**
La página abierta es la del job. Entrar al build en curso; el prompt está en la Stage View y en Console Output.

**`$'\r': command not found`** o errores raros en `sh` (Windows)
El archivo tiene finales de línea CRLF. El repo trae `.gitattributes` para evitarlo; si se editó con un editor que forzó CRLF, convertir a LF (VS Code: abajo a la derecha, clic en CRLF > LF) y ejecutar `git config --global core.autocrlf input`.

## Git y GitHub (módulos 4 a 7)

**`git push` pide contraseña y no la acepta**
GitHub no acepta contraseñas. Usar un PAT como contraseña, o `gh auth login`. En Windows suele abrirse el navegador solo.

**`fatal: The current branch feature/x has no upstream branch`**
Ejecutar `git push -u origin feature/x`.

**Scan Repository Log dice `Not Found`** o `Could not connect`
El PAT no incluye el repo (fine-grained sin el repo seleccionado) o la URL está mal. Verificar con **Validate** en la configuración del Branch Source.

**El build corre pero no aparece el check en GitHub**
Al PAT le falta **Commit statuses: Read and write**. Regenerar el token con ese permiso y actualizar la credencial.

**El PR no aparece en el multibranch**
Jenkins todavía no escaneó el repo. Ejecutar **Scan Repository Now**.

**Webhook: GitHub muestra 302, 404 o 403**
La URL debe terminar en `/github-webhook/` con barra final. 403 con "No valid crumb" es porque se usó otra URL (`/job/x/build`).

**Webhook: el ping da 200 pero el push no dispara**
El webhook no tiene marcado el evento **Pushes**, o el multibranch tiene desactivado el escaneo por eventos. Revisar los eventos del webhook.

**ngrok: `authentication failed`**
Token mal pegado en `.env` (comillas, espacios) o el archivo se llama `.env.txt` (Windows). El archivo debe llamarse exactamente `.env`.

**ngrok muestra una página de advertencia**
Es la versión gratuita. Afecta solo a navegadores, no a los webhooks. Hacer clic en "Visit Site".

## Docker en pipelines (módulos 9 y 10)

**`denied: requested access to the resource is denied`** en `docker push`
El nombre de la imagen no empieza con el usuario propio de Docker Hub, o el token es de solo lectura.

**`curl: (6) Could not resolve host: smoke-N`**
El contenedor no está en `jenkins_net`. Verificar `--network jenkins_net` en el `docker run`.

**`curl: (22) The requested URL returned error`**
La app no levantó en 3 segundos, o falló. Ejecutar `docker logs smoke-N` desde la terminal local (si el contenedor todavía existe) o subir el `sleep`.

**El workspace está vacío dentro del agente Docker** (módulo 10)
Falta `args '--volumes-from jenkins'`.

**`docker: Error response from daemon: Conflict. The container name "/smoke-N" is already in use`**
Quedó un contenedor de un build anterior que falló antes del `post`. Ejecutar `docker rm -f smoke-N`.

## Agentes y JCasC (módulos 11 y 12)

**El agente dice `Connection refused` o `UnknownHostException: jenkins`**
Falta `--network jenkins_net` o la URL no es `http://jenkins:8080`.

**JCasC: `Invalid configuration elements` o `mapping values are not allowed`**
Indentación del YAML. Dos espacios, sin tabs.

**JCasC: `Configuration variable ${X} not found`**
La variable no está definida en el compose o en `.env`.

## Reset total

Cuando nada funciona y se quiere volver a cero:

```bash
docker compose --profile ngrok --profile cloudflared down -v
docker compose up -d
```

Se pierden jobs, credenciales y usuario. Rehacer el wizard (5 minutos).
