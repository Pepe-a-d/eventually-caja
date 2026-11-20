# Cálculos de los contra-reportes (sesión del Mac)

Son los programas con los que la sesión del Mac comprobó las cifras de los reportes de la v3, la v4 y el parche v4.1. Están tal cual se usaron: son cuadernos de cálculo, no un programa acabado. Sirven para repetir una cifra de un contra-reporte o para medir una pieza nueva.

## Cómo se usan

Hace falta Python 3 con `numpy`. Cada programa se lanza desde su carpeta y escribe una tabla en pantalla:

```
cd calculos-mac/v4.1
python m1.py
```

Los que miden piezas leen los `.3mf` de `probetas-v4/`. Los que calculan imanes usan `reporte-v3/imanes.py`. Las rutas son relativas al repositorio: funcionan igual en el Mac y en el PC.

**Ojo:** `probetas-v4/` contiene ahora las piezas del parche v4.1. Los programas de `v4/` se escribieron para las de la v4 sin parchear. Para repetir sus cifras hay que volver a ese estado: `git checkout 4874e30 -- probetas-v4` (y `git checkout main -- probetas-v4` para deshacerlo).

## Qué hay en cada carpeta

### `v3/` — contra-reporte de la v3

| Fichero | Qué calcula |
| --- | --- |
| `geo.py` | Geometría de la v2: anillo, reloj, pestillo, gravedad, tarjeta |
| `imanes.py` | Fuerza entre dos imanes de 5 × 1,6 mm (N35, 1,2 T): tirón de frente y arrastre de lado |
| `v3.py` | Resbalón, muelle y forma real de la pinza con el brazalete puesto |
| `v3b.py` | Apertura de emergencia, salida de la pinza, caída de la funda, carga del pestillo, imanes y calor |
| `v3c.py`, `v3d.py` | Por qué el cierre de un empujón se acuña; pico basculante; muelle con tope y precarga |

### `v4/` — contra-reporte de la v4

| Fichero | Qué calcula |
| --- | --- |
| `malla.py` | Lector de `.3mf` y rayos sobre la malla. Lo usan los demás |
| `emerg.py` | La ranura de emergencia no llegaba al pestillo (medido en el aro de la boca) |
| `espiral.py` | El diente no retenía el taco de la espiral |
| `resto.py` | Puentes del panel, peana corredera, retén de la funda, la aguja como tirador |

### `v4.1/` — contra-reporte del parche v4.1

| Fichero | Qué calcula |
| --- | --- |
| `malla.py` | El mismo lector |
| `m1.py` | Ranura de emergencia: por dónde pasa el clip y cuándo suelta el pestillo |
| `m2.py` | Tapa trasera (pestaña y clip), rebaje de las puntas del rotor |
| `m3.py` | Peana y rebanada de caja: lengüetas, muescas y chaflanes de las guías |
| `m4.py` | Tira del suelo sobre la ranura pasante, rozamiento del rotor tumbado, retención de la lengüeta |
| `m5.py` | Ventana de giro para meter el rotor (arranque del canal contra el taco) |
| `esp.py` | Primer intento de la espiral. **No converge a partir de 68°: no usar.** Se queda como referencia |
| `esp2.py` | Espiral con el taco en su tetón: par, giro del taco, fuerza en el tetón, deformación |
| `funda.py` | Rigidez de la pared de la funda (elementos finitos de placa) y fuerza del retén; imanes de esquina |

## Cómo se mide una pieza

`carga(fichero)` devuelve vértices y triángulos. `rayo(V, T, origen, dirección)` devuelve los puntos donde un rayo corta la malla. Entre el corte 1 y el 2 hay plástico, entre el 2 y el 3 hay aire, y así sucesivamente.

Las piezas están giradas para imprimir. Para pasar de las cotas del generador a las de la malla:

- Piezas con el **frente arriba**: (x, y + 46,34, z − 35,69)
- Piezas con el **frente abajo**: (x, −(y + 46,34), 35,69 − z)

Estas cifras salen de la v4.1. Si cambia el tamaño de la caja, cambian.
