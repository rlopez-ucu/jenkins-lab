# Módulo 9: Credenciales en pipelines, build y push de imagen (docente)

**Tiempo:** 15 min. **Hora:** 20:40 a 20:55.

## Conceptos a enseñar

- **`withCredentials`:** el step que expone una credencial como variables de entorno solo dentro de su bloque. Afuera no existen. Jenkins enmascara el valor en el log: si se imprime, se ve `****`.
- **Por qué `docker login --password-stdin`:** para que el token no quede en la línea de comando (que va al log y a `ps`).
- **Comilla simple en `sh`:** si se usa `"$DH_TOKEN"` con comilla doble de Groovy, el secreto se interpola en el script antes de ejecutarse y Jenkins avisa con un warning. Con comilla simple lo resuelve el shell y queda enmascarado. Es la regla del módulo 3 con una razón de seguridad.
- **El flujo build → smoke test → push:** construir la imagen con tag = número de build, levantarla, pegarle a `/health`, y solo si responde, subirla. Y solo desde `main`. Esto es CD en su forma mínima.
- **Docker outside of Docker:** Jenkins usa el daemon de la computadora a través del socket. La imagen queda en la computadora del alumno (que lo vean con `docker images`). El contenedor del smoke test corre en la red `jenkins_net` para que Jenkins lo alcance por nombre.
- **Tags:** `:BUILD_NUMBER` para trazabilidad y `:latest` por comodidad. Que sepan que `latest` no significa nada.

## Antes del módulo

Los alumnos necesitan cuenta en Docker Hub y un **access token** (Account Settings > Security > New Access Token, permisos Read & Write). Pedirles que lo generen mientras el docente explica.

## Qué mostrar

1. Cargar el token de Docker Hub como credencial `dockerhub` (Username with password; username = usuario de Docker Hub, password = token).
2. Pegar los tres stages nuevos en el Jenkinsfile. Explicar `environment { IMAGE = "..." }`, el smoke test y el `when { branch 'main' }` del push.
3. Push a main, esperar el webhook. Mostrar en el log: `docker build`, el `curl` al health que devuelve el JSON con la versión = número de build, `docker login` con `****`, y el push.
4. Abrir Docker Hub en el navegador: la imagen está. Ejecutar `docker images` en la computadora: también está.
5. Mostrar el intento de imprimir el secreto: agregar `sh 'echo $DH_TOKEN'` dentro del bloque y ejecutar. Sale `****`. Quitarlo.

## Dónde suelen atascarse

- `denied: requested access to the resource is denied`: el `IMAGE` no empieza con su usuario de Docker Hub, o el token es de solo lectura.
- El smoke test falla con `curl: (6) Could not resolve host`: el contenedor no está en `jenkins_net`. Verificar el `--network`.
- `port is already allocated`: no aplica, el smoke test no publica puertos. Si alguien agregó `-p`, que lo saque.
- El `post { always }` con `docker rm -f` es lo que evita contenedores zombies si el smoke falla. Mostrarlo.
- Windows: nada específico; todo corre dentro del contenedor.

## Checkpoint (20:55)

Build verde en `main` con la imagen publicada en Docker Hub con dos tags, y un intento fallido de imprimir el token que muestra `****`.

## Cierre (20:55 a 21:00)

- Repasar los tres hitos: job en la UI → Jenkinsfile en el repo → GitHub dispara y Jenkins publica.
- Mostrar `entregable.md`.
- Indicar los módulos extra para quien quiera seguir.
- Recordar apagar: `docker compose --profile ngrok down`. Los datos quedan en el volumen.
