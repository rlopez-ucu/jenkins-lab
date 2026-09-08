# Módulo 6: Credenciales de GitHub y pipeline multibranch (docente)

**Tiempo:** 20 min. **Hora:** 19:55 a 20:15. Es el módulo más denso; no se debe recortar.

## Conceptos a enseñar

- **Credenciales en Jenkins:** un almacén cifrado de secretos con un ID. Los jobs referencian el ID, nunca el secreto. Tipos que se usan hoy: Username with password (para el PAT de GitHub), Secret text, SSH key. Jenkins enmascara el valor en los logs.
- **PAT (personal access token) de GitHub:** un token con permisos acotados que reemplaza la contraseña. Fine-grained: permisos por repo. Classic: por scopes. Para la clase, fine-grained con Contents (read), Pull requests (read), Commit statuses (read and write), Metadata (read).
- **Multibranch pipeline:** en vez de un job apuntando a una rama, un job "padre" que escanea el repo y crea un sub-job por cada rama y cada PR que tenga Jenkinsfile. Rama nueva = job nuevo, rama borrada = job borrado. Es lo que se usa en la práctica.
- **GitHub Branch Source:** el plugin que hace ese escaneo usando la API de GitHub (no solo git). Por eso ve PRs y puede publicar **commit statuses**: el check verde o rojo al lado del commit y en el PR.
- **Variables nuevas:** `BRANCH_NAME`, `CHANGE_ID` (número de PR), `CHANGE_TARGET`. Y las condiciones `when { branch 'main' }` y `when { changeRequest() }`.
- **El flujo real de equipo:** rama feature → PR → CI corre y publica status → alguien revisa → merge → CI corre en main y despliega. Hoy los alumnos lo hacen entero, solos, con su propio repo.

## Qué mostrar

1. El docente crea el PAT en vivo. Mostrar la pantalla de permisos y explicar cada uno de los cuatro. Copiarlo y decir en voz alta "esto no se pega en un chat ni en un Jenkinsfile".
2. Cargarlo en Jenkins: Manage Jenkins > Credentials > System > Global > Add. Tipo Username with password, ID `github-pat`. Explicar que el ID es lo que se escribe en los jobs.
3. Crear el multibranch. Mostrar **Behaviours**: Discover branches (all), Discover pull requests from origin (merging the PR with the target). Guardar y revisar el **Scan Repository Log**: encontró `main` y creó un job.
4. Cambiar el Jenkinsfile: agregar el stage Deploy con `when { branch 'main' }` y el stage `Info` que imprime `BRANCH_NAME` y `CHANGE_ID`. Push a main. Mostrar que el job de main corrió solo (por el scan periódico) o forzarlo con **Scan Repository Now**.
5. Crear una rama `feature/saludo`, cambiar algo (el mensaje de `/health`) y su test, push, abrir un PR en GitHub. **Scan Repository Now**. Mostrar: apareció un job para la rama y otro para el PR (`PR-1`). Abrir el PR en GitHub: abajo está el check de Jenkins con link al build. Deploy no corrió (no es main).
6. Hacer merge del PR. Scan. El job de main corre con Deploy. Los jobs de la rama y el PR desaparecen en el próximo scan (o quedan marcados para borrar).

## Sobre el scan periódico

Activar **Scan Repository Triggers > Periodically if not otherwise run: 1 minute**. Esto hace que todo funcione aunque el webhook del módulo 7 falle. En el módulo 7 se desactiva para demostrar el webhook, y después se vuelve a activar como red de seguridad.

## Dónde suelen atascarse

- El PAT fine-grained no tiene el repo seleccionado ("Only select repositories" sin elegir ninguno). El scan dice `Not Found`.
- Olvidan Commit statuses: el build corre pero no aparece el check en GitHub.
- Ponen el PAT como "Secret text" en vez de "Username with password". GitHub Branch Source necesita el segundo.
- La URL del repo en el multibranch: es la HTTPS sin `.git` (con `.git` también anda, pero el plugin la normaliza y a veces confunde).
- El PR no aparece: el scan no corrió todavía. **Scan Repository Now**.
- `git push` de la rama nueva pide `--set-upstream`. Que usen `git push -u origin feature/saludo`.

## Checkpoint (20:15)

Job multibranch `06-libreria-mb` con sub-jobs para `main` y al menos un PR (o su rama ya mergeada), y un check de Jenkins visible en un PR de GitHub.
