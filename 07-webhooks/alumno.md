# Módulo 7: Webhooks (alumno)

**Objetivo:** que GitHub le avise a la instancia de Jenkins cuando se hace push, en vez de que Jenkins pregunte cada minuto.

## 1. El problema

El Jenkins local está en `localhost`. GitHub no puede llegar ahí. Se necesita un túnel: un programa que da una URL pública en Internet y redirige todo lo que llega al contenedor de Jenkins.

## 2. Configuración del token de ngrok

Volver a la carpeta `00-setup` del repo de la clase y crear el archivo `.env` a partir del ejemplo.

### Linux / macOS

```bash
cd jenkins-lab/jenkins/00-setup
cp .env.example .env
```

### Windows (PowerShell)

```powershell
cd jenkins-lab\jenkins\00-setup
Copy-Item .env.example .env
```

Abrir `.env` con un editor y pegar el token de ngrok (se consigue en https://dashboard.ngrok.com/get-started/your-authtoken). Sin comillas:

```
NGROK_AUTHTOKEN=<token>
```

## 3. Levantar el túnel

Mismo comando en todos los sistemas:

```bash
docker compose --profile ngrok up -d
```

Abrir http://localhost:4040. Ahí se ve la URL pública, algo como `https://a1b2-190-64-1-1.ngrok-free.app`. Copiarla.

Si se abre esa URL en el navegador, ngrok muestra una advertencia antes de dejar pasar. Es normal en la versión gratuita y no afecta a los webhooks.

### Si no se tiene cuenta de ngrok

Usar el otro túnel, que no pide cuenta:

```bash
docker compose --profile cloudflared up -d
docker compose logs cloudflared
```

En los logs aparece una URL `https://....trycloudflare.com`. Esa es la URL pública. Cambia cada vez que se reinicia el contenedor.

## 4. Creación del webhook en GitHub

1. En el repositorio propio: **Settings > Webhooks > Add webhook**.
2. **Payload URL:** la URL pública más `/github-webhook/`. Con la barra al final. Ejemplo: `https://a1b2-190-64-1-1.ngrok-free.app/github-webhook/`
3. **Content type:** `application/json`.
4. **Which events:** elegir **Let me select individual events** y marcar **Pushes** y **Pull requests**.
5. **Add webhook**.

GitHub manda un evento `ping` enseguida. Entrar al webhook recién creado, pestaña **Recent Deliveries**: debe haber un ping con tilde verde y respuesta `200`.

## 5. Probar que dispara solo

Primero, desactivar el scan periódico para asegurar que el webhook es el que trabaja:

1. Job `06-libreria-mb` > **Configure** > desmarcar **Periodically if not otherwise run** > **Save**.

Ahora hacer un cambio y push:

```bash
echo "" >> README.md
git commit -am "Probando webhook"
git push
```

Revisar Jenkins: en menos de 10 segundos el job `main` de `06-libreria-mb` arranca. En GitHub, en **Recent Deliveries**, aparece un evento `push` con `200`.

Abrir ese delivery: en **Request** está el JSON que GitHub le mandó a Jenkins (commit, autor, rama). En **Response** lo que Jenkins contestó. Si algo falla, este es el lugar para revisar. El botón **Redeliver** vuelve a mandar el mismo evento.

## 6. Volver a activar el scan

Dejar el scan periódico activado como respaldo: si el túnel se cae, Jenkins igual se entera al minuto.

1. `06-libreria-mb` > **Configure** > marcar **Periodically if not otherwise run**, 1 minute > **Save**.

## 7. Opcional: links correctos desde GitHub

Los checks en el PR tienen un link "Details" que apunta a `http://localhost:8080/...`. Funciona en la máquina local pero no para otra persona. Para arreglarlo: **Manage Jenkins > System > Jenkins URL**, indicar la URL pública. Recordar volver a `http://localhost:8080/` al apagar el túnel.

## Checkpoint

Un push dispara el build sin scan periódico, y Recent Deliveries muestra el evento con 200.
