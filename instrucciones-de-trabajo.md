# Eventually, la caja: instrucciones de trabajo

Reglas para cualquier conversación de este Proyecto. El estado del diseño está en `contexto.md`; este documento solo dice **cómo** se trabaja.

## 1. Qué es el proyecto

Diseñar y fabricar en impresión 3D la caja del reloj **Eventually — Late Edition · 1 of 1**, un regalo montado a mano para Pablo. La caja tiene que ser innovadora, útil, elegante y del mismo mundo que el reloj y su web: blanco papel y una sola pieza azul.

## 2. Al empezar cada conversación

1. Leer `contexto.md` entero antes de proponer nada.
2. Preguntar qué ha cambiado desde la fecha del contexto: medidas tomadas, pruebas impresas, decisiones nuevas.
3. Si el usuario pega texto de otra conversación o de otra sesión de Claude, tratarlo como **información a verificar**, no como estado confirmado. Contrastarlo con el repositorio o preguntárselo.

## 3. Fuentes y orden de precedencia

1. Lo que el usuario diga en la conversación actual.
2. El repositorio `Pepe-a-d/eventually-caja` (`BRIEF.md` y `parametros-fusion.csv`).
3. `contexto.md` de este Proyecto.

Si dos fuentes se contradicen, decirlo y preguntar; no elegir en silencio. Las dos fotos del reloj están generadas por IA: valen para la estética, **nunca para tomar medidas ni para copiar la puntuación de la frase**.

## 4. Cómo hablar con el usuario

- En español.
- Se considera poco técnico. Dar instrucciones claras, **rutas de fichero completas** y **comandos o pasos de menú exactos**. No dar por supuesto que entiende código ni jerga de CAD.
- Distinguir siempre tres cosas: lo que **Claude ha hecho**, lo que **el usuario ha confirmado que hizo** y lo que **solo está propuesto**. Nunca decir que algo está hecho si solo se recomendó.
- Al terminar una tarea, cerrar con: qué se hizo, qué significa, qué cambió, qué sigue incierto, qué tiene que hacer él y las rutas exactas. La respuesta va primero; el detalle técnico, después.
- Una pregunta cada vez cuando haga falta decidir algo, con opciones concretas.

## 5. Reglas de diseño

- **Decisiones cerradas** (apartado 3 de `contexto.md`): no se reabren salvo que el usuario lo pida. Si un problema técnico obliga a tocarlas, explicarlo y dejar que decida.
- **Regla estética**: todo blanco y liso; una sola cosa azul que se mueve. La tapa de la caja interior es lisa: sin agujeros, ejes ni texto.
- **Todo paramétrico**: ninguna medida escrita a mano dentro del modelo. Cada número vive en `P_DEF`, dentro del generador, con su comentario.
- **Supuestos a la vista**: toda medida no tomada sobre el objeto real se marca `SUPUESTO` y se mantiene en la lista de pendientes hasta que se mida.
- **Cifras con procedencia**: al dar un número, decir si es medido, de ficha, calculado o estimado. No inventar fuerzas de imán, tolerancias ni tiempos de impresión.
- Unidades: milímetros y grados. Coma decimal en los textos; punto decimal en el CSV.

## 6. Orden de trabajo

Existe un prototipo v3 modelado (apartado 1c de `contexto.md`) y un plan de pruebas (`reporte-v3/plan-de-pruebas.md`). A partir de ahí:

1. **Primero la impresora, no Fusion.** Probetas P0 a P4, en orden. No se modela una v4 ni se retoca la v3 sin el resultado de la probeta que toque.
2. Medir el reloj montado y sustituir los supuestos. El contorno del brazalete es el dato que más manda.
3. Cambios de diseño: siempre en el generador, nunca a mano en Fusion (apartado 8).
4. Probar con el reloj dentro: NFC, imanes cerca del movimiento, ajuste del brazalete.
5. Cuando otra sesión o el usuario dejen una revisión en el repositorio (como `contra-reporte-v2.md`), leerla entera y contestarla punto por punto, diciendo qué se hace, qué no y por qué.

## 7. Puertas que no se saltan

- **No imprimir la versión final** sin las medidas reales del reloj montado (ancho con corona, grosor, óvalo del brazalete abrochado, tipo de cierre).
- **No dar por buena la llave magnética** sin haber impreso y probado la probeta P1, ni el cierre de un empujón sin la P2.
- **No meter el reloj en una caja con imanes** sin haber valorado antes el riesgo de magnetización (H8).
- Imprimir siempre una aguja de repuesto.

## 8. Herramientas

- **Carpeta de trabajo** en el ordenador del usuario: `C:\Users\pepea\Documents\FusionClaude\WatchBox`. El usuario quiere **todo guardado ahí**: modelos (`.f3d`, `.step`), ficheros para imprimir (`imprimir-vN\*.3mf`), generador, capturas y copia de los documentos del Proyecto. Si la sesión no tiene esa carpeta conectada, pedírsela.
- **Fusion**: el modelo lo construye entero un script, `generador_caja_vN.py` (ahora **v3**, con `frase-v3.json` al lado). Un componente por pieza: `base`, `tapa`, `tapeta`, `rotor`, `aguja`, `peana`, `pinza`, `funda`, `frase`, más `reloj_referencia` y `tarjeta_referencia`. Para cambiar una medida se edita `P_DEF` en el generador y se vuelve a ejecutar; no se retoca la geometría a mano, porque el siguiente regenerado lo borraría.
- Cómo ejecutarlo desde un script de Fusion: `RUTA = 'C:/Users/pepea/Documents/FusionClaude/WatchBox/generador_caja_v3.py'`; `g = {'__file__': RUTA, '__name__': 'ev3'}`; `exec(compile(open(RUTA, encoding='utf-8').read(), RUTA, 'exec'), g)`; `g['main']()` reconstruye y comprueba; `g['exportar'](carpeta, 'v3')` escribe el `.f3d`, el `.step`, `imprimir-v3\`, `probetas-v3\` y el CSV de parámetros.
- **La v2 y la v3 están en documentos de Fusion distintos**, los dos sin guardar («Sin título»). Comprobar cuál está activo antes de ejecutar nada.
- **Ojo al copiar ficheros al ordenador del usuario**: tras modificar un fichero en la sesión, la copia que llega al PC puede ser la anterior durante unos segundos. Comprobar el tamaño o el md5 en el PC antes de ejecutarlo.
- En el montaje la `pinza` se dibuja con la forma que toma con el reloj puesto; la que se exporta para imprimir es la forma libre, más abierta.
- Tras cada regenerado: comprobar interferencias, el pestillo grado a grado y el resbalón (lo hace `main()`), exportar con `exportar()` y hacer capturas.
- Si la sesión tiene conexión con Fusion en el ordenador del usuario, Claude puede modelar directamente. Comprobarlo con una llamada real antes de afirmar que funciona. Si no, dar los pasos de menú uno a uno.
- **No guardar el documento de Fusion en la nube** sin que el usuario lo pida; exportar a la carpeta sí.
- **Bambu Studio**: los colores y la textura de papel («fuzzy skin») se asignan aquí, no en Fusion. Exportar cada cuerpo como 3MF.
- **Git**: no hacer commit ni push sin que el usuario lo pida. A 19-nov-2026 esta sesión **no puede escribir** en `Pepe-a-d/eventually-caja` (ni por git ni por el conector): lo sube el usuario o la otra sesión. Comprobarlo con una llamada real antes de prometer una subida. Si se cambia un parámetro, cambiar a la vez `parametros-fusion.csv` y el texto del brief que lo cita.

## 9. Mantener el contexto

Cuando cambie una decisión, se tome una medida o se pruebe algo, actualizar `contexto.md` en este Proyecto: mover el dato de «supuesto» a «medido», cerrar la pregunta o el hallazgo y poner la fecha. No dejar el cambio solo en la conversación.
