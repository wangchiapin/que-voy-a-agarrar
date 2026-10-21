# ¿Qué voy a agarrar? · 我要拿什麼？

Juego de chino: escucha la frase, camina por la casa y elige el objeto correcto.
Un solo archivo (`index.html`), sin dependencias; se abre directamente o en GitHub Pages.

## Qué es

Cada partida genera una casa distinta (cocina, dormitorio, baño, estudio, sala...). El juego dice una frase en chino, por ejemplo "我要到廚房的碗櫃拿筷子" ("voy al armario de la cocina a tomar los palillos"). El jugador toca el mapa para caminar hasta el lugar indicado y después elige el objeto correcto entre tres. La voz usa siempre `speechSynthesis` con `zh-TW`.

## Niveles

1. **Las habitaciones (認識房間)**: ir a la habitación correcta y tomar el objeto.
2. **Ir al mueble (走到家具)**: ir junto al mueble correcto (nevera, escritorio, sofá...) y tomar el objeto.
3. **Palabras de lugar (加上方位詞)**: al lado, delante, detrás, izquierda y derecha se caminan en el mapa; encima, debajo y dentro se eligen en una lista. Algunas preguntas tienen dos paradas.

Cada nivel tiene 10 preguntas. El nivel siguiente se desbloquea con 2 estrellas en el anterior.

## Puntuación

- 3 corazones; cada error quita uno. Sin corazones se pierde el nivel.
- Estrellas según la precisión a la primera: 90 % o más = 3, 70 % o más = 2, menos = 1.
- Combo: x1.5 con 3 preguntas seguidas sin error, x2 con 5.
- Modo escucha (聽力模式, sin mostrar la frase): puntos x1.5.
- Pista: 3 por partida; un paso con pista da la mitad de puntos. Bonus de 5 puntos por pregunta rápida sin errores ni pistas.

## Ajustes

Compartidos con los demás juegos (clave `localStorage` `hanziGames.settings`, formato `{v:1, script, lang, phon, rate}`; al guardar se conservan los campos de otros juegos):

| Ajuste | Valores | Efecto |
| --- | --- | --- |
| `script` | trad / simp | Caracteres tradicionales o simplificados (frase y textos de la interfaz en chino) |
| `lang` | es / en / zh | Idioma de la interfaz y de la traducción. `zh` = solo chino, sin traducciones |
| `phon` | pinyin / zhuyin / both / off | Lectura sobre cada carácter |
| `rate` | slow / normal / fast | Velocidad de voz 0.45 / 0.65 / 0.85 |

Solo de este juego (clave `homefetch_map_v1`, junto con el progreso y el nombre): modo escucha, textos del mapa (solo habitaciones / todo) y sonido.

Si la clave compartida no existe, la primera vez se migran los ajustes antiguos de `homefetch_map_v1`. Los cambios hechos en otro juego o pestaña se aplican aquí al instante (evento `storage`). Si el dispositivo no tiene voz en chino, aparece un aviso.

## Clasificación

Ranking en línea conectado al proyecto de Firebase `memorma-24dab` (compartido con Memorama y Ordena el Armario), con inicio de sesión anónimo: colecciones `homefetchmap_L1` … `homefetchmap_L9` (por ahora se usan L1 a L3), un documento por dispositivo y nivel con la mejor puntuación, y se muestran los 10 mejores. Si no se puede conectar, el juego usa un ranking local por nivel en este navegador (clave `hfm_board_L{nivel}`). La configuración está en la constante `FIREBASE_CONFIG` de `index.html`.

Desde 2026-10-21 también se registran visitas, inicios y partidas terminadas (colecciones `visits` y `plays` del mismo proyecto; GA no cambia).

## Prueba rápida

`index.html?seed=123` fija la casa; `&fast=1` acelera la caminata (útil para pruebas).
