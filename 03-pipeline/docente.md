# Módulo 3: Pipeline declarativo escrito en la UI (docente)

**Tiempo:** 20 min. **Hora:** 18:55 a 19:15. Después viene la pausa.

## Conceptos a enseñar

- **Pipeline:** un job cuya definición es código (Groovy) en vez de formularios. El código se llama **Jenkinsfile**. En este módulo se escribe en la UI; en el módulo 4 se mueve al repo.
- **Declarativo vs scripted:** el declarativo tiene una estructura fija (`pipeline { agent, stages, post }`) y es el que se usa en el curso. El scripted es Groovy libre (`node { ... }`); los alumnos lo van a ver en pipelines viejos. Mencionarlo y seguir.
- **Bloques del declarativo:**
  - `agent`: dónde corre. `any` = cualquier executor disponible.
  - `environment`: variables para todo el pipeline.
  - `stages` > `stage` > `steps`: la secuencia. Cada stage es una columna en la vista.
  - `post`: qué hacer al final, según el resultado: `always`, `success`, `failure`, `unstable`, `changed`.
- **Steps básicos:** `echo`, `sh`, `sh(returnStdout: true)`. Y que `sh` con triple comilla acepta varias líneas.
- **Snippet Generator:** la herramienta para descubrir la sintaxis de cualquier step. Enseñar a usarla vale más que memorizar.
- **Replay:** re-ejecutar un build editando el script sin tocar la config. Ideal para probar.

## Qué mostrar

1. Crear el job Pipeline con el script v1 (tres stages). Correr. Abrir el build: la **Stage View** muestra columnas por stage con tiempos. Comparar con el freestyle: "antes era una lista de comandos, ahora tiene estructura y Jenkins entiende dónde falló".
2. Hacer fallar el stage Test (cambiar el `exit 0` por `exit 1`). Correr. Mostrar: el stage Test rojo, Deploy no corrió, y `post { failure }` sí. "Esto es lo que va a mandar el mensaje a Slack en la vida real".
3. Abrir **Pipeline Syntax** (link en el job). Elegir `archiveArtifacts` en el Snippet Generator, completar los campos, **Generate**. Pegar el resultado en el script. "Así descubren cualquier step sin googlear".
4. Usar **Replay** para probar un cambio sin guardar.

## Explicación de la sintaxis del `sh`

- `sh 'comando'`: comilla simple, Groovy no interpola. `$VAR` lo resuelve el shell.
- `sh "comando ${VAR}"`: comilla doble, Groovy interpola antes. Sirve para variables de Groovy (`env.X`, `params.X`).
- Regla práctica: comilla simple salvo que se necesite algo de Groovy. Evita problemas con secretos (módulo 9).

## Dónde suelen atascarse

- Los alumnos olvidan una llave. El error dice `expecting '}'` con línea. Indicarles que cuenten las llaves.
- Escriben `stage('Test')` sin `steps { }` adentro. En declarativo, `steps` es obligatorio.
- El job no muestra la Stage View hasta que corre el primer build.
- Copian el script desde un PDF con comillas "inteligentes". Indicarles que lo copien de `alumno.md`.

## Checkpoint (19:15)

Job `03-pipeline-ui` con un build verde de 3 stages, uno rojo donde Deploy se saltó, y un artefacto agregado con el Snippet Generator.

**Pausa 10 min.**
