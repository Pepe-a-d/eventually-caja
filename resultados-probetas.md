# Eventually, la caja: resultados de las probetas

Lo que han dicho las piezas impresas. Cada resultado lleva la fecha y quién lo midió.

## P0. Tolerancias (20 de noviembre de 2026)

Impresa y probada por Pepe en la Bambu Lab X1 Carbon. Ficheros de `probetas-v4\` (v4.1). Tira colocada con la esquina cortada abajo a la izquierda.

| Qué | Resultado de la probeta | Valor del modelo | ¿Hay que cambiar algo? |
| --- | --- | --- | --- |
| Alojamiento del imán | El tercero: **5,15 mm**. Entra apretando y no se cae | `iman_aloj_d` = 5,15 mm | No |
| Holgura | Con **0,10 mm** por lado la barrita entra y se queda sujeta. Con **0,15 mm** pasa sin forzar. Con 0,20 a 0,35 mm pasa holgada | `holg_tapa` = 0,20 mm · `holg_desliza` = 0,30 mm · `holg_presion` = 0,15 mm | No (ver notas) |
| Piel | Con **0,8 mm**, la más fina, ya no se ve la sombra del imán | `tapa_piel` = 1,4 mm | No (ver notas) |
| Imán embutido con pausa | Se quedó en su sitio al reanudar | — | No |

**Sin probar:** la fuerza del imán embutido frente a uno suelto (la prueba de los clips). Pepe decidió no hacerla. Queda sin saber si el calor de la impresión le quita fuerza.

### Notas (interpretación de la sesión del Mac)

- **El modelo es más holgado de lo que la impresora necesita.** El plan pedía `holg_tapa` = la ventana más justa que pasa (0,15) y `holg_desliza` una más (0,20). El modelo lleva 0,20 y 0,30. No se cambia: el panel entra seguro. Si en P2 el panel baila en la boca, hay margen para bajar a 0,15.
- **`holg_presion` = 0,15 mm no aprieta en esta impresora:** con 0,15 la barrita pasa sin forzar. Un encaje que tenga que sujetar por presión necesita 0,10. Hoy solo afecta al contorno de la tapa trasera, que no se sujeta por presión sino con su pestaña (y cinta en P1, porque el clip no retiene: contra-reporte v4.1, I1).
- **La piel tiene 0,6 mm de margen.** Si en P1 la aguja no arrastra el rotor, se puede bajar `tapa_piel` de 1,4 hasta 0,8 mm sin que se vea el imán. La prueba se hizo con luz normal, no a contraluz, y con un imán: no con el mecanismo entero detrás.
- **Conclusión: P1 y el aro de P2 se imprimen con los ficheros que ya hay.** No hace falta regenerar nada.
