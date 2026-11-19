# Eventually — la caja

> **Este es el brief original (v0), del 19 de noviembre de 2026. Se conserva como punto de partida.**
> El diseño ha cambiado desde entonces: la caja ya está modelada y ahora se abre por delante (v2).
> El estado actual está en [`contexto.md`](contexto.md) y en [`reporte-v2/reporte-v2.pdf`](reporte-v2/reporte-v2.pdf).
> Las medidas de este documento y de `parametros-fusion.csv` ya no son las vigentes; las vigentes están en `parametros-fusion-v2.csv`.

Documento para retomar el diseño de la caja en Fusion desde otro ordenador.
Estado: **concepto cerrado, nada modelado.** Las medidas son una primera propuesta (v0)
y están todas en `parametros-fusion.csv` para poder cambiarlas.

Escrito el 19 de noviembre de 2026.

---

## 1. De qué va esto

Pepe está montando a mano un reloj para su amigo Pablo. El reloj se llama **Eventually —
Late Edition · 1 of 1**. Ya existen:

- **El reloj**: caja de acero estilo PRX de 40 mm con brazalete integrado, esfera blanca con
  la frase «Who cares, I'm already late» escrita a mano en azul y los doce números
  amontonados abajo, agujas de acero y un segundero azul. Movimiento Seiko NH36.
- **La web**: https://pepe-a-d.github.io/eventually/ — al hacer scroll el reloj se monta pieza
  a pieza sobre papel blanco. Papel claro, tinta azul, tipografía manuscrita.
- **La tarjeta de autenticidad**: 85 × 55 mm, impresa. Va dentro de la caja.
- **Un QR y una etiqueta NFC** que llevan a la web.

Falta la **caja**, impresa en 3D. Tiene que ser innovadora, útil, elegante y del mismo
mundo que el reloj y la web: blanco papel y una sola pieza azul.

## 2. El concepto

La caja se abre en el mismo orden en que el reloj se monta en la web: primero el papel,
luego la aguja, luego el reloj.

1. **La funda.** Exterior, blanca, con textura de papel. Lleva la frase
   «Who cares, I'm already late» en azul. Dentro, oculta, la etiqueta NFC.
2. **La caja interior.** Sale deslizándose de la funda y encaja con un clic de imán.
   Su tapa es **completamente lisa**: ni agujeros ni ejes ni texto.
3. **La aguja es la llave.** Una aguja azul suelta, con forma de segundero, vive pegada
   por imán en un rebaje de la funda. Se coloca en el centro de la tapa, se gira, y un
   pestillo oculto bajo la superficie la sigue arrastrado por su imán hasta soltarse.
   Sin la aguja, la caja no se abre.
4. **El reloj.** Va abrochado en un soporte que se saca entero y que, puesto en la
   mesilla, presenta la esfera inclinada. La caja se guarda; el soporte se queda en uso.
   Debajo del soporte, en su ranura, la tarjeta.

### Decisiones tomadas por Pepe

- Abre con **la aguja como llave magnética**. Descartado poner palabras en la tapa
  («pronto / tarde» no le gustó).
- Lleva **las tres cosas**: aguja que gira, imanes y caja dentro de funda deslizante.
- La frase va **en la funda**; la aguja pertenece a **la caja interior**.
- Lleva hueco para la **tarjeta**, hueco para el **NFC** y **textura de papel**.
- Quiere probar su filamento **mármol blanco**.

### Descartado

- Reloj tumbado y abierto: el brazalete integrado lleva cierre de mariposa (por confirmar)
  y no se abre en línea.
- Otras aperturas que se propusieron y no se eligieron: aguja que levanta la tapa con una
  rampa helicoidal (era la alternativa robusta, **plan B si la llave magnética no tira**),
  darle cuerda con varias vueltas, hora secreta, lema palabra a palabra.

## 3. Datos de partida

| Dato | Valor | Fuente |
|---|---|---|
| Impresora | Bambu Lab serie H2, multicolor | Pepe dijo «H2 Carbon»: confirmar modelo exacto |
| Imanes | 5 × 1,6 mm (disco) | Pepe los tiene |
| Etiqueta NFC | 25 mm de diámetro | Pepe la tiene |
| Tarjeta | 85 × 55 mm, cartulina de 300–350 g | ya diseñada |
| Reloj: diámetro | 40 mm sin corona | ficha del vendedor |
| Reloj: grosor | 11 mm | ficha del vendedor |
| Reloj: de asa a asa | 44 mm | ficha del vendedor |
| Reloj: ancho con corona | ~43,5 mm | **supuesto**, sin medir |
| Brazalete: ancho | ~27 mm en la caja, ~18 mm en el cierre | **supuesto** (PRX típico) |
| Brazalete: grosor | ~3,5 mm | **supuesto** |
| Brazalete abrochado | óvalo de ~67 × 53 mm por fuera | **supuesto** (muñeca de 17,5 cm) |
| Cierre | mariposa | **supuesto**, sin confirmar |

Pepe pidió empezar con las medidas de un reloj normal de este tipo. **Todo lo marcado
como supuesto hay que medirlo con el reloj montado antes de imprimir la versión final.**

## 4. Las piezas

Seis piezas impresas. Los números son la propuesta v0.

### 4.1 Funda (`funda`)
- Tubo rectangular abierto por un extremo. La caja interior entra por el lado largo.
- Exterior aprox. **95 × 67 × 81 mm**, pared de 2 mm, holgura de deslizamiento 0,3 mm por lado.
- **Frase** «Who cares, I'm already late» en azul, incrustada a ras en la cara superior.
- **Rebaje NFC** en la cara interior del techo: Ø 25,6 mm × 0,5 mm. Queda tapado por la caja.
- **Rebaje para la aguja-llave** en el fondo cerrado (cara exterior), con su silueta y un
  imán debajo para que se quede pegada.
- **Imán de cierre** en el fondo, que casa con otro en la trasera de la caja interior.
- Muesca para el pulgar en el borde abierto, para empujar la caja.

### 4.2 Caja interior (`base`)
- Exterior aprox. **93 × 63 × 71 mm**. Cavidad interior 88 × 58 × 68 mm.
- Pared 2,4 mm, suelo 2,4 mm.
- **Ranura de la tarjeta** en el suelo: 86 × 56 × 1,2 mm, con muesca para el dedo.
- **Asiento del soporte**: dos nervios bajos que lo centran sobre la tarjeta.
- **Cuatro imanes** en las esquinas del borde superior, para el clic de la tapa.
- **Dos labios** de 2 mm en el interior de las paredes largas, donde engancha el pestillo.
- Un imán en la cara trasera, para el clic contra la funda.

### 4.3 Tapa (`tapa`)
- **Cara superior lisa**, piel de 1,0 mm sobre el mecanismo.
- Por debajo, un alojamiento circular donde gira el rotor.
- **Imán central fijo**: atrae al imán del cubo de la aguja y la centra sola.
- Cuatro imanes en las esquinas, enfrentados a los de la base.
- Faldón de centrado de 3 mm que entra en la base.

### 4.4 Rotor del pestillo (`rotor`)
- Barra que gira bajo la piel de la tapa, alrededor del centro.
- Lleva **un imán a 20 mm del centro**, que es el que arrastra la aguja.
- Sus dos extremos son los **pestillos**: en reposo quedan bajo los labios de la base.
  Girada unos 50°, salen de los labios y la tapa queda libre.
- Apoya sobre tres nervios finos para rozar lo mínimo.
- Dos topes limitan el giro a 0° (cerrado) y 60° (abierto), con un resalte que da un
  pequeño clic en cada extremo.

### 4.5 Tapeta del mecanismo (`tapeta`)
- Disco fino que cierra el alojamiento del rotor por debajo. Encaja a presión o pegado.

### 4.6 Aguja-llave (`aguja`)
- Azul. Silueta de segundero: cubo redondo, varilla fina con punta de flecha y contrapeso
  en pala. Largo total ~58 mm (30 de punta + 14 de cola desde el centro), grosor 3,2 mm.
- **Dos imanes**: uno en el cubo (se centra sobre la tapa) y otro a 20 mm del centro,
  bajo la varilla (arrastra el rotor).
- Los imanes van metidos por debajo, con 0,2 mm de piel o a ras.

### 4.7 Soporte (`soporte`)
- Óvalo de **60 × 46 mm** y 30 mm de ancho, donde se abrocha el brazalete.
- Dos caras de apoyo: una plana, para ir dentro de la caja, y otra **inclinada 25°**, para
  que en la mesilla la esfera mire hacia quien la ve.
- Hueco por dentro para aligerar y para poder apretar el cierre con los dedos.

## 5. Cómo funciona la llave magnética

```
        aguja (fuera)        [imán cubo]────────[imán arrastre]───▶ punta
   ══════════════════════════════════════════════════════════════  piel de la tapa, 1,0 mm
        tapa (dentro)        [imán central]     [imán del rotor]
                                  fijo            en el rotor, gira con la aguja
```

1. Se acerca la aguja a la tapa. El imán del cubo se va solo al centro.
2. Al orientarla, su segundo imán encuentra el del rotor y se «engancha».
3. Se gira la aguja unos 60°. El rotor la sigue y los pestillos salen de los labios.
4. Se levanta la tapa: solo la sujetan ya los cuatro imanes de las esquinas.

Polaridades: cada pareja enfrentada se **atrae**. Montar los cuatro de las esquinas con la
misma orientación para no tener que mirar.

### Riesgos y cómo atacarlos

| # | Riesgo | Qué hacer |
|---|---|---|
| R1 | **El imán no arrastra el rotor.** A 1,2 mm de separación, dos imanes de 5 × 1,6 tiran poco, y de lado mucho menos. Las cifras de fuerza no están calculadas ni medidas. | Imprimir primero **solo una probeta**: un disco con piel de 1,0 mm, el rotor y la aguja. Si no tira: piel de 0,8 mm, dos imanes apilados en la aguja, o radio de arrastre menor. Si aun así no: **plan B**, la rampa helicoidal. |
| R2 | El rotor roza y se queda. | Tres nervios de apoyo, holgura axial de 0,3 mm, grafito en polvo. |
| R3 | El imán del rotor se pega a los de las esquinas. | Mantenerlo a más de 15 mm de cualquier imán de esquina en todo su recorrido. |
| R4 | La aguja se pierde. | Su rebaje con imán en la funda. Imprimir una de repuesto. |
| R5 | El acero del reloj interfiere con el NFC. | El NFC va en el techo de la funda, a más de 15 mm del reloj. Probar con el reloj dentro. |
| R6 | La frase manuscrita tiene trazos demasiado finos para la boquilla. | Trazo mínimo de 0,8 mm: engrosar el texto o calcar la frase real de la esfera como vectores. |

## 6. Material e impresión

| Pieza | Filamento | Acabado |
|---|---|---|
| Funda | **Mármol blanco** | Textura de papel por fuera |
| Base, tapa, tapeta, soporte | Blanco mate | Liso |
| Aguja-llave, frase | Azul mate, lo más cercano a `#1F3FA8` | Liso |

- **Textura de papel**: es el ajuste «fuzzy skin» del laminador. Solo en el contorno
  exterior de la funda. Las caras que deslizan tienen que quedar lisas. Por comprobar en
  Bambu Studio si se puede desactivar en la zona de la frase con un modificador.
- **Frase**: incrustada en azul, 0,6 mm de fondo. Si la cara de la frase se imprime
  contra la cama, sale muy nítida.
- **Imanes**: alojamientos de Ø 5,15 × 1,8 mm, a presión, con una gota de cianoacrilato.
  Los que quedan ocultos (rotor, aguja) se pueden meter con una pausa de impresión.
- **Holguras de partida**: 0,3 mm por lado para deslizar, 0,2 mm para tapa sobre base,
  0,15 mm para encajes a presión. Ajustar con la probeta.
- Altura de capa 0,16–0,2 mm; la piel de 1,0 mm de la tapa son 5 capas de 0,2.

## 7. Estética: lo que tiene que casar con la web

- **Colores**: papel `#F7F6F2`, tinta azul `#1F3FA8`, texto `#15171C`, gris `#555A64`.
- **Tipografías** (las tres son libres, de Google Fonts; en Windows hay que instalar los
  TTF para usarlas en Fusion):
  - *Reenie Beanie*: la manuscrita, la de la frase.
  - *Instrument Serif*: la del nombre «Eventually».
  - *Instrument Sans*: textos pequeños.
- **Regla**: todo blanco y liso; una sola cosa azul que se mueve.
- La frase exacta, con su partición: `Who cares,` / `I'm already late.`

## 8. Trabajar en Fusion

Propuesta de organización, a decidir al retomar:

1. Un diseño con **parámetros de usuario** (los de `parametros-fusion.csv`) y un
   **componente por pieza**: `funda`, `base`, `tapa`, `rotor`, `tapeta`, `aguja`, `soporte`.
2. Orden: base → tapa → rotor y tapeta → aguja → soporte → funda. La funda al final,
   porque depende del exterior de la base.
3. Una **junta de revolución** entre rotor y tapa para comprobar el recorrido de los
   pestillos y la distancia a los imanes de las esquinas.
4. Exportar cada cuerpo como 3MF. Los colores se asignan en Bambu Studio.

**Antes de la caja entera, la probeta de R1.** Es media hora de impresión y decide si el
concepto vale.

`parametros-fusion.csv` va sin cabecera, con las columnas *nombre, unidad, expresión,
comentario*. Sirve para el complemento ParameterIO de Fusion o para que un script los
cree con la API; si el importador pide otro formato, se adapta.

## 9. Preguntas abiertas

1. Modelo exacto de la impresora H2 y si lleva sistema multicolor.
2. Medidas reales del reloj montado: ancho con corona, grosor, óvalo del brazalete
   abrochado y tipo de cierre.
3. ¿La funda abre por un extremo corto o por uno largo?
4. ¿La frase va con la tipografía Reenie Beanie o calcada de la esfera real?
5. ¿Dónde vive la aguja cuando no se usa: fondo de la funda, lateral, o dentro?
6. ¿El soporte se queda en blanco o lleva algún detalle?
7. ¿Lleva algo escrito por dentro, como el lema «Llegará. Cuando llegue.» en el interior
   de la tapa?
8. **Geometría exacta del enganche.** El faldón de la tapa y los labios de la base
   compiten por el mismo sitio junto a la pared: hay que resolver en el CAD a qué altura
   va cada uno. Es lo primero que hay que dibujar después de la probeta.

## 10. Para retomar

Abre una sesión de Claude en el PC, en la carpeta donde esté este documento, y pega:

> Lee `BRIEF.md` y `parametros-fusion.csv`. Es el diseño de la caja impresa en 3D del reloj
> Eventually; el concepto está cerrado y no hay nada modelado. Quiero modelarla en Fusion.
> Empieza por la probeta del riesgo R1 (piel, rotor y aguja) y, antes de dibujar nada,
> repasa conmigo las preguntas abiertas del apartado 9.

En la carpeta `referencias/` van las imágenes que hacen falta para modelar:

- `esfera-sin-agujas.jpeg`: la esfera con la frase y los números, para calcar la letra.
- `reloj-terminado.jpeg`: el reloj completo visto desde arriba.
- `tarjeta-anverso.png` y `tarjeta-reverso.png`: la tarjeta que tiene que caber en la ranura.
- `qr.svg`: el QR de la web, en un solo trazo.

Las dos fotos del reloj están generadas por IA a partir de las piezas: sirven para la
estética, **no para tomar medidas**.

Otros enlaces del proyecto:

- Web publicada: https://pepe-a-d.github.io/eventually/
- Tarjeta en Figma: https://www.figma.com/design/zTqZch5frY3qcnWlQMConH
