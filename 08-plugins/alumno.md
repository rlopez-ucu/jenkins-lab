# Módulo 8: Plugins (alumno)

**Objetivo:** instalar plugins, saber dónde se administran, y dejar registro de cuáles están instalados.

Todo en el navegador, salvo el último paso.

## 1. Revisar qué está instalado

1. **Manage Jenkins > Plugins**.
2. Pestaña **Installed plugins**. Buscar `git`. Observar: la versión, y que el botón de desinstalar está deshabilitado porque otros plugins dependen de él.

Todo lo que se usó hasta ahora (Git, Pipeline, GitHub Branch Source, JUnit, Timestamper) es un plugin.

## 2. Instalar Pipeline Graph View

1. Pestaña **Available plugins**. Buscar `graph view`.
2. Marcar **Pipeline: Graph View** y hacer clic en **Install**.
3. Esperar a que todo quede en verde. No pide reinicio.
4. Abrir cualquier build de `06-libreria-mb` > `main`. Ahora tiene **Pipeline Overview** en el menú izquierdo. Es una vista de grafo, más clara que la Stage View cuando hay stages en paralelo. Comparar las dos.

## 3. Instalar Docker Pipeline

1. **Available plugins**, buscar `docker pipeline`.
2. Marcar **Docker Pipeline** y hacer clic en **Install**.
3. Este agrega a los pipelines el objeto `docker` (`docker.build`, `docker.withRegistry`) y la opción `agent { docker { ... } }`. Se usa en los módulos 9 y 10.

## 4. Revisar las actualizaciones

Pestaña **Updates**. Hay plugins con versión nueva. Los que tienen una advertencia en rojo tienen un problema de seguridad conocido. En una empresa, esto se actualiza con criterio: uno por uno, probando, no todo junto un viernes.

## 5. Exportar la lista de plugins

Sirve para reconstruir un Jenkins igual en otra máquina. Ejecutar esto en la terminal:

### Linux / macOS

```bash
curl -s -u <usuario-jenkins>:<contraseña> \
  'http://localhost:8080/pluginManager/api/json?depth=1&tree=plugins[shortName,version]' \
  | python3 -c "import sys, json; [print(p['shortName']) for p in json.load(sys.stdin)['plugins']]"
```

### Windows (PowerShell)

```powershell
$cred = "<usuario-jenkins>:<contraseña>"
$b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($cred))
$r = Invoke-RestMethod -Uri 'http://localhost:8080/pluginManager/api/json?depth=1&tree=plugins[shortName,version]' -Headers @{Authorization = "Basic $b64"}
$r.plugins | ForEach-Object { $_.shortName }
```

Esa lista es el formato de `00-setup/plugins.txt`. Abrir ese archivo y comparar: ahora hay dos más (`pipeline-graph-view` y `docker-workflow`). Si se agregan ahí y se reconstruye la imagen, la próxima vez ya vienen.

## Checkpoint

Dos plugins nuevos instalados, la vista Pipeline Overview funciona, y se sabe cómo exportar la lista.
