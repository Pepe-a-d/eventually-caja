# Eventually, la caja v4: guía de montaje

Escrita el 20 de noviembre de 2026 a partir del modelo. **Nadie ha montado todavía esta caja.** Corrige la guía de la v3, que describía un montaje imposible.

**No imprimas la caja entera sin haber medido el reloj.** Las probetas P0 y P1 sí se pueden imprimir ya.

## 1. Qué hace falta

8 imanes de 5 × 1,6 mm (10 con una aguja de repuesto), un rotulador, la etiqueta NFC, un clip, PLA blanco, azul y mármol, y PETG para la pinza.

## 2. La regla de los imanes

**Todos con la misma cara mirando hacia el frente de la caja.** Apila los imanes en una torre y marca con el rotulador la cara de arriba de cada uno.

**Comprobación, siempre antes de tapar un imán:** acerca la torre al imán puesto, con la marca de la torre mirando hacia el mismo lado que debe mirar la del imán. Tiene que atraer.

## 3. Orden de impresión

Capa de 0,2 mm. Sin soportes. Los ficheros de `imprimir-v4\` ya vienen girados.

| Orden | Pieza | Material | Imanes y ajustes |
| --- | --- | --- | --- |
| 1 | `base.3mf` | PLA blanco | Pausa hacia los 63,5 mm de altura: 2 imanes de esquina, **marca arriba**. Va primero: si un imán queda al revés, los del panel se orientan después contra estos y no se pierde nada |
| 2 | `tapa.3mf` | PLA blanco | Cara vista en la cama. 7 capas inferiores macizas. Pausa hacia los 5,3 mm: 2 imanes de esquina, **marca abajo**. Antes de taparlos, compruébalos contra los de la base |
| 3 | `rotor.3mf` | PLA blanco | Espiral en la cama. Paredes Arachne. El grosor de espiral que haya ganado en P1 |
| 4 | `tapeta.3mf` | PLA blanco | Es la tapa trasera |
| 5 | `aguja.3mf` | PLA azul | Pausa a 2,2 mm: 2 imanes, marca arriba. Imprime tres |
| 6 | `peana.3mf` | PLA blanco | De pie |
| 7 | `pinza.3mf` | **PETG** | De canto. **Solo con el brazalete medido** |
| 8 | `funda.3mf` + `frase.3mf` | Mármol + azul | Se importan a la vez, como un objeto de dos piezas. Techo en la cama |

Las alturas de pausa salen del modelo: confírmalas en la vista previa del laminador. La pausa va justo antes de la primera capa que tapa el agujero.

## 4. Montaje del panel

Con la cara vista sobre la mesa. El borde de abajo es el de la ranura para la uña.

1. **Imán central**, en el hueco del eje, marca abajo.
2. **Imán del rotor**, por la cara de la espiral, marca a la vista.
3. **Rotor.** Espiral hacia abajo, brazo del imán hacia el borde de abajo. Mételo en el eje **girado unos 45°**: en vertical no entra, porque arriba y abajo hay dos bandas macizas. Luego gíralo hasta la vertical; las puntas pasan por debajo de las bandas.
4. **Precarga.** El taco de la espiral queda en un canal curvo. Empújalo con el clip por el canal hasta que salte un pequeño diente. Suelta: el rotor queda empujado contra su tope.
5. **Prueba.** Gira el rotor con el dedo y suéltalo. Tiene que volver al tope de golpe, con el panel de pie, tumbado y boca abajo.
6. **Tapa trasera.** Entra a presión en su hueco.
7. **Prueba con la aguja**, por la cara vista: se pega vertical, gira a la derecha hasta el tope, se queda; al quitarla, el rotor vuelve.
8. **Tarjeta**, por arriba entre los carriles, hasta los topes. Los resaltes la pellizcan.

## 5. Montaje de la caja

1. **Reloj en la pinza, fuera de la caja.** Aprieta la pinza, pásale el brazalete cerrado y suelta.
2. **Pinza en la peana, también fuera.** Baja a las dos cunas.
3. **El bloque entero a la caja.** Desliza la peana entre las dos guías hasta el clic del fondo.
4. **Panel.** Pon la aguja y gírala hasta el tope. Mete el panel hasta que quede a ras. Quita la aguja. Tira del panel: no tiene que salir. Si entra al revés no llega a ras: dale la vuelta.
5. **Aguja** en su rebaje, punta hacia el frente. Entra con un poco de roce.
6. **NFC** en el rebaje redondo de dentro del techo de la funda.
7. **Funda.** Baja hasta que los nervios hagan clic.

## 6. Para sacar el reloj

Tira del reloj hacia ti. Sale con la pinza y la peana.

## 7. Si no abre

- **Se ha perdido la aguja:** dos imanes pegados a un palito, separados 16 mm, abren igual.
- **El pestillo está atascado:** en la base de la caja, cerca del frente, hay una ranura. Mete el clip a la derecha del pestillo (mirando la caja de frente) y arrástralo hacia la izquierda unos 2 cm mientras tiras del panel.

## 8. Aviso para Pablo

La aguja lleva dos imanes. Que no la deje sobre el reloj.
