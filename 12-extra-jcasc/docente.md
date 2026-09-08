# Módulo 12 (extra): Jenkins como código con JCasC (docente)

**Tiempo:** 15 min.

## Conceptos a enseñar

- **El problema:** todo lo que se configuró hoy (usuario, credenciales, jobs) vive en el volumen. Si se pierde, se rehace a mano. Nadie sabe qué cambió ni cuándo.
- **Configuration as Code (JCasC):** un YAML que describe la configuración de Jenkins. Al arrancar, Jenkins lo aplica. Mismo principio que Terraform o los manifests de Kubernetes: el estado deseado está en un archivo versionado.
- **Qué cubre:** seguridad, usuarios, credenciales (con variables de entorno para los secretos), nodos, configuración de plugins, y hasta jobs (con el plugin Job DSL, que no se instala hoy).
- **Skip del wizard:** `-Djenkins.install.runSetupWizard=false`. Con JCasC no hace falta.
- **La combinación completa:** Dockerfile (versión + plugins) + JCasC (configuración) + Jenkinsfile en cada repo (pipelines) = un Jenkins reconstruible desde cero.

## Qué mostrar

1. Abrir `00-setup/casc/jenkins.yaml` y `docker-compose.casc.yml`. Explicar cada línea.
2. **Aviso:** el siguiente paso borra el volumen. Los alumnos que quieran conservar su Jenkins de hoy deben saltarlo o exportarlo primero (`docker run --rm -v jenkins_home:/data -v $PWD:/backup alpine tar czf /backup/jenkins_home.tgz /data`).
3. `docker compose down -v` y levantar con los dos archivos de compose. Sin wizard, login con `admin`/`admin123`, mensaje del sistema visible.
4. Manage Jenkins > Configuration as Code: mostrar **View Configuration** (el YAML efectivo, sirve para copiar la sintaxis de cualquier cosa que se configuró en la UI) y **Reload existing configuration**.
5. Agregar la credencial de GitHub al YAML con una variable de entorno (ejemplo en `alumno.md`). Reload. Aparece en Credentials.

## Dónde suelen atascarse

- Indentación del YAML.
- El secreto pasado como `${VAR}` sin definir la variable en compose: JCasC falla al arrancar con un mensaje claro en los logs.
- Después de `down -v` no aparece nada de lo de hoy. Es lo esperado; el docente ya lo avisó.

## Checkpoint

Jenkins levantado sin wizard desde el YAML, y una credencial agregada por código.
