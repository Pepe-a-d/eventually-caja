# Eventually, la caja v3: guía de montaje

Escrita el 19 de noviembre de 2026 a partir del modelo. **Nadie ha montado todavía esta caja**: si un paso no sale como dice aquí, manda el paso, no la guía, y hay que corregirla.

Los ficheros de `imprimir-v3/` ya vienen girados como deben ir en la cama. No los gires.

## 1. Qué hace falta

- 8 imanes de 5 × 1,6 mm (10 si haces una aguja de repuesto).
- Un rotulador permanente.
- La etiqueta NFC de 25 mm.
- PLA blanco, PLA azul, PLA blanco mármol para la funda y un poco de PETG para la pinza.
- Un clip.

## 2. La regla de los imanes

**Todos los imanes van con la misma cara mirando hacia el frente de la caja.**

1. Apila los imanes en una torre. Se colocan solos, todos igual.
2. Pinta con el rotulador la cara de arriba de la torre.
3. Saca uno de arriba, pinta la cara que queda arriba, y así con todos.

Ya tienes todos marcados por la misma cara. Esa cara es **la marca**.

| Imán | Cómo se pone | La marca queda… |
| --- | --- | --- |
| Aguja (2) | En la pausa, con la pieza en la cama | hacia arriba |
| Panel, esquinas (2) | En la pausa, con la cara vista en la cama | hacia **abajo** |
| Panel, central (1) | A mano, por detrás, en el hueco del eje | hacia **abajo** (hacia la cara vista) |
| Rotor (1) | A mano, por la cara de la espiral | a la vista, en la cara de la espiral |
| Caja, esquinas (2) | En la pausa, con la boca hacia arriba | hacia arriba |

**Antes de tapar ningún imán, compruébalo.** Acerca la torre al imán ya puesto, con la marca de la torre mirando hacia el mismo lado que debe mirar la del imán. Tiene que atraer. Si repele, el imán está al revés.

Un imán embutido al revés no se puede sacar. Esa pieza se tira.

## 3. Impresión

Capa de 0,2 mm en todo. Sin soportes en ninguna pieza.

| Pieza | Material | Ajustes que importan |
| --- | --- | --- |
| `base.3mf` | PLA blanco | Pared trasera en la cama. **Pausa a unos 63,4 mm** para los 2 imanes de esquina |
| `tapa.3mf` | PLA blanco | Cara vista en la cama. **7 capas inferiores macizas** (es la piel de 1,4 mm, y así no se transparenta el imán). **Pausa a 5,2 mm** para los 2 imanes de esquina |
| `tapeta.3mf` | PLA blanco | — |
| `rotor.3mf` | PLA blanco | Cara de la espiral en la cama. Generador de paredes Arachne, para que la espiral salga de una pasada. Sin borde de adherencia |
| `aguja.3mf` | PLA azul | **Pausa a 2,2 mm** para los 2 imanes. Imprime tres |
| `peana.3mf` | PLA blanco | De pie |
| `pinza.3mf` | **PETG** | De canto, tal como viene |
| `funda.3mf` + `frase.3mf` | Mármol + azul | Techo en la cama. Ver 3.1 |

Las alturas de pausa salen del modelo. **Compruébalas en la vista previa del laminador:** la pausa va justo antes de la primera capa que tapa el agujero del imán.

En cada pausa: mete el imán hasta el fondo, con la marca como dice la tabla. Tiene que entrar a presión; si baila, la boquilla (que es de acero) se lo lleva. El diámetro del agujero se elige con la probeta P0.

### 3.1 La funda con la frase

1. En Bambu Studio, importa `funda.3mf` y `frase.3mf` **a la vez** y contesta que sí cuando pregunte si son un solo objeto de varias piezas.
2. Asigna el filamento mármol a la funda y el azul a la frase.
3. No las muevas una respecto a otra.

La frase ocupa las 3 primeras capas. El cambio de color solo pasa ahí.

## 4. Montaje del panel

Con el panel boca abajo, la cara vista sobre la mesa.

1. **Imán central.** Mételo en el hueco del eje, con la marca hacia abajo, hasta el fondo.
2. **Imán del rotor.** Mételo en el brazo que tiene agujero, por la cara de la espiral.
3. **Rotor.** Colócalo en el eje con la espiral hacia abajo. El brazo del imán apunta hacia el borde de abajo del panel, que es el de la ranura para la uña (la esquina cortada queda arriba). El taco de la espiral entra en su muesca; solo cabe de una manera.
4. **Prueba antes de cerrar.** Gira el rotor con el dedo hacia los dos lados y suéltalo: tiene que volver solo al centro.
5. **Tapeta.** Entra por el borde de arriba del panel y baja hasta el tope. Sin pegamento.
6. **Prueba con la aguja.** Dale la vuelta al panel. Pon la aguja en el centro: se pega vertical, punta arriba. Gírala a la derecha hasta el tope y suéltala: se queda. Quítala: el rotor vuelve.
7. **Tarjeta.** Entra por arriba entre los dos carriles, hasta los topes.

## 5. Montaje de la caja

1. **Peana.** Mete primero el talón de atrás bajo el suelo y baja el frente. Los dientes de delante la centran.
2. **Reloj.** Fuera de la caja: aprieta la pinza, pásale el brazalete cerrado y suéltala. La cara plana queda bajo la tapa del reloj; el cierre, por detrás.
3. **Pinza a la peana.** Déjala caer en las dos cunas, con el reloj mirando al frente.
4. **Panel.** Solo entra de una manera: la esquina cortada, arriba a la derecha. Empuja hasta que quede a ras. Tira de él: no tiene que salir.
5. **Aguja.** En su rebaje, encima de la caja, con la punta hacia el frente.
6. **NFC.** Pégalo en el rebaje redondo que hay por dentro del techo de la funda.
7. **Funda.** Bájala despacio.

## 6. Si el panel no abre

En el techo de la caja, cerca del frente, hay un taladro de 1,5 mm. Mete un clip, empuja hacia abajo unos 2 mm y, sin soltar, tira del panel por abajo.

## 7. Aviso para Pablo

La aguja lleva dos imanes. Sobre el reloj, a 4 mm, supera seis veces el límite que aguanta un reloj mecánico sin magnetizarse (dato del contra-reporte). Que no la deje encima.
