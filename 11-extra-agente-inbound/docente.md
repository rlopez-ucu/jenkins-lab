# Módulo 11 (extra): Agente inbound en otro contenedor (docente)

**Tiempo:** 15 min.

## Conceptos a enseñar

- **Controller y agents:** el controller tiene la UI y coordina; los agents ejecutan. En producción el controller no corre builds (0 executors) y hay varios agents con distintas capacidades.
- **Inbound agent:** el agent se conecta AL controller (no al revés). Sirve cuando el agent está detrás de un firewall o NAT. Usa el puerto 50000 que se expuso en compose. El otro tipo es SSH: el controller se conecta al agent.
- **Labels:** etiquetas que describen al agent (`linux`, `docker`, `python`, `gpu`). El pipeline pide `agent { label 'python' }` y Jenkins elige un agent que la tenga.
- **Secret del agent:** cada nodo tiene un secreto que el agent presenta al conectarse. Es la credencial del nodo.

## Qué mostrar

1. Manage Jenkins > Nodes > New Node. Nombre `agente-1`, Permanent Agent. Remote root `/home/jenkins/agent`, Labels `linux worker`, Launch method `Launch agent by connecting it to the controller`. Save.
2. Abrir el nodo: muestra el comando con el secret. Copiar el secret.
3. Levantar el agent como contenedor en la red `jenkins_net` (comando en `alumno.md`). Refrescar Nodes: `agente-1` conectado.
4. Pipeline de prueba con `agent { label 'worker' }` que imprime `hostname` y `NODE_NAME`. Correr el build. Mostrar el hostname del contenedor del agent.
5. Poner el controller en 0 executors (Manage Jenkins > Nodes > Built-In Node > Configure). Correr el job multibranch: queda en cola "waiting for next available executor" porque el agent no tiene Python ni Docker. Volver a 2. "Por eso los labels importan".

## Dónde suelen atascarse

- El agent dice `Connection refused`: la URL debe ser `http://jenkins:8080` (nombre del contenedor en la red), no `localhost`.
- `--network jenkins_net` faltante.
- Los alumnos copian el secret con espacios al final.
- Windows PowerShell: los saltos de línea de comando largo se hacen con `` ` `` (backtick), no con `\`. El comando de `alumno.md` está en una línea para evitar el problema.

## Checkpoint

Nodo `agente-1` conectado y un build que corrió ahí, con el hostname del agent en el log.
