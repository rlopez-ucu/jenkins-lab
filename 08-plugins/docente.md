# Módulo 8: Plugins (docente)

**Tiempo:** 10 min. **Hora:** 20:30 a 20:40.

## Conceptos a enseñar

- **Jenkins es un núcleo chico más plugins.** Git, pipeline, GitHub, JUnit: todo lo que usaron es un plugin. El "suggested" del wizard son unos 20. Hay más de 1800 en total.
- **Update Center:** el catálogo. Manage Jenkins > Plugins. Pestañas: Updates, Available, Installed, Advanced.
- **Dependencias:** instalar uno arrastra otros. Desinstalar puede romper jobs que lo usan.
- **Reinicio:** algunos plugins piden reiniciar. La opción "Restart Jenkins when installation is complete and no jobs are running" hace eso.
- **Reproducibilidad:** la lista de plugins de una instalación se puede exportar y meter en `plugins.txt` para construir la imagen (es lo que se hizo en el Dockerfile). Enlazar con IaC: "el servidor de CI también es código".
- **Criterio para elegir plugins:** fecha del último release, cantidad de instalaciones, si tiene advertencias de seguridad (Jenkins las marca en rojo en la lista).

## Qué mostrar

1. Manage Jenkins > Plugins > Installed. Buscar `git`. Mostrar qué versión, y que no se puede desinstalar porque otros dependen de él.
2. Available: buscar `Pipeline: Graph View`. Instalarlo con "Install" (sin reinicio). Abrir un build viejo: ahora tiene **Pipeline Overview** con el grafo. Compararlo con la Stage View.
3. Instalar `Docker Pipeline` (id `docker-workflow`). Se usa en el módulo 10 (extra) y su API `docker.withRegistry` es opción en el 9.
4. Pestaña Updates: mostrar que hay actualizaciones disponibles y explicar por qué en producción no se aprietan todas juntas un viernes.
5. Abrir `00-setup/plugins.txt` y mostrar cómo se listan. Comando para exportar la lista de una instalación viva (está en `alumno.md`).

## Dónde suelen atascarse

- No aparece "Pipeline Overview" después de instalar: refrescar la página del build.
- La búsqueda en Available no encuentra: escribir menos letras (`graph` en vez de `pipeline graph view`).
- Instalan y marcan reinicio, y el reinicio tarda 1 minuto: que esperen; `docker compose logs -f jenkins` para ver.

## Checkpoint (20:40)

Pipeline Graph View y Docker Pipeline instalados, y los builds muestran la vista de grafo.
