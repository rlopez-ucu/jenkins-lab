# Módulo 7: Webhooks (docente)

**Tiempo:** 15 min. **Hora:** 20:15 a 20:30.

## Conceptos a enseñar

- **Polling vs webhook:** hasta ahora Jenkins pregunta cada minuto "¿hay algo nuevo?". Con webhook, GitHub avisa en el momento. Menos carga, menos espera, y así funciona en cualquier empresa.
- **Un webhook es un HTTP POST:** GitHub hace un POST con un JSON a una URL que se le indica. Jenkins expone `/github-webhook/` para recibirlo. Se puede ver el payload en GitHub (Recent Deliveries) y reenviarlo a mano. Eso lo hace fácil de depurar.
- **El problema de localhost:** GitHub no puede llegar a la computadora del alumno. Solución: un túnel (ngrok) que da una URL pública y la redirige al contenedor. En una empresa, Jenkins tiene una URL pública o está en la misma red que el servidor Git.
- **Jenkins URL:** Jenkins arma links (en los commit statuses, por ejemplo) con la URL configurada en System. Con el túnel, conviene ponerle la URL pública para que los links del PR funcionen desde afuera. Opcional en clase.
- **Seguridad, en una frase:** el endpoint acepta cualquier POST, por eso existe el "secret" del webhook y el plugin lo valida si se configura. Hoy no se configura; que sepan que existe.

## Qué mostrar

1. Explicar el túnel con un dibujo: GitHub → ngrok.com → contenedor ngrok en la computadora → contenedor jenkins. Compose los pone en la misma red, por eso `http jenkins:8080`.
2. Levantar el túnel con el perfil de compose. Mostrar http://localhost:4040 con la URL pública.
3. En GitHub, Settings > Webhooks > Add. Payload URL = URL pública + `/github-webhook/`. Content type `application/json`. Events: push y pull requests. Mostrar el ping verde en Recent Deliveries.
4. **Desactivar el scan periódico** en el multibranch para demostrar que es el webhook el que dispara.
5. Hacer un commit trivial y push. Mostrar en Jenkins que el build arrancó en segundos, y en GitHub la delivery `push` con respuesta 200.
6. Mostrar **Redeliver** en GitHub: "si Jenkins estaba caído, se reenvía el evento".
7. Volver a activar el scan periódico. "Doble seguridad".

## Alternativa sin cuenta

Si alguien no tiene token de ngrok, el perfil `cloudflared` da una URL pública sin cuenta. Es menos estable (la URL cambia en cada arranque) pero alcanza para la clase. Está en `alumno.md`.

## Dónde suelen atascarse

- Olvidan la barra final en `/github-webhook/`. Sin la barra, Jenkins redirige y GitHub muestra 302 o 404.
- Pegan la URL de http://localhost:4040 en vez de la pública que se ve ahí adentro.
- El `.env` no está en `00-setup`, o tiene comillas alrededor del token. Sin comillas.
- ngrok free muestra una página de advertencia si abren la URL en un navegador. A los webhooks no les pasa. Que no se asusten.
- Windows: `Copy-Item` para copiar `.env.example` a `.env`, o el explorador. Y que el archivo no quede como `.env.txt`.
- El ping llega (200) pero el push no dispara: el multibranch necesita que el evento sea `push` o `pull_request`; verificar que marcaron los dos eventos.

## Checkpoint (20:30)

Un push a `main` dispara el build en menos de 10 segundos sin scan periódico, y en GitHub la delivery muestra 200.
