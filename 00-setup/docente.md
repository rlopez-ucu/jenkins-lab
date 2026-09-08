# Módulo 0: Intro y levantar Jenkins (docente)

**Tiempo:** 10 min de intro + 20 min de setup. **Hora:** 18:00 a 18:30.

## Conceptos a enseñar

- **Integración continua (CI):** cada cambio que se sube al repo se compila y se prueba solo, sin que nadie lo pida. Lo que se gana: enterarse en minutos de que algo se rompió, no en la semana de la entrega.
- **Entrega/despliegue continuo (CD):** el mismo mecanismo empuja el cambio a un ambiente. En esta clase se llega hasta publicar una imagen Docker.
- **Jenkins:** un servidor que ejecuta jobs. Es viejo (2011, antes Hudson 2005), es open source, tiene miles de plugins, y sigue siendo el más usado en empresas grandes. Alternativas: GitHub Actions, GitLab CI, CircleCI. La diferencia principal: Jenkins lo hospeda la propia organización.
- **Vocabulario que van a ver en la UI:** job (o project), build (una ejecución de un job), workspace (la carpeta donde corre el build), executor (un "carril" de ejecución), node/agent (una máquina que ejecuta builds), plugin.
- **Arquitectura mínima:** un controller (lo que se levanta hoy) que tiene la UI y guarda la config en `/var/jenkins_home`. Puede tener agents (módulo 11). Hoy todo corre en el controller.

## Intro (10 min, sin que nadie toque el teclado)

1. Preguntar: "¿Cómo saben hoy que su código anda antes de entregarlo?" Casi todos van a decir "lo corro yo". Ese es el problema que resuelve CI.
2. Mostrar el cronograma del README. Marcar los tres hitos: freestyle (18:30), Jenkinsfile en el repo (19:40), GitHub disparando builds solos (20:30).
3. Mostrar el Jenkins del docente ya levantado por 30 segundos: dashboard, un job, un build verde. "A esto llegan hoy".
4. Explicar por qué Jenkins corre en Docker: todos la misma versión, se borra con un comando, y los pasos del pipeline son siempre Linux aunque la computadora sea Windows.

## Setup (20 min)

Los alumnos siguen `alumno.md`. El docente hace lo mismo desde cero en el proyector,
en paralelo (borrar el volumen antes: `docker compose down -v`), pero más lento,
y comentando:

- `docker compose up -d`: qué levanta (un contenedor, un volumen, una red). Mostrar `docker compose ps`.
- El **initialAdminPassword**: por qué existe (nadie más que quien tiene acceso al disco puede tomar el control de un Jenkins recién instalado).
- **Install suggested plugins:** explicar que los plugins ya están en la imagen, por eso tarda poco. En una instalación limpia tarda 5 minutos.
- **Primer usuario admin:** que usen un password que se acuerden. Se pierde solo si borran el volumen.
- **Jenkins URL:** dejar `http://localhost:8080/`. Se usa para armar links en mails y webhooks; se cambia en el módulo 7.

## Dónde suelen atascarse

- Windows sin Docker Desktop abierto: `error during connect`. Abrir Docker Desktop y esperar el ícono verde.
- Puerto 8080 ocupado: cambiar `"8080:8080"` por `"8081:8080"` en `docker-compose.yml`. Todo lo demás de la clase sigue igual pero con 8081.
- Linux sin permiso de docker: `permission denied while trying to connect`. Correr `sudo usermod -aG docker $USER` y volver a loguearse, o usar `sudo` en todo.
- Alguien no hizo el prework: que corra `docker compose build` ahora. Tarda 5 a 15 min. Que siga los pasos en la pantalla de un compañero mientras tanto.
- La página muestra "Jenkins is getting ready to work": esperar 30 a 60 segundos y refrescar.

## Checkpoint (18:30)

Todos ven el dashboard de Jenkins vacío con el mensaje "Welcome to Jenkins!" y su usuario arriba a la derecha. Pedir que levanten la mano quienes no llegaron y asignarles un compañero.
