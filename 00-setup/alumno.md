# Módulo 0: Levantar Jenkins (alumno)

**Objetivo:** tener Jenkins corriendo en http://localhost:8080 con el usuario propio creado.

## 1. Abrir una terminal en la carpeta de setup

### Linux / macOS

```bash
cd <REPO_DE_LA_CLASE>/jenkins/00-setup
```

### Windows (PowerShell)

```powershell
cd <REPO_DE_LA_CLASE>\jenkins\00-setup
```

Verificar que Docker esté andando (en Windows y macOS, Docker Desktop tiene que estar abierto):

```bash
docker info
```

## 2. Levantar Jenkins

Mismo comando en todos los sistemas:

```bash
docker compose up -d
```

Si en el prework no se construyó la imagen, este comando la construye ahora (tarda varios minutos).

Revisar qué se levantó:

```bash
docker compose ps
```

Debe verse un contenedor `jenkins` con estado `running`.

## 3. Obtener la contraseña inicial

Jenkins genera una contraseña al arrancar y la guarda en un archivo dentro del contenedor.

### Linux / macOS

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Windows (PowerShell)

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Es el mismo comando: `cat` se ejecuta adentro del contenedor, que es Linux. Copiar el texto que aparece (32 caracteres).

Si indica `No such file or directory`, Jenkins todavía está arrancando. Esperar 30 segundos y volver a probar. Se puede seguir el arranque con `docker compose logs -f jenkins` (se sale con Ctrl+C).

## 4. Completar el wizard

1. Abrir http://localhost:8080 en el navegador.
2. Pegar la contraseña en **Administrator password** y hacer clic en **Continue**.
3. Elegir **Install suggested plugins**. Como ya vienen en la imagen, tarda menos de un minuto.
4. **Create First Admin User:** indicar un usuario y una contraseña fáciles de recordar. Completar los otros campos con cualquier cosa válida. Clic en **Save and Continue**.
5. **Instance Configuration:** dejar `http://localhost:8080/` y clic en **Save and Finish**.
6. Clic en **Start using Jenkins**.

## 5. Checkpoint

Debe verse el dashboard con el texto "Welcome to Jenkins!" y el usuario propio arriba a la derecha.

## Comandos útiles para el resto de la clase

```bash
docker compose ps              # ver estado
docker compose logs -f jenkins # ver logs (Ctrl+C para salir)
docker compose restart jenkins # reiniciar Jenkins sin perder nada
docker compose down            # apagar (la config queda en el volumen)
docker compose down -v         # apagar Y BORRAR TODO (volver a cero)
```
