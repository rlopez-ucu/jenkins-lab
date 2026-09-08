# Módulo 2: Job freestyle con parámetros (docente)

**Tiempo:** 10 min. **Hora:** 18:45 a 18:55.

## Conceptos a enseñar

- **Parámetro de build:** un valor que quien lanza el build elige en un formulario. El job deja de ser "siempre lo mismo" y pasa a ser "una operación que se ejecuta con datos": desplegar a QA o a prod, con la versión 1.2 o la 1.3, con o sin tests.
- **Tipos:** String, Choice, Boolean, Password, File. En este módulo se usan los tres primeros.
- **Cómo llegan al build:** como variables de entorno. `$ENTORNO` en el shell. Esto es igual en freestyle y en pipeline.
- **"Build Now" pasa a ser "Build with Parameters".** Cambia el botón. Y el build muestra con qué parámetros corrió (link "Parameters" en la página del build). Eso es trazabilidad: dentro de un mes se sabe qué versión se mandó a prod y quién apretó el botón.

## Qué mostrar

El docente configura el job junto con los alumnos. Al llegar a **This project is parameterized**, explicar cada campo del formulario a medida que se completa: Name es el nombre de la variable, Default es lo que aparece precargado, Description es lo que ve el usuario.

Correr dos builds: uno con `ENTORNO=dev` y `VERBOSE` desmarcado, otro con `prod` y `VERBOSE` marcado. Comparar los console outputs y mostrar la página **Parameters** de cada build.

## Idea para conectar con lo que viene

"El parámetro `ENTORNO=prod` hoy solo imprime. En el módulo 5 vamos a hacer que si es prod, el pipeline se frene y pida aprobación."

## Dónde suelen atascarse

- Los alumnos ponen espacios o minúsculas en el Name del parámetro. Funciona, pero después en shell `$mi param` no funciona. Convención: MAYÚSCULAS_CON_GUION_BAJO.
- En Choice, las opciones van una por línea, no separadas por coma.
- El Boolean llega como el texto `true` o `false`, no como 1/0. Por eso el `if` compara con `"true"`.

## Checkpoint (18:55)

Un job `02-parametros` con dos builds cuyos parámetros difieren, visibles en la página de cada build.
