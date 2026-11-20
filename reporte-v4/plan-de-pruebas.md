# Eventually, la caja v4: plan de pruebas

Es el plan corregido del contra-reporte de la v3 (su apartado 9), con los ficheros de la v4 **parcheada (v4.1)** y las correcciones del contra-reporte de la v4. Todos están en `probetas-v4\`, ya orientados.

En las probetas los imanes no se pegan: entran a presión y se sacan con un clip por el taladro de detrás.

| Orden | Qué | Ficheros | Vale si |
| --- | --- | --- | --- |
| 1 | **Medir el reloj** | Tira de papel y calibre | Tienes: contorno interior del brazalete cerrado, ancho con corona, ancho y grosor del brazalete, ancho por fuera de las asas, tipo y grosor del cierre |
| 2 | **P0** tolerancias | `p0-tolerancias`, `p0-llave`, `p0-iman-embutido` | Eliges alojamiento de imán, holgura y piel. El imán embutido con pausa levanta los mismos clips que uno suelto |
| 3 | **P1** llave | `p1-panel`, `p1-tapa-trasera`, `p1-rotor-muelle-fino`, `-medio`, `-grueso`, `p1-aguja-de-prueba` | La aguja arrastra 10 de 10, de pie, tumbado y boca abajo, con menos de 10° de retraso. La aguja girada se queda. Al quitarla, el rotor vuelve **al tope** en las tres posturas, **también después de 20 giros completos de la aguja**, y el taco sigue en su tetón. La tapa trasera se queda puesta al sacar la tarjeta. Te quedas con el muelle **más grueso** que deje la aguja girada |
| 4 | **P2** cierre con la aguja | `p2-aro-de-la-boca` y el panel de P1 | Cerrar girando la aguja de vuelta funciona 10 de 10. Cerrado, aguanta 2 kg colgados del panel. Un clip por la ranura de la base lo abre. Tirando de la aguja sale el panel |
| 5 | **P2** empujón (opcional) | `p2-rotor-articulado` en el mismo panel | Cierra de un empujón 20 de 20 y aguanta los 2 kg. Si no, la caja se queda con el rotor rígido y no pasa nada |
| 6 | **P3** soporte | `p3-pinza` (PETG), `p3-peana`, `p3-rebanada-de-caja` | El reloj real entra y sale tirando de él, con una mano, sin tocar el techo. La peana aguanta boca abajo y sale tirando con un dedo. La pinza tensa el brazalete y su punta no toca el reloj |
| 7 | **P4** funda | `p4-funda-corta` con `p4-frase`, `p4-vaso-para-lastrar` | La frase se lee. Con el vaso lastrado a 260 g (monedas), cogida por la funda la caja no cae. Con un tirón suave sale, y baja en más de 2 s. El móvil lee el NFC con el reloj, o una cuchara, debajo. **Ojo:** la funda corta es casi el doble de rígida que la entera y retiene casi el doble (**del contra-reporte**); si el filamento lo permite, prueba con la funda entera |

**P3 no se imprime sin el paso 1:** la pinza y la rebanada dependen de la medida.

**Sin el reloj montado** se pueden hacer los pasos 2, 3, 4, 5 y 7.

## Si falla

| Qué pasa | Qué tocar en `P_DEF` |
| --- | --- |
| El rotor no gira ni con el dedo | Subir `muelle_holgura` de 0,6 a 0,8 |
| La aguja no arrastra | Bajar `tapa_piel` o alargar `rotor_radio_iman` |
| El rotor no vuelve al tope | **Mira primero si el taco sigue en su tetón.** Solo después: muelle más grueso o más `muelle_precarga` |
| La aguja no se queda girada | Muelle más fino; bajar `muelle_precarga` |
| La aguja se suelta antes de sacar el panel | Subir `iman_cubierta`; si no basta, quitar los imanes de esquina |
| El panel se cae solo | Bajar `iman_cubierta` |
| La peana no hace clic o cuesta sacarla | `lengueta_resalte`, `lengueta_grosor` |
| La funda no retiene, o cuesta sacarla | `reten_funda_sale`, `reten_funda_rebaje` |
| La funda cae de golpe | Bajar `holg_desliza` |
| La tapa trasera se suelta | Subir `tapeta_clip_resalte` |
| El rotor articulado se atasca | No retocar el bracito: que el pico no roce la piel, o un chaflán más tendido (`rotor_chaflan`) |
