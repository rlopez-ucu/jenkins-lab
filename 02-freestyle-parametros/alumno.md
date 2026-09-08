# Módulo 2: Job freestyle con parámetros (alumno)

**Objetivo:** que quien lanza el build elija valores en un formulario, y usar esos valores dentro del build.

Todo en el navegador.

## 1. Creación del job

1. **New Item**, nombre `02-parametros`, tipo **Freestyle project**, **OK**.
2. Marcar la casilla **This project is parameterized**.
3. **Add Parameter > String Parameter**:
   - Name: `NOMBRE`
   - Default Value: `mundo`
   - Description: `A quién saludamos`
4. **Add Parameter > Choice Parameter**:
   - Name: `ENTORNO`
   - Choices (una por línea):
     ```
     dev
     qa
     prod
     ```
   - Description: `Ambiente destino`
5. **Add Parameter > Boolean Parameter**:
   - Name: `VERBOSE`
   - Default Value: desmarcado
   - Description: `Mostrar todas las variables de entorno`
6. En **Build Steps > Add build step > Execute shell** pegar:

```bash
echo "Hola, $NOMBRE"
echo "Vamos a desplegar al ambiente: $ENTORNO"

if [ "$ENTORNO" = "prod" ]; then
  echo "CUIDADO: esto es produccion"
fi

if [ "$VERBOSE" = "true" ]; then
  echo "--- variables de entorno ---"
  env | sort
fi
```

7. **Save**.

## 2. Ejecución de dos builds distintos

Observar que el botón ya no dice "Build Now": dice **Build with Parameters**.

1. Hacer clic en **Build with Parameters**. Dejar los valores por defecto. **Build**.
2. Otra vez **Build with Parameters**. Indicar en `NOMBRE` el nombre del alumno, en `ENTORNO` el valor `prod`, y marcar `VERBOSE`. **Build**.
3. Abrir el Console Output de cada build y comparar.
4. En la página de cada build hay un link **Parameters** a la izquierda. Ahí queda registrado con qué valores corrió. Eso resulta útil cuando alguien pregunta "¿qué versión mandaron a prod el martes?".

## 3. Cómo llegan los parámetros

Los parámetros son **variables de entorno** dentro del build. Por eso se usan como `$NOMBRE` en el shell. Al activar `VERBOSE`, aparecen en la lista junto con `BUILD_NUMBER` y las demás.

El Boolean llega como el texto `true` o `false`. Por eso el `if` compara con `"true"`.

## Checkpoint

Dos builds con parámetros distintos, y se sabe dónde ver con qué parámetros corrió cada uno.
