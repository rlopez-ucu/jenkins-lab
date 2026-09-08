# Módulo 11 (extra): Agente inbound en otro contenedor (alumno)

**Objetivo:** conectar un segundo contenedor como agente de Jenkins y mandar un build a que corra ahí usando labels.

## 1. Crear el nodo en Jenkins

1. **Manage Jenkins > Nodes > New Node**.
2. Node name: `agente-1`. Type: **Permanent Agent**. **Create**.
3. Completar:
   - Remote root directory: `/home/jenkins/agent`
   - Labels: `linux worker`
   - Launch method: **Launch agent by connecting it to the controller**
4. **Save**.
5. Entrar al nodo `agente-1`. Muestra un comando con `-secret <valor>`. Copiar solo el valor del secret.

## 2. Levantar el agente

Es un contenedor con la imagen oficial `jenkins/inbound-agent`, en la misma red que Jenkins. Reemplazar `<SECRET>`.

### Linux / macOS

```bash
docker run -d --name agente-1 --network jenkins_net --init jenkins/inbound-agent:latest -url http://jenkins:8080 -secret <SECRET> -name agente-1 -workDir /home/jenkins/agent
```

### Windows (PowerShell)

```powershell
docker run -d --name agente-1 --network jenkins_net --init jenkins/inbound-agent:latest -url http://jenkins:8080 -secret <SECRET> -name agente-1 -workDir /home/jenkins/agent
```

Es el mismo comando. La URL es `http://jenkins:8080` porque el agente le habla a Jenkins por la red interna de Docker, donde el contenedor se llama `jenkins`.

Verificar: **Manage Jenkins > Nodes**. `agente-1` aparece conectado (sin la X roja). Si no, revisar `docker logs agente-1`.

## 3. Enviar un build al agente

Crear un job Pipeline `11-en-agente` con este script:

```groovy
pipeline {
    agent {
        label 'worker'
    }

    stages {
        stage('Donde estoy') {
            steps {
                echo "Corriendo en el nodo: ${env.NODE_NAME}"
                sh 'hostname'
                sh 'whoami'
                sh 'java -version'
            }
        }
    }
}
```

**Build Now**. El `hostname` es el ID del contenedor `agente-1`, y `NODE_NAME` es `agente-1`.

Cambiar el label a `worker2` y correr el build: queda en cola con "There are no nodes with the label 'worker2'". Jenkins espera a que aparezca un agente con esa label. Cancelar el build.

## 4. Para entender

- Este agente no tiene Python ni Docker. Si se envía el pipeline de `libreria-api` con `label 'worker'`, falla. Los labels sirven para que cada job vaya a un agente con lo que necesita.
- En producción, el controller suele tener 0 executors (Manage Jenkins > Nodes > Built-In Node > Configure > Number of executors) y todo corre en agentes.

## 5. Limpieza

```bash
docker rm -f agente-1
```

Y en Jenkins, borrar el nodo o dejarlo desconectado.

## Checkpoint

Un build corrió en `agente-1` y se entiende qué pasa cuando ningún agente tiene la label pedida.
