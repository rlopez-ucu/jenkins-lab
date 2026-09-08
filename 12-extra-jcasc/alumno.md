# Módulo 12 (extra): Jenkins como código con JCasC (alumno)

**Objetivo:** levantar un Jenkins ya configurado desde un archivo YAML, sin wizard, y agregar una credencial por código.

**Aviso:** este módulo borra el Jenkins actual (volumen incluido). Para conservarlo, hacer un backup primero:

```bash
docker run --rm -v jenkins_home:/data -v "$PWD:/backup" alpine tar czf /backup/jenkins_home.tgz /data
```

(En PowerShell usar `${PWD}` en vez de `$PWD`.)

## 1. Revisar los archivos

En `00-setup`:

- `docker-compose.casc.yml`: agrega variables de entorno y monta la carpeta `casc`. `runSetupWizard=false` salta el wizard.
- `casc/jenkins.yaml`: la configuración. Un usuario admin, 2 executors, mensaje del sistema, URL.

## 2. Levantar Jenkins desde código

Mismos comandos en todos los sistemas, desde `00-setup`:

```bash
docker compose --profile ngrok down -v
docker compose -f docker-compose.yml -f docker-compose.casc.yml up -d
```

Esperar un minuto y abrir http://localhost:8080. No hay wizard. Entrar con `admin` / `admin123`. Arriba aparece el mensaje del sistema definido en el YAML.

## 3. Revisar la configuración efectiva

**Manage Jenkins > Configuration as Code**. Hacer clic en **View Configuration**: es el YAML completo de la instancia de Jenkins, incluso lo que no se escribió. Para saber cómo se escribe algo en YAML, configurarlo en la UI y revisarlo aquí.

## 4. Agregar una credencial por código

Editar `casc/jenkins.yaml` y agregar al final:

```yaml
credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              scope: GLOBAL
              id: github-pat
              username: "<usuario-github>"
              password: "${GITHUB_PAT}"
              description: "PAT de GitHub (desde JCasC)"
```

Editar `docker-compose.casc.yml` y agregar bajo `environment`:

```yaml
      GITHUB_PAT: ${GITHUB_PAT:-}
```

Y en el `.env` propio agregar una línea con el token propio:

```
GITHUB_PAT=github_pat_...
```

El secreto no va en el YAML: va en una variable de entorno que el YAML referencia. El YAML se puede subir a git; el `.env` no.

Aplicar:

```bash
docker compose -f docker-compose.yml -f docker-compose.casc.yml up -d
```

En Jenkins, **Manage Jenkins > Configuration as Code > Reload existing configuration**. Ir a **Credentials**: está `github-pat`.

## 5. Para entender

Con Dockerfile (versión y plugins) + `jenkins.yaml` (configuración) + Jenkinsfile en cada repo (pipelines), un Jenkins entero se reconstruye desde cero con un comando. Es lo mismo que se vio con IaC, aplicado al servidor de CI.

## Checkpoint

Jenkins levantado sin wizard, con usuario y credencial definidos en YAML.
