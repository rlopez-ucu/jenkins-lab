# Antes de la clase (alumno)

Estos pasos se realizan en casa. Llevan 20 a 30 minutos y descargan varios GB. Quien
llegue a la clase sin completarlos perderá los primeros 40 minutos descargando.

## 1. Cuentas

- [ ] Cuenta en [GitHub](https://github.com/signup). Si ya se dispone de una, no hace falta crear otra.
- [ ] Cuenta gratuita en [ngrok](https://dashboard.ngrok.com/signup). Se usa para que GitHub pueda avisar a la instancia de Jenkins local cuando se hace push.
- [ ] Cuenta gratuita en [Docker Hub](https://hub.docker.com/signup). Se usa para subir una imagen.

## 2. Herramientas

### Linux (Ubuntu / Debian)

```bash
# Docker Engine + Compose plugin
sudo apt-get update
sudo apt-get install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Usar docker sin sudo (cerrar y abrir la sesión después)
sudo usermod -aG docker $USER
```

Otras distros: seguir https://docs.docker.com/engine/install/

### Windows 10/11

1. Instalar [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/). Aceptar la opción WSL 2 cuando la ofrezca. Reiniciar si lo solicita.
2. Instalar Git: abrir PowerShell y ejecutar:

```powershell
winget install --id Git.Git -e
```

3. Cerrar y abrir PowerShell de nuevo para que `git` quede en el PATH.

En clase se usa **PowerShell** (no CMD, no Git Bash). Los comandos de la guía
para Windows están pensados para PowerShell.

### macOS

```bash
brew install --cask docker
brew install git
```

Abrir Docker Desktop una vez para que termine de instalarse.

## 3. Configurar git

Todos los sistemas:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Solo Windows (evita que Windows cambie los finales de línea y rompa scripts en Linux):

```powershell
git config --global core.autocrlf input
```

## 4. Verificar

```bash
docker --version
docker compose version
docker run --rm hello-world
git --version
```

Los cuatro comandos tienen que responder sin error. En Windows, Docker Desktop
tiene que estar abierto (ícono de la ballena en la barra de tareas).

## 5. Descargar la imagen de Jenkins (lo más pesado)

Clonar el repositorio de la clase y construir la imagen. Esto baja unos 1.5 GB y tarda
entre 5 y 15 minutos según la conexión.

### Linux / macOS

```bash
git clone https://github.com/<ORG_O_USUARIO>/<REPO_DE_LA_CLASE>.git
cd <REPO_DE_LA_CLASE>/jenkins/00-setup
docker compose build
```

### Windows (PowerShell)

```powershell
git clone https://github.com/<ORG_O_USUARIO>/<REPO_DE_LA_CLASE>.git
cd <REPO_DE_LA_CLASE>\jenkins\00-setup
docker compose build
```

Si termina con `exit code 0` y aparece algo como `ucu-devops/jenkins:lts` en
`docker images`, el prework está completo. No levantar Jenkins todavía: eso se hace en clase.

## 6. Token de ngrok

Entrar a https://dashboard.ngrok.com/get-started/your-authtoken, copiar el token y
guardarlo en un lugar a mano. Se pegará en un archivo en el módulo 7.
