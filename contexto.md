# Eventually, la caja: contexto

> **AVISO del 20 de noviembre de 2026, añadido por la sesión del Mac. Lee esto antes que nada.**
> **La v4 y su parche v4.1 están PARADAS.** La probeta P1 falló: los imanes no mueven el mecanismo. Pepe volvió a la fase de diseño y eligió otra caja: cilíndrica, con iris y ascensor, movidos por un bisel con planetario.
> **Manda [`BRIEF-v5.md`](BRIEF-v5.md)**, que explica qué pasó, qué se decidió y por dónde empezar. Los resultados de las probetas están en [`resultados-probetas.md`](resultados-probetas.md).
> Todo lo que sigue en este documento, incluido el apartado 0, es histórico hasta que se ponga al día.

Estado a **19 de noviembre de 2026**, con el **prototipo v4** ya modelado en Fusion (apartado 0; la v3 está en el 1c). Integra el repositorio `Pepe-a-d/eventually-caja` (hasta el commit `4153169`), la web publicada, el contra-reporte de la v2 y el trabajo de las tres versiones. **Donde este documento hable de la v2 o del brief y no coincida con el apartado 1c, manda el 1c.**

## 0. Estado a 20 de noviembre de 2026: prototipo v4 (MANDA sobre todo lo demás)

- **v4 modelada en Fusion y exportada.** Responde a `contra-reporte-v3.md` (commit `ddc97e8`, 4 fallos graves y 10 importantes sobre la v3). Detalle en `reporte-v4/reporte-v4.md`; montaje en `reporte-v4/guia-de-montaje.md`; pruebas en `reporte-v4/plan-de-pruebas.md`. **Nada impreso ni medido. Van cinco versiones.**
- **Qué cambia respecto a la v3 (apartado 1c):** rotor rígido de **un solo sentido**, con tope en cerrado y espiral precargada 18°; la caja **se cierra con la aguja puesta** (fuera el resbalón de la v3, que se acuñaba); un segundo rotor **articulado** opcional para cerrar de un empujón, que cabe en el mismo panel y solo entra si pasa P2; banda maciza del panel detrás de cada pestillo y **tapa trasera entera** a presión (el rotor se monta girado 45° y el taco de la espiral se lleva con un clip hasta pasar un diente); **pinza a medida** (brazalete + 6 mm), dibujada en su forma libre; **peana corredera** entre dos guías con labio, que sale tirando del reloj; **emergencia por la base** (ranura sobre el pestillo de abajo, se arrastra de lado); **retén de la funda** (dos nervios de 0,5 mm); imanes de esquina bajo 1,3 mm (1,2 N) para que la aguja haga de tirador; fuera la esquina achaflanada (el «solo al derecho» es un resalte por detrás); retenes de aguja y tarjeta.
- **Medidas:** con funda 98,6 × 76,0 × 95,4 mm; caja 94,0 × 71,4 × 92,7; panel 6,6 de grueso. 8 imanes. 165 parámetros (`parametros-fusion-v4.csv`).
- **Del modelo:** pestillo bloqueado de 0° a 21°, libre desde 22°; rotor rígido libre de 0° a 50°; rotor articulado sin choques en reposo y libre de 0° a 47°; el rotor entra a 45° sin tocar los puentes. Interferencias que quedan, a propósito: roce de la aguja en su rebaje y pellizco de la tarjeta.
- **Sin hacer:** pista de apertura y aviso del imán en la web (punto 12); quitar imanes de esquina, rotor en PETG, texto interior y pomo (16 a 18); mover v0 y v1 a `archivo/`.
- **Regla que no se salta:** ninguna caja entera sin medir antes el reloj. `brazalete_contorno` vale 180 mm por suposición.
- **Preguntas al usuario sin contestar:** fecha de entrega (preguntada cinco veces); si el reloj está montado y cuánto mide el brazalete; si vale cerrar con la aguja puesta; si quiere conservar el clic de imán del panel; si la otra sesión pone la pista y el aviso en la web; grado de los imanes.
- **GitHub:** el usuario subió la v3 a mano (`277be6d`, `21fb41d`); la otra sesión añadió `contra-reporte-v3.md` (`ddc97e8`). El usuario subió la v4 a mano (`4874e30`) y la otra sesión añadió `contra-reporte-v4.md` (`f3f798a`). **El parche v4.1 lo subió esta sesión el 20-nov-2026** (integración nativa de GitHub, con permiso de escritura desde ese día; el conector de GitHub sigue devolviendo 403): rama `parche-v4.1`, pull request nº 1, **fusionada en `main` ese mismo día a petición del usuario**.
- **Fusion:** v2, v3 y v4 están en tres documentos distintos sin guardar («Sin título»). El generador de la v4 es `generador_caja_v4.py`, en la carpeta de trabajo, y usa `frase-v3.json`.
- **Siguiente paso:** medir el reloj e imprimir P0 y P1 de `probetas-v4\`. No modelar una v5 sin ese resultado.
- **PARCHE v4.1 (20-nov-2026, sobre `contra-reporte-v4.md`, commit `f3f798a`).** El usuario pidió «no una v5: un parche de la v4». Mismo generador y mismos nombres de fichero, regenerados. Detalle en `reporte-v4/parche-v4.1.md`. Cambios: ranura de emergencia **pasante** y comprobada en `main()`; el taco de la espiral ya no va tras un diente, tiene un **ojo que entra en un tetón** del panel y un resalte de la tapa trasera lo retiene; puntas del rotor rebajadas 0,4 mm y holgura al labio de 0,35; tapa trasera con **pestaña y clip**; peana retenida por dos **lengüetas elásticas** (unos 2,7 N, calculado); nervios de la funda de 0,8 mm; chaflán de entrada en las guías; imanes de esquina bajo 1,8 mm (0,69 N); **se cierra girando la aguja de vuelta**, no confiando en el muelle. 178 parámetros; medidas exteriores iguales. Sin hacer: imán bajo el rebaje de la aguja, pomo, y todo lo que espera a la medida del reloj. El parche **no está subido a GitHub**.

## 1. Resumen

- **Estado**: **prototipo v3 modelado en Fusion y exportado** (apartado 1c). **Nada impreso, nada medido** sobre el reloj real. Van cuatro versiones (v0 brief, v1, v2, v3) sin imprimir una pieza.
- **Por qué hay una v3**: el 19-nov-2026 se subió al repositorio `contra-reporte-v2.md`, una revisión crítica de la v2 con 6 fallos graves, 11 importantes, cálculos de fuerzas, la especificación de la v3 en 23 puntos y un plan de cinco probetas. El usuario pidió: «léelo, analízalo y prepara una v3 teniendo en cuenta todos los requisitos y anotaciones». La respuesta punto por punto está en `reporte-v3/reporte-v3.md`.
- **Por qué hubo una v2**: el usuario vio la v1 (caja alta que se abría por arriba) y dijo que era muy incómodo acceder al reloj y usar la caja como expositor. Pidió rediseñar el sistema, una llave más fina y estilizada, y la frase con la tipografía del reloj y de la web.
- **Imanes**: el usuario tiene **14 contados** (dato del 19-nov-2026 que corrige un «de sobra» anterior) y **no tiene chapas de acero**. La v3 usa 8; 10 con una aguja de repuesto.
- **Siguiente paso**: **imprimir la probeta P0 y la P1** (`reporte-v3/plan-de-pruebas.md`). No modelar más hasta tener ese resultado. En paralelo, medir el reloj: lo primero, el contorno interior del brazalete cerrado.
- **Plazo**: la tarjeta y la web dicen «montado a mano, diciembre de 2026». La fecha de entrega no consta: **preguntarla**.
- **Carpeta de trabajo** en el ordenador del usuario: `C:\Users\pepea\Documents\FusionClaude\WatchBox`. Ahí está todo.
- **GitHub**: `Pepe-a-d/eventually-caja`, público, rama `main`. El 19-nov-2026 **el usuario subió la v2 a mano** (commit `e340db5`, «Add files via upload»). Después llegaron dos commits con el contra-reporte (`331fa6b` y `4153169`, autor `5vm4hcmchy-hub`, hechos desde otra sesión de Claude). **La v3 no está subida**: la sesión de Claude de este proyecto sigue sin permiso de escritura. Se probó tres veces: el proxy de git respondió que el repositorio no está en el conjunto autorizado, `add_repo` con escritura fue rechazado por falta de permiso push, y el conector de GitHub (cuenta `Pepe-a-d`) devolvió «403 Resource not accessible by integration» al crear una rama. Los dos navegadores Chrome conectados a la cuenta son de macOS y el usuario dijo que no son suyos: no usarlos. Antes de dar algo por subido, comprobar el repositorio.

## 1c. Prototipo v3 (19-nov-2026)

Sustituye a la v2. Detalle y figuras en `reporte-v3/reporte-v3.md`; montaje en `reporte-v3/guia-de-montaje.md`; pruebas en `reporte-v3/plan-de-pruebas.md`.

**Cómo se usa.** Se levanta la funda (campana). Queda un bloque blanco con la aguja azul tumbada encima, a ras. La aguja se pone en el centro del frente, se gira 50° a la derecha y se queda. Se tira del panel por abajo. En la mano queda el panel con la tarjeta; dentro, el reloj de pie. Para cerrar se empuja el panel, sin aguja.

**Piezas (9 imprimibles).**

| Pieza | Material | Qué es |
| --- | --- | --- |
| `base` | PLA blanco | Caja interior, 94,0 × 70,3 × 91,7 mm. Boca al frente. Aguja guardada en un rebaje del techo. Rebaje en el suelo para la peana. Bisel de apertura bajo el panel, en dos tramos |
| `tapa` | PLA blanco | Panel frontal a ras, 87,6 × 83,3 × 6,0 mm (7,7 con los carriles). Piel de 1,4. Esquina superior derecha achaflanada. Carriles en U para la tarjeta por detrás |
| `tapeta` | PLA blanco | Tira de 40 mm en cola de milano que retiene el rotor. Entra por arriba, sin pegamento |
| `rotor` | PLA blanco | Barra vertical de 8 mm con un pestillo en cada extremo, cubo, y una **espiral** de 1,5 vueltas que hace de muelle |
| `aguja` | PLA azul | 54 mm, 2,6 de grueso. Cubo de 9, cola en pala, varilla de 2,2 a 1,6, flecha calada. Dos imanes embutidos |
| `peana` | PLA blanco | Base encastrada en el suelo (talón a 45° y cuatro dientes) con dos cunas |
| `pinza` | **PETG** | Pinza en C, extrusión pura de 36 mm. Cara plana rígida de 43 mm y brazo elástico de 1,6 |
| `funda` + `frase` | Mármol + azul | Campana de 98,6 × 74,9 × 94,4 mm. Frase en el techo, NFC debajo por dentro |

Referencias, no se imprimen: `reloj_referencia` (cabeza, corona, brazalete y cierre) y `tarjeta_referencia`.

**Mecanismo.**

- El rotor gira **hacia los dos lados** desde su reposo: 13,7° a izquierdas cuando la boca lo empuja al cerrar (resbalón) y 50° a derechas con la aguja. Se libera a 24,1°. No descansa contra un tope: lo centra la espiral.
- El pico de cada pestillo está en la esquina de la barra, a 4 mm del eje; el canto va inclinado y lleva un chaflán de 2,2 mm en la cara de entrada.
- Enganche de 2,0 mm; por encima de 1 mm entre −8° y +18,5° (del modelo).
- Taladro de emergencia de 1,5 mm en el techo, sobre el pico del pestillo de arriba.
- El imán del rotor y la pala de la aguja van a 16 mm del eje.

**Imanes (8).** Aguja 2, central 1, rotor 1, esquinas del panel 2 (arriba-izquierda y abajo-derecha) y sus 2 parejas en la caja. Los de esquina van embutidos con pausa bajo 0,8 mm; los de la aguja, bajo 0,4. Regla de montaje: todos con la misma cara hacia el frente.

**Comprobado en el modelo** (Fusion, 19-nov-2026): sin interferencias entre los 11 cuerpos; pestillo bloqueado de −12° a +22° grado a grado; el rotor gira libre de −15° a +50°; el resbalón pide al rotor hasta 13° y lo deja pasar; cristal a 3,0 mm de los carriles; brazalete a 3,0 mm del techo; 9,0 mm de hueco tras la pinza.

**Calculado** (`reporte-v3/calculos-v3.txt`; `imanes.py` reproduce la tabla 3.1 del contra-reporte): aguja contra rotor 0,89 N a 2,0 mm; arrastre máximo 6,9 mN·m; espiral 1,0 mN·m a 50° con 0,6 mm de grueso; la aguja girada se sujeta con 5,0 mN·m; panel sujeto con 2,3 N; campo en el centro del movimiento 900 A/m (límite ISO 764: 4 800), 1 400 con la aguja puesta. El imán central queda a 17,2 mm del movimiento (23,7 en la v2).

**Decisiones de Claude que se apartan del contra-reporte, y por qué.**

- **Resbalón**: no es un chaflán en una punta centrada (no hace girar: el empuje pasa por el eje). Pico descentrado y giro en sentido contrario al de la aguja.
- **Muelle**: no es un brazo que apoya en un tetón (se deformaría un 3 %). Espiral, al 0,35 %.
- **Bisel**: no es a todo lo ancho; los 34 mm centrales son el labio del pestillo de abajo.
- **Tapeta**: no cubre toda la cámara; las dos ventanas que deja las tapa la tarjeta. Así el panel no tiene puentes.
- **Aguja guardada**: de atrás adelante y a la derecha, no centrada, para que su rebaje se imprima sin puente y quede lejos del NFC.
- **Tamaño**: se cumple el fondo (74,9; objetivo 75) pero el alto sube a 94,4. Lo fija `brazalete_contorno`, hoy 180 mm por suposición: con 160 serían 84,6 de alto; con 200, 104,3.

**Sin hacer**: punto 20 (mover `BRIEF.md` y la v1 a `archivo/`), punto 21 (pomo: no, se mantiene la aguja fina), punto 22 (aviso del imán en tarjeta o web) y punto 23 (texto interior).

**Riesgos nuevos de la v3**, todos para las probetas: que la espiral se imprima pegada al alma que la cruza en puente; que el chaflán del resbalón deslice; la pinza con brazaletes en los extremos del rango; el labio en voladizo de los carriles; que la boquilla (de acero) arranque los imanes embutidos; que la peana, boca abajo, levante el frente unos 3 mm.

**Parámetros**: 135, en `parametros-fusion-v3.csv`. El apartado 11 lista los de la v2: ya no valen.

## 1b. Prototipo v2: la caja-expositor (19-nov-2026). SUSTITUIDO por la v3

**La idea.** La caja ya no se abre por arriba: se abre **por delante**. El frente es un panel liso, como una esfera en blanco, y la aguja se coloca en su centro y se gira como la manecilla de un reloj. Al quitar el panel, la caja queda como una vitrina: el reloj de pie, recostado 25°, con la tarjeta de fondo.

**Cómo se usa.**

1. La funda lleva la frase en el frente y la aguja guardada en el lateral cerrado.
2. Se saca la caja de la funda pellizcándola por las muescas de arriba y de abajo.
3. Se pone la aguja en el centro del frente liso, con la punta hacia arriba (las 12), y se gira en sentido horario unos 40° (hasta la 1 y pico).
4. Con la uña en la muesca de la pared izquierda se saca el panel frontal. Se puede dejar pegado por imanes en la trasera de la caja.
5. El reloj queda a la vista sobre su soporte, con 21 mm libres a cada lado para meter los dedos. El soporte sale tirando hacia delante y sirve también solo, en la mesilla.

**Qué hay en Fusion.** Un documento con 75 parámetros de usuario y 10 componentes: `base`, `tapa`, `tapeta`, `rotor`, `aguja`, `soporte`, `funda`, `frase`, y dos de referencia que no se imprimen (`reloj_referencia`, `tarjeta_referencia`). El documento de Fusion estaba **sin guardar en la nube** («Sin título») al terminar; hay copia exportada en la carpeta de trabajo.

**Cómo está hecho.** La geometría la genera `generador_caja_v2.py`, que lee `frase.json` de su misma carpeta. Las formas **no se actualizan solas** al cambiar un parámetro en Fusion: se edita `P_DEF` en el generador y se vuelve a ejecutar entero. Para ejecutarlo desde Claude, con Fusion abierto:

```python
RUTA = 'C:/Users/pepea/Documents/FusionClaude/WatchBox/generador_caja_v2.py'
g = {'__file__': RUTA, '__name__': 'ev2'}
exec(compile(open(RUTA, encoding='utf-8').read(), RUTA, 'exec'), g)
for linea in g['main'](): print(linea)      # reconstruye y comprueba
g['exportar']('C:/Users/pepea/Documents/FusionClaude/WatchBox', 'v2')   # f3d, step y 3mf
```

Ejes: X ancho (la funda abre por +X), Y fondo (el frente es −Y), Z alto.

**Decisiones v2.** Tomadas por Claude a partir de lo que pidió el usuario; **pendientes de su visto bueno**.

| Tema | Decisión v2 |
|---|---|
| Apertura | Por delante. El panel frontal (87,6 × 71,6 × 4,6 mm) va encastrado a ras y es completamente liso. |
| Reloj | De pie y recostado 25° hacia atrás, mirando al frente. El punto más adelantado queda a 5 mm del panel y a 9,6 mm de la boca de la caja. |
| Soporte | Anillo ovalado de 60 × 46 × 30 mm, inclinado, con dos patines de 8 mm que llegan hasta debajo del reloj para que no vuelque. Encaja en un rebaje de 1,2 mm del suelo y lo sujetan dos imanes. Una sola postura: la misma dentro de la caja y en la mesilla. |
| Tarjeta | De pie contra la pared del fondo, como telón, sujeta por dos guías en cuña en las paredes laterales. Se mete curvándola un poco. Ya no va en el suelo, así que no estorba al soporte (resuelve H15). |
| Enganche | Mismo sistema que la v1, girado: el rotor es vertical y sus extremos entran 1,3 mm en ranuras del techo y del suelo. Giro de 40° (era 60°) para que la cámara quepa bajo la tapeta. |
| Cierre por gravedad | El único imán del rotor va en el brazo de abajo, así que con la caja de pie el rotor tiende a volver solo a la posición de cerrado. |
| Aguja | Más fina: 51,8 mm de largo, 2,4 mm de grosor (era 3,2), varilla que se afina de 2,0 a 1,2 mm, punta de flecha calada de 10 × 6,5 mm, cubo de 9 mm y un disco de 8,6 mm en la cola. Los dos imanes van en el cubo y en el disco de la cola, a 13,5 mm. |
| Aguja guardada | En el fondo cerrado de la funda, en un rebaje de 1,4 mm con su silueta y un plato alrededor del cubo para cogerla. Sobresale 1,0 mm. Dos imanes la sujetan por fuera y hacen el clic con la caja por dentro. |
| Panel aparcado | Cuatro imanes en la cara trasera de la caja para dejar ahí el panel mientras la caja hace de expositor. |
| Frase | En el frente de la funda, arriba a la izquierda: «Who cares,» / «I'm already late.» en **Reenie Beanie**, sacada del fichero de fuente del repositorio de la web (`fonts/reenie-beanie.woff2`). Bloque de 74,4 × 22,4 mm, incrustado 0,6 mm. Trazo **engordado 0,20 mm por lado** para que sea imprimible con boquilla de 0,4 (R6): el trazo medio pasa de 0,56 a 0,95 mm. Es un cuerpo aparte (`frase`) para imprimirlo en azul con el AMS. |
| NFC | En el techo de la funda, por dentro, desplazado 27 mm hacia el fondo. |
| Funda | Abre por un lateral. Muescas de 12 mm de radio arriba y abajo para sacar la caja. |
| Impresora | Bambu Lab X1 Carbon con AMS (confirmado). La pieza mayor mide 98,1 × 92,2 × 83,4 mm: cabe. |

**Medidas resultantes.**

| Pieza | Ancho × fondo × alto (mm) | Volumen |
|---|---|---|
| `funda` | 98,1 × 92,2 × 83,4 | 92,1 cm³ |
| `base` | 94,0 × 87,6 × 78,8 (hueco 88 × 80 × 72) | 114,1 cm³ |
| `tapa` | 87,6 × 4,6 × 71,6 | 19,7 cm³ |
| `tapeta` | 62,0 × 1,0 × 71,6 | 4,4 cm³ |
| `rotor` | 14,0 × 2,2 × 74,6 | 1,4 cm³ |
| `aguja` | 51,8 de largo × 9,0 × 2,4 | 0,4 cm³ |
| `soporte` | 46,0 × 60,0 × 63,2 | 30,0 cm³ |
| `frase` | 74,4 × 0,6 × 22,4 | 0,1 cm³ |

La caja es más profunda que la v1 (87,6 mm frente a 64) porque el reloj va de pie sobre el óvalo. Aplanar el óvalo la acortaría, pero sus medidas siguen siendo un supuesto hasta medir el brazalete.

**Imanes**: 24 (funda 2, base 12, tapa 5, rotor 1, aguja 2, soporte 2), más 2 por cada aguja de repuesto.

**Comprobado en el modelo.**

- Análisis de interferencias de Fusion entre los 10 cuerpos: ninguna.
- Pestillo: bloqueado de 0° a 20°, libre desde 25°. El rotor no toca tapa ni caja en todo el recorrido y los topes lo paran por debajo de 0° y por encima de 40°.
- Imanes del panel al centro del movimiento del reloj: 23,7 mm (central) y 31,3 mm (rotor). Al punto más cercano del reloj, el borde inferior del bisel: 11,2 mm.
- Reloj a 5,0 mm del panel y a 5,0 mm del techo; brazalete a 5,4 mm de la pared trasera.

**No comprobado (solo se sabrá imprimiendo).**

- Que el imán de la cola de la aguja arrastre un rotor de 74,6 mm (R1). El brazo de arrastre es ahora de 13,5 mm en vez de 20.
- Que el cierre por gravedad funcione en la práctica y que el rotor no se mueva con la caja tumbada.
- Que la aguja, tan fina, aguante el uso: imprimir repuestos.
- La lectura del NFC y el efecto real de los imanes sobre el reloj.
- Que la tarjeta se quede en su sitio con la caja boca abajo.
- Las holguras (0,2 mm panel, 0,3 mm funda).

**Lo que el prototipo v2 no lleva.**

- Redondeos y chaflanes: todas las aristas están vivas.
- Textura de papel: se pone en Bambu Studio.
- Los tres nervios de apoyo del rotor y el clic en los topes.
- La corona y el brazalete en el volumen de referencia del reloj.
- Decisión sobre la puntuación de la frase (H9): lleva coma y punto, como el brief y la web.

**Notas de impresión.**

- `base`: con la pared trasera sobre la cama y la boca hacia arriba. Refuerzos y guías están a 45°, pensados para salir sin soportes.
- `tapa`: con la cara lisa sobre la cama.
- `funda` + `frase`: cargarlas juntas en Bambu Studio como un solo objeto de dos piezas y dar a `frase` el filamento azul. Con la cara de la frase sobre la cama sale más nítida, pero el techo queda en puente; de pie sobre el fondo cerrado no hay puentes, pero hay cambio de color en muchas capas.
- `soporte`: necesitará soportes.

**Historia.** La v1 (caja de 94 × 64 × 81,5 mm que se abría por arriba, aguja de 44 mm con flecha ancha) queda archivada en la carpeta de trabajo: `Eventually-caja-v1.f3d`, `Eventually-caja-v1.step`, `imprimir-v1\` y `generador_caja_v1.py`.

## 2. Lo que ya existe

| Cosa | Detalle |
|---|---|
| Reloj | Eventually — Late Edition · 1 of 1. Caja de acero cepillado estilo PRX de 40 mm, brazalete integrado, cristal de zafiro, movimiento Seiko NH36 automático. Esfera blanca con la frase manuscrita en azul arriba y los doce números amontonados abajo. Agujas de acero y segundero azul con punta de flecha y contrapeso en pala. |
| Web | https://pepe-a-d.github.io/eventually/ · Al hacer scroll el reloj se monta pieza a pieza sobre papel blanco. Secciones: El corazón, La esfera, Las agujas, La azul, La caja; ficha técnica e instrucciones de uso. Lema: «Llegará. Cuando llegue.» |
| Tarjeta | Certificado de autenticidad, 85 × 55 mm, cartulina de 300–350 g. Anverso: «Late Edition · 1 of 1», «Eventually», «Llegará. Cuando llegue.» Reverso: ficha, «Montado a mano para Pablo. Pepe» y el QR. Diseño en Figma: https://www.figma.com/design/zTqZch5frY3qcnWlQMConH |
| QR | `referencias/qr.svg`, 33 módulos, azul `#1F3FA8`. **Comprobado**: lleva a https://pepe-a-d.github.io/eventually/ |
| NFC | Etiqueta de 25 mm de diámetro que lleva a la web. El usuario la tiene. |
| Imanes | Discos de 5 × 1,6 mm. **Tiene 14 contados** (y alguno suelto más), dato del 19-nov-2026 que corrige el «de sobra» anterior. **No tiene chapas de acero**: el diseño solo puede contar con imanes. La v2 usa 24: no se puede montar. La v3 debe salir con 14 como máximo; ver `contra-reporte-v2.md`, apartado I4. |

## 3. El concepto y las decisiones cerradas

La caja se abre en el mismo orden en que el reloj se monta en la web: primero el papel, luego la aguja, luego el reloj.

1. **Funda** exterior blanca con textura de papel y la frase en azul. Dentro, oculta, la etiqueta NFC.
2. **Caja interior** que sale deslizándose y encaja con un clic de imán. Su tapa es completamente lisa.
3. **La aguja es la llave**: una aguja azul suelta con forma de segundero, guardada por imán en un rebaje de la funda. Se pone en el centro de la tapa, se gira, y un pestillo oculto la sigue arrastrado por su imán hasta soltarse.
4. **Soporte** donde va abrochado el reloj. Se saca entero y en la mesilla presenta la esfera inclinada. Debajo, en su ranura, la tarjeta.

**Decidido por el autor:**

- Abre con la aguja como llave magnética. Nada de palabras en la tapa («pronto / tarde» no gustó).
- Lleva las tres cosas: aguja que gira, imanes y caja dentro de funda deslizante.
- La frase va en la funda; la aguja pertenece a la caja interior.
- Lleva hueco para la tarjeta, hueco para el NFC y textura de papel.
- Quiere probar su filamento mármol blanco.

**Descartado:**

- Reloj tumbado y abierto (el brazalete integrado no se abre en línea).
- Darle cuerda con varias vueltas, hora secreta, lema palabra a palabra.
- Aguja que levanta la tapa con una rampa helicoidal: no se eligió, pero queda como **plan B** si la llave magnética no tira.

## 4. Datos de partida

| Dato | Valor | Estado |
|---|---|---|
| Reloj: diámetro sin corona | 40 mm | Ficha del vendedor |
| Reloj: grosor | 11 mm | Ficha del vendedor |
| Reloj: de asa a asa | 44 mm | Ficha del vendedor |
| Reloj: ancho con corona | ~43,5 mm | **Supuesto**, medir |
| Brazalete: ancho | ~27 mm junto a la caja, ~18 mm en el cierre | **Supuesto** |
| Brazalete: grosor | ~3,5 mm | **Supuesto** |
| Brazalete abrochado | óvalo de ~67 × 53 mm por fuera | **Supuesto** (muñeca de 17,5 cm) |
| Cierre | mariposa | **Supuesto** |
| Tarjeta | 85 × 55 mm | Ya diseñada |
| Imanes | 5 × 1,6 mm | Los tiene |
| NFC | Ø 25 mm | La tiene |
| Impresora | Bambu Lab X1 Carbon con AMS (multicolor) | **Confirmado por el usuario** el 19-nov-2026. El brief decía «H2 Carbon». |

## 5. Las piezas según el brief v0

Son **siete** piezas impresas (el brief dice «seis», ver H2). Esta tabla es la propuesta original; las medidas del prototipo están en el apartado 1b.

| Pieza | Qué es | Medidas v0 |
|---|---|---|
| `funda` | Tubo rectangular con un extremo abierto. Frase en azul incrustada a ras en la cara superior. Rebaje del NFC en la cara interior del techo. Rebaje con imán para guardar la aguja en el fondo cerrado. Imán de cierre. Muesca para el pulgar. | Exterior 95,1 × 67,4 × 81,0 mm. Pared 2 mm. Holgura 0,3 mm por lado. |
| `base` | Caja interior. Ranura de la tarjeta en el suelo (86 × 56 × 1,2 mm) con muesca para el dedo. Dos nervios que centran el soporte. Cuatro imanes en las esquinas del borde superior. Dos labios de 2 mm en las paredes largas. Un imán en la trasera. | Exterior 92,8 × 62,8 × 70,4 mm. Cavidad 88 × 58 × 68 mm. Pared y suelo 2,4 mm. |
| `tapa` | Cara superior lisa, piel de 1,0 mm sobre el mecanismo. Alojamiento circular del rotor. Imán central fijo. Cuatro imanes en las esquinas. Faldón de centrado de 3 mm. | Alto total 6 mm. |
| `rotor` | Barra que gira bajo la piel. Imán a 20 mm del centro. Sus extremos son los pestillos. Tres nervios de apoyo, topes a 0° y 60° con un pequeño clic. | 57 × 9 × 2,2 mm. Juego axial 0,3 mm. |
| `tapeta` | Disco fino que cierra el alojamiento del rotor por debajo, a presión o pegado. | Sin medidas en el CSV. |
| `aguja` | Azul, silueta de segundero: cubo, varilla con punta de flecha y contrapeso en pala. Dos imanes: uno en el cubo y otro a 20 mm del centro. | Punta 30 mm, cola 14 mm, grosor 3,2 mm, cubo Ø 12 mm, varilla 2,4 mm. |
| `soporte` | Óvalo donde se abrocha el brazalete. Una cara plana para la caja y otra inclinada 25° para la mesilla. Hueco interior para aligerar y apretar el cierre. | 60 × 46 mm, 30 mm de ancho. |

## 6. Cómo funciona la llave magnética

```
     aguja (fuera)      [imán cubo]────────[imán arrastre]───▶ punta
══════════════════════════════════════════════════════════════  piel de la tapa, 1,0 mm
     tapa (dentro)      [imán central]     [imán del rotor]
                             fijo           gira con la aguja
```

1. Se acerca la aguja a la tapa: el imán del cubo se va solo al centro.
2. Al orientarla, su segundo imán engancha el del rotor.
3. Se gira unos 60°: el rotor la sigue y los pestillos salen de los labios.
4. Se levanta la tapa: ya solo la sujetan los cuatro imanes de las esquinas.

Cada pareja enfrentada se atrae. Los cuatro de las esquinas se montan con la misma orientación.

## 7. Riesgos del brief

| # | Riesgo | Qué hacer |
|---|---|---|
| R1 | **El imán no arrastra el rotor.** A 1,2 mm de separación tiran poco y de lado mucho menos. Fuerzas sin calcular ni medir. | Imprimir primero una **probeta**: disco con piel de 1,0 mm, rotor y aguja. Si no tira: piel de 0,8 mm, dos imanes apilados en la aguja o radio menor. Si aun así no: plan B. |
| R2 | El rotor roza y se queda. | Tres nervios de apoyo, juego axial de 0,3 mm, grafito en polvo. |
| R3 | El imán del rotor se pega a los de las esquinas. | Mantenerlo a más de 15 mm en todo el recorrido. |
| R4 | La aguja se pierde. | Rebaje con imán en la funda. Una de repuesto. |
| R5 | El acero del reloj interfiere con el NFC. | NFC en el techo de la funda, a más de 15 mm del reloj. Probar con el reloj dentro. |
| R6 | Trazos de la frase demasiado finos para la boquilla. | Trazo mínimo 0,8 mm: engrosar o calcar la frase de la esfera como vectores. |

## 8. Hallazgos del análisis del 19-nov-2026

Detectados por Claude al cruzar el brief con el CSV. **Ninguno está corregido en el repositorio.** El prototipo v2 propone una solución para H1, H3 a H8, H10, H12 y H15 (apartado 1b), pendiente del visto bueno del usuario. Las cifras de esta lista se refieren al brief v0.

**Afectan a la geometría (resolver antes de modelar):**

- **H1. Largo de la aguja.** El brief dice «~58 mm (30 de punta + 14 de cola)», pero 30 + 14 = 44 mm. Uno de los dos números está mal.
- **H2. Número de piezas.** El brief dice «seis piezas impresas» y describe siete.
- **H3. Imanes de esquina.** El alojamiento mide Ø 5,15 mm y la pared de la base 2,4 mm: el imán no cabe en el canto. Hacen falta refuerzos en las esquinas, que no pueden bajar hasta el suelo porque chocarían con la tarjeta (85 × 55 en una cavidad de 88 × 58). El faldón de la tapa tendrá que esquivarlos.
- **H4. Fondo de la funda.** Tiene 2 mm de pared, pero ahí van el rebaje de la aguja (3,2 mm de grosor), su imán (1,8 mm) y el imán de cierre (1,8 mm). Si la aguja queda a ras hacen falta unos 5 mm, y `funda_largo` crecería lo mismo.
- **H5. Imán de arrastre en la aguja.** Va «bajo la varilla» a 20 mm del centro, pero la varilla mide 2,4 mm de ancho y el imán 5 mm. Necesita un ensanche (por ejemplo, alojarlo en la punta de flecha) o cambiar el radio, que entonces cambia también en el rotor.
- **H6. Tapa y faldón.** No queda claro si los 3 mm de faldón están dentro de los 6 mm de `tapa_alto`. Si lo están, la tapa sobresale 3 mm, la funda sobra 3 mm de alto y el aire sobre el cristal baja de 7,5 a 4,5 mm.
- **H7. NFC.** R5 pide más de 15 mm entre NFC y reloj, pero con las medidas v0 quedan entre 10,8 y 13,8 mm (según H6). Además, el imán central de la tapa queda a unos 1,3 mm justo debajo del centro de la etiqueta. Probarlo pronto. Alternativas: etiqueta NFC para superficies metálicas o moverla a una pared lateral de la funda.
- **H8. Imanes cerca del movimiento (riesgo nuevo, no está en el brief).** El reloj es mecánico y los imanes pueden magnetizarlo y hacer que adelante. El imán central queda a 8–11 mm del cristal. Estimación de orden de magnitud, en el eje y para un solo imán: unos 4–9 mT a 8–10 mm y unos 1,5 mT a 15 mm, y aproximadamente el doble con la aguja puesta. La referencia habitual de resistencia magnética (ISO 764) es 4800 A/m, unos 6 mT. El volante está más lejos y fuera del eje, así que el valor real será menor, pero el margen no es holgado. **Es una estimación, no una medida.** Opciones: más aire entre tapa y reloj, comprobar con una brújula o una app de magnetómetro, tener un desmagnetizador a mano.

**Otros puntos:**

- **H9. Puntuación de la frase.** En las fotos de la esfera pone «Who cares / I'm already late», sin coma ni punto. El brief y la web escriben «Who cares, I'm already late.» Las fotos son de IA, así que hay que mirar la esfera real y decidir cuál va en la funda.
- **H10. Rotor muy justo.** Al girar, la esquina del rotor pasa a 0,15 mm de la pared (semidiagonal 28,85 mm frente a 29 mm). Redondear los extremos. Los pestillos quedan libres desde unos 30° de giro, así que los 60° previstos dan margen. `labio_arco` está definido en grados, pero los labios van en paredes rectas.
- **H11. Techo de la funda.** Donde coinciden la frase (0,6 mm por fuera) y el rebaje del NFC (0,5 mm por dentro) quedan 0,9 mm de pared. Viable, pero fino.
- **H12. Sentido de deslizamiento.** El CSV asume que la funda abre por un extremo corto (la caja desliza a lo largo de sus 93 mm). La pregunta 3 sigue abierta; si cambia, cambian las fórmulas de la funda.
- **H13. Impresora. Resuelto**: es una Bambu Lab X1 Carbon con AMS, confirmado por el usuario.
- **H15. Nervios del soporte y ranura de la tarjeta.** El brief pide «dos nervios bajos» en el suelo para centrar el soporte, pero la ranura de la tarjeta (86 × 56) ocupa casi todo el suelo (88 × 58): no caben sin tapar la tarjeta. Sin algo que lo sujete, el soporte queda suelto dentro de la caja y el reloj puede golpear las paredes.
- **H14. Color del papel.** El brief da `#F7F6F2`; la web parece declarar `#F4F3EF` como color de tema. Diferencia mínima, sin verificar en el código.

**Comprobado y correcto:**

- Los 54 parámetros del CSV se evalúan sin errores y las medidas que cita el brief coinciden con ellos (redondeadas).
- R3: suponiendo los imanes de esquina a 4,5 mm de cada pared interior, el imán del rotor pasa como mínimo a 26,5 mm de ellos. Cumple los 15 mm.
- La proporción de las imágenes de la tarjeta corresponde a 85 × 55 mm.
- El QR lleva a la web.

## 9. Material e impresión

| Pieza | Filamento | Acabado |
|---|---|---|
| Funda | Mármol blanco | Textura de papel por fuera |
| Base, tapa, tapeta, soporte | Blanco mate | Liso |
| Aguja y frase | Azul mate, lo más cercano a `#1F3FA8` | Liso |

- **Textura de papel**: ajuste «fuzzy skin» del laminador, solo en el contorno exterior de la funda. Las caras que deslizan, lisas. Por comprobar en Bambu Studio si se puede desactivar en la zona de la frase con un modificador.
- **Frase**: incrustada en azul, 0,6 mm de fondo. Sale más nítida si esa cara se imprime contra la cama.
- **Imanes**: alojamientos de Ø 5,15 × 1,8 mm, a presión con una gota de cianoacrilato. Los ocultos (rotor, aguja) pueden meterse con una pausa de impresión.
- **Holguras de partida**: 0,3 mm por lado para deslizar, 0,2 mm tapa sobre base, 0,15 mm a presión. Ajustar con la probeta.
- **Capa**: 0,16–0,2 mm. La piel de 1,0 mm son 5 capas de 0,2.

## 10. Estética

- **Colores**: papel `#F7F6F2`, tinta azul `#1F3FA8`, texto `#15171C`, gris `#555A64`.
- **Tipografías** (Google Fonts, libres; en Windows hay que instalar los TTF para usarlas en Fusion): *Reenie Beanie* para la frase manuscrita, *Instrument Serif* para «Eventually», *Instrument Sans* para textos pequeños.
- **Regla**: todo blanco y liso; una sola cosa azul que se mueve.
- **Frase según el brief**, con su partición: `Who cares,` / `I'm already late.` (ver H9).

## 11. Parámetros del prototipo v2 (ya no valen: ver `parametros-fusion-v3.csv`)

Son los 75 parámetros cargados en Fusion, sacados de `P_DEF` en `generador_caja_v2.py` (copia en `parametros-fusion-v2.csv`, en la carpeta de trabajo). Los marcados «v2» son nuevos o cambian respecto a la v1. El CSV del repositorio (commit `0fda075`, 54 parámetros) sigue en v0.

| Parámetro | Valor | Expresión | Comentario |
|---|---|---|---|
| `reloj_diametro` | 40 mm | `40 mm` | Caja del reloj sin corona (ficha del vendedor) |
| `reloj_grosor` | 11 mm | `11 mm` | Del cristal a la tapa trasera (ficha del vendedor) |
| `reloj_asa_asa` | 44 mm | `44 mm` | De asa a asa (ficha del vendedor) |
| `reloj_ancho_corona` | 43,5 mm | `43.5 mm` | SUPUESTO: ancho total con corona. Medir |
| `brazalete_ancho` | 27 mm | `27 mm` | SUPUESTO: ancho del brazalete junto a la caja. Medir |
| `brazalete_grosor` | 3,5 mm | `3.5 mm` | SUPUESTO: grosor del brazalete. Medir |
| `tarjeta_largo` | 85 mm | `85 mm` | Tarjeta de autenticidad |
| `tarjeta_ancho` | 55 mm | `55 mm` | Tarjeta de autenticidad |
| `tarjeta_grosor` | 0,5 mm | `0.5 mm` | Cartulina de 300-350 g |
| `iman_d` | 5 mm | `5 mm` | Diametro del iman |
| `iman_h` | 1,6 mm | `1.6 mm` | Altura del iman |
| `iman_aloj_d` | 5,15 mm | `iman_d + 0.15 mm` | Alojamiento a presion |
| `iman_aloj_h` | 1,8 mm | `iman_h + 0.2 mm` | Fondo del alojamiento |
| `iman_retiro` | 0,5 mm | `0.5 mm` | Retiro extra de los imanes de esquina para suavizar el clic |
| `nfc_d` | 25 mm | `25 mm` | Etiqueta NFC |
| `nfc_aloj_d` | 25,6 mm | `nfc_d + 0.6 mm` | Rebaje del NFC en el techo de la funda |
| `nfc_aloj_h` | 0,5 mm | `0.5 mm` | Fondo del rebaje del NFC |
| `nfc_y` | 27 mm | `27 mm` | v2: NFC hacia el fondo de la caja, lejos del reloj y de los imanes |
| `holg_desliza` | 0,3 mm | `0.3 mm` | Holgura por lado entre funda y caja |
| `holg_tapa` | 0,2 mm | `0.2 mm` | Holgura por lado entre tapa y caja |
| `holg_presion` | 0,15 mm | `0.15 mm` | Holgura para encajes a presion |
| `pared` | 3 mm | `3 mm` | Paredes laterales y fondo de la caja |
| `pared_techo` | 3,4 mm | `3.4 mm` | v2: techo y suelo de la caja: ranura del pestillo, rebaje e imanes del soporte |
| `pared_funda` | 2 mm | `2 mm` | Pared de la funda |
| `funda_fondo` | 3,8 mm | `3.8 mm` | v2: fondo cerrado de la funda: rebaje de aguja + imanes |
| `soporte_largo` | 60 mm | `60 mm` | SUPUESTO: eje largo del ovalo del soporte. Ajustar al brazalete |
| `soporte_alto` | 46 mm | `46 mm` | SUPUESTO: eje corto del ovalo del soporte |
| `soporte_ancho` | 30 mm | `30 mm` | Ancho del soporte (sentido de la muneca) |
| `soporte_inclinacion` | 25° | `25 deg` | v2: cuanto se recuesta la esfera hacia atras respecto a la vertical |
| `soporte_pared` | 4 mm | `4 mm` | Grosor del anillo del soporte |
| `soporte_pie` | 4,5 mm | `4.5 mm` | Altura libre bajo el anillo para el brazalete |
| `soporte_rebaje` | 1,2 mm | `1.2 mm` | v2: rebaje del suelo donde encajan los patines |
| `soporte_iman_retiro` | 1,2 mm | `1.2 mm` | v2: retiro de los imanes del soporte para que salga sin arrastrar la caja |
| `patin_ancho` | 8 mm | `8 mm` | Ancho de cada patin lateral del soporte |
| `patin_alto` | 14 mm | `14 mm` | Altura de los patines |
| `patin_frente` | 34 mm | `34 mm` | v2: del centro del anillo al frente del patin (bajo el reloj, para que no vuelque) |
| `patin_detras` | 22 mm | `22 mm` | v2: del centro del anillo a la trasera del patin |
| `aire_frente` | 5 mm | `5 mm` | v2: aire entre la tapa y el punto mas adelantado del reloj |
| `guia_tarjeta` | 2,5 mm | `2.5 mm` | v2: saliente de las guias en cuna que sujetan la tarjeta al fondo |
| `guia_alto` | 45 mm | `45 mm` | v2: altura de las guias de la tarjeta |
| `nicho_ancho` | 88 mm | `tarjeta_largo + 3 mm` | v2: ancho interior de la caja |
| `nicho_alto` | 72 mm | `72 mm` | v2: alto interior de la caja |
| `nicho_fondo` | 80 mm | `80 mm` | v2: fondo interior de la caja, de la tapa a la pared trasera |
| `tapa_piel` | 1 mm | `1 mm` | Piel sobre el mecanismo. Bajar a 0.8 si el iman no arrastra |
| `rotor_grosor` | 2,2 mm | `2.2 mm` | Grosor del rotor |
| `rotor_holg_axial` | 0,3 mm | `0.3 mm` | Juego del rotor |
| `rotor_ancho` | 9 mm | `9 mm` | Ancho de la barra del rotor |
| `rotor_giro` | 40° | `40 deg` | v2: giro entre cerrado y abierto |
| `rotor_radio_iman` | 13,5 mm | `13.5 mm` | v2: del centro al iman de arrastre (va en la cola de la aguja) |
| `rotor_enganche` | 1,3 mm | `1.3 mm` | Cuanto entra cada pestillo del rotor en techo y suelo |
| `rotor_radio` | 37,3 mm | `nicho_alto / 2 + rotor_enganche` | Radio del rotor, extremos redondeados |
| `pestillo_grosor` | 1,2 mm | `1.2 mm` | Grosor del pestillo en cada extremo del rotor |
| `tapeta_grosor` | 1 mm | `1 mm` | Grosor de la tapeta |
| `tapeta_largo` | 62 mm | `62 mm` | Largo de la tapeta |
| `tapa_alto` | 4,6 mm | `tapa_piel + rotor_grosor + rotor_holg_axial + tapeta_grosor + 0.1 mm` | Grosor de la tapa frontal, encastrada a ras |
| `refuerzo_esq` | 8,5 mm | `8.5 mm` | Refuerzo de esquina para los imanes de la tapa |
| `caja_ancho` | 94 mm | `nicho_ancho + 2 * pared` | v2: exterior de la caja |
| `caja_alto` | 78,8 mm | `nicho_alto + 2 * pared_techo` | v2: exterior de la caja |
| `caja_fondo` | 87,6 mm | `pared + nicho_fondo + tapa_alto` | v2: exterior de la caja, tapa incluida |
| `aguja_punta` | 34 mm | `34 mm` | v2: del centro a la punta |
| `aguja_grosor` | 2,4 mm | `2.4 mm` | v2: grosor de la aguja-llave (era 3.2) |
| `aguja_cubo_d` | 9 mm | `9 mm` | v2: diametro del cubo (era 12) |
| `aguja_pala_d` | 8,6 mm | `8.6 mm` | v2: diametro del disco de la cola, aloja el iman de arrastre |
| `aguja_varilla` | 2 mm | `2 mm` | v2: ancho de la varilla junto al cubo |
| `aguja_varilla_punta` | 1,2 mm | `1.2 mm` | v2: ancho de la varilla junto a la flecha |
| `aguja_flecha_largo` | 10 mm | `10 mm` | v2: largo de la punta de flecha calada |
| `aguja_flecha_ancho` | 6,5 mm | `6.5 mm` | v2: ancho de la punta de flecha |
| `aguja_flecha_pared` | 1 mm | `1 mm` | v2: grosor del contorno de la flecha |
| `aguja_rebaje` | 1,4 mm | `1.4 mm` | v2: profundidad del rebaje de la aguja en la funda |
| `funda_largo` | 98,1 mm | `caja_ancho + holg_desliza + funda_fondo` | Exterior de la funda (un extremo abierto) |
| `funda_ancho` | 92,2 mm | `caja_fondo + 2 * holg_desliza + 2 * pared_funda` | Exterior de la funda |
| `funda_alto` | 83,4 mm | `caja_alto + 2 * holg_desliza + 2 * pared_funda` | Exterior de la funda |
| `frase_fondo` | 0,6 mm | `0.6 mm` | Profundidad de la frase incrustada |
| `frase_trazo_min` | 0,8 mm | `0.8 mm` | Trazo minimo imprimible de la letra |
| `frase_margen` | 11 mm | `11 mm` | v2: margen de la frase desde la esquina superior izquierda del frente de la funda |

## 12. Preguntas abiertas

**Añadidas con la v3**: ¿cuánto mide el contorno del brazalete? (manda en el alto de la caja); ¿de qué grado son los imanes?; ¿vale la funda de campana, que cambia el gesto de deslizar por el de levantar?; ¿vale el rebaje redondo para coger la aguja?

**Las de abajo vienen de la v2**; las que hablan de la v2 ya no aplican.

**Del brief:**

1. ~~Modelo exacto de la impresora~~ Resuelta: X1 Carbon con AMS.
2. Medidas reales del reloj montado: ancho con corona, grosor, óvalo del brazalete abrochado y tipo de cierre.
3. ~~¿La funda abre por un extremo corto o por uno largo?~~ En la v2 abre por un lateral.
4. ~~¿Tipografía o calco?~~ Resuelta por el usuario: la tipografía del reloj y de la web (Reenie Beanie).
5. ¿Dónde vive la aguja cuando no se usa? En la v2, en el fondo cerrado de la funda. Sin confirmar.
6. ¿El soporte se queda en blanco o lleva algún detalle?
7. ¿Lleva algo escrito por dentro, como «Llegará. Cuando llegue.» en el interior de la tapa?
8. Geometría exacta del enganche: el faldón de la tapa y los labios de la base compiten por el mismo sitio junto a la pared.

**Nuevas de este análisis:**

9. ¿Cuál es la fecha de entrega del regalo?
10. ~~¿La aguja mide 44 o 58 mm?~~ La v2 mide 51,8 mm, más fina, a petición del usuario.
11. ¿Frase con coma y punto, o como está en la esfera real? (H9)
12. ~~¿Cuántos imanes hay?~~ Resuelta el 19-nov-2026: **14**. La v2 usa 24, así que el límite para la v3 es 14.
13. ¿Visto bueno a la v2 (apartado 1b)? En especial: apertura frontal, reloj recostado 25°, tarjeta como telón de fondo, forma de la aguja y tamaño de la caja (98 × 92 × 83 mm con funda).

## 13. Próximos pasos

1. **Subir la v3 a GitHub** (lo hace el usuario o una sesión con permiso de escritura). Lista de ficheros en `reporte-v3/reporte-v3.md`, apartado 8.
2. **Imprimir P0 y P1** y anotar el resultado. Después P2, P3 y P4.
3. **Medir el reloj**: contorno interior del brazalete cerrado, ancho con corona, ancho por fuera de las asas, ancho y grosor del brazalete, grosor del cierre.
4. Regenerar el modelo con los valores de las probetas y las medidas reales.
5. Decisiones del usuario pendientes: fecha de entrega; aguja con pomo o plana; texto por dentro; aviso del imán en la tarjeta o en la web; si se mueven la v0 y la v1 a `archivo/`; si se guarda el documento de Fusion en la nube y con qué nombre.

## 14. Recursos

- Reporte ilustrado de la v2 (13 figuras: secuencia de uso, vistas, explosionada, mecanismo, cortes, aguja, frase, mapa de imanes): documento de Claude en https://claude.ai/artifact/6rz71bxzmzG8sH2qDRZtQg y copia en la carpeta de trabajo, `reporte-v2\reporte-v2.pdf` (también `.html`, `.md` y las figuras sueltas). Las figuras se regeneran con las capturas de Fusion y un script de matplotlib; si cambia el modelo, hay que rehacerlas.
- Generador del prototipo: `generador_caja_v3.py`, **en la carpeta de trabajo** (en el Proyecto de Claude solo están copiados el de la v1 y el de la v2). Necesita `frase-v3.json` a su lado
- Reporte de la v3: `reporte-v3/reporte-v3.md` y `.pdf`, con `guia-de-montaje.md` y `plan-de-pruebas.md`
- Contra-reporte de la v2: `contra-reporte-v2.md`, en el repositorio y en la carpeta de trabajo
- Carpeta de trabajo: `C:\Users\pepea\Documents\FusionClaude\WatchBox`
- Repositorio de la caja: https://github.com/Pepe-a-d/eventually-caja (en `4153169` a 19-nov-2026: v2 y contra-reporte; la v3 no está subida)
- Repositorio de la web: https://github.com/Pepe-a-d/eventually
- Web publicada: https://pepe-a-d.github.io/eventually/
- Tarjeta en Figma: https://www.figma.com/design/zTqZch5frY3qcnWlQMConH
- Referencias en el repositorio, carpeta `referencias/`: `esfera-sin-agujas.jpeg` (para calcar la letra), `reloj-terminado.jpeg`, `tarjeta-anverso.png`, `tarjeta-reverso.png`, `qr.svg`. Las dos fotos del reloj son de IA: **no sirven para medir**.
