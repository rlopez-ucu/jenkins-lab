# Módulo 5: Parámetros, `when` y aprobación manual en pipeline (docente)

**Tiempo:** 15 min. **Hora:** 19:40 a 19:55.

## Conceptos a enseñar

- **`parameters { }`:** lo mismo que "This project is parameterized" del módulo 2, pero en código. Tipos: `string`, `choice`, `booleanParam`, `password`, `text`.
- **`params.X`:** cómo se leen en Groovy. En `sh` también están como `$X` (variable de entorno).
- **`when { }`:** condición para que un stage corra. Si no se cumple, el stage se salta (gris) y el pipeline sigue. Condiciones útiles: `expression { }`, `branch 'main'`, `changeRequest()`, `environment name: 'X', value: 'y'`, `not { }`, `allOf { }`.
- **`input`:** pausa el pipeline y espera que alguien apruebe en la UI. Es el "botón de deploy a prod". Tiene timeout opcional y se puede restringir a ciertos usuarios (`submitter`).
- **Un detalle importante:** la primera vez que corre un Jenkinsfile con `parameters`, Jenkins recién ahí se entera de que hay parámetros. Ese primer build corre con valores default y **después** aparece "Build with Parameters". Es una fuente clásica de confusión. Además, en ese primer build `params.X` tiene el default pero `$X` en `sh` está vacío: las variables de entorno solo existen si el build se lanzó con parámetros. El Jenkinsfile del módulo imprime las dos formas a propósito para que los alumnos lo vean.
- **Ocupa un executor mientras espera:** `input` dentro de `agent any` bloquea un executor hasta que alguien aprueba. Mencionar que la solución es `agent none` arriba y `agent any` por stage. Está en el Jenkinsfile del módulo como comentario.

## Qué mostrar

1. Agregar el bloque `parameters` y los stages `Aprobación` y `Deploy` al Jenkinsfile. Push. Build Now. Explicar por qué este build no pidió parámetros.
2. Segundo build: **Build with Parameters** con `ENTORNO=dev`. Aprobación se salta (gris), Deploy corre.
3. Tercer build: `ENTORNO=prod`. El pipeline se queda esperando en Aprobación. Mostrar dónde aparece el botón: en la Stage View aparece un cuadro con **Proceed / Abort**, y también en el console output hay un link. Aprobar. Sigue.
4. Cuarto build: `prod` con `EJECUTAR_TESTS` desmarcado. Test se salta. "Esto es útil para hotfixes... y peligroso. Por eso en la vida real se combina con `when { branch 'main' }`".

## Dónde suelen atascarse

- No aparece "Build with Parameters": los alumnos no corrieron el primer build después del push. Hacer Build Now una vez.
- `input` no muestra el botón: están mirando la página del job y no del build. Pedirles que entren al build en curso; el prompt aparece en la Stage View y en Console Output.
- Error `No such DSL method 'choice'`: escribieron `choice` fuera del bloque `parameters`.

## Checkpoint (19:55)

Cuatro builds del job `04-libreria-scm`: uno sin parámetros, uno a dev sin aprobación, uno a prod aprobado a mano, uno sin tests.
