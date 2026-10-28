# ¿Dónde lo pongo? · 我要放哪裡？

(Antes «¿Qué voy a agarrar? · 我要拿什麼？». El repositorio y la URL conservan el nombre `que-voy-a-agarrar`.)

Juego de chino: escucha la frase «我要把XX放到XX», elige el objeto correcto y llévalo por la casa hasta su lugar.
Un solo archivo (`index.html`), sin dependencias; se abre directamente o en GitHub Pages.

## Qué es

Cada partida genera una casa distinta (cocina, dormitorio, baño, estudio, sala, balcón). El juego dice una frase en chino, por ejemplo "我要把筷子放到廚房的碗櫃" ("voy a poner los palillos en el armario de la cocina"). Primero aparecen tres objetos y el jugador elige el que dice la frase; después toca el mapa para caminar con él hasta el lugar indicado. La voz usa siempre `speechSynthesis` con `zh-TW`. El mapa no lleva textos: el nombre del lugar aparece al llegar o con la pista. Al entrar en otra habitación sale un aviso «你已進入…» y al empezar «你現在在…».

La pantalla de inicio es única: el título (con un fondo de la casa del propio juego) y tres tarjetas de nivel con estrellas y mejor puntuación a la derecha; tocar una tarjeta empieza la partida. El engranaje (también dentro de la partida) abre los ajustes. En ordenador, la partida usa dos columnas: mapa a la izquierda (2/3) y frase y opciones a la derecha.

## Niveles

1. **Poner en la habitación (放到房間)**: llevar el objeto a la habitación correcta.
2. **Poner junto al mueble (放到家具旁邊)**: llevarlo junto al mueble correcto (nevera, escritorio, sofá...).
3. **Poner en el lugar exacto (放到準確位置)**: al lado, delante, detrás, izquierda y derecha se caminan en el mapa; encima, debajo y dentro se eligen entre seis imágenes (por defecto sin texto; en Ajustes se puede activar «Imagen + texto»). Algunas preguntas tienen dos paradas.

Cada nivel tiene 10 preguntas. El nivel siguiente se desbloquea con 2 estrellas en el anterior. Contenido: 6 habitaciones, 24 muebles y 34 objetos.

## Puntuación

- 3 corazones; cada error quita uno. Sin corazones se pierde el nivel.
- Estrellas según la precisión a la primera: 90 % o más = 3, 70 % o más = 2, menos = 1.
- Combo: x1.5 con 3 preguntas seguidas sin error, x2 con 5.
- Modo escucha (聽力模式, en Ajustes; sin mostrar la frase): puntos x1.5.
- Pista: 3 por partida; un paso con pista da la mitad de puntos. Bonus de 5 puntos por pregunta rápida sin errores ni pistas.

## Ajustes

Compartidos con los demás juegos (clave `localStorage` `hanziGames.settings`, formato `{v:1, script, lang, phon, rate}`; al guardar se conservan los campos de otros juegos):

| Ajuste | Valores | Efecto |
| --- | --- | --- |
| `script` | trad / simp | Caracteres tradicionales o simplificados (frase y textos de la interfaz en chino) |
| `lang` | es / en / zh | Idioma de la interfaz y de la traducción. `zh` = solo chino, sin traducciones |
| `phon` | pinyin / zhuyin / both / off | Lectura sobre cada carácter |
| `rate` | slow / normal / fast | Velocidad de voz 0.45 / 0.65 / 0.85 |

Solo de este juego (clave `homefetch_map_v1`, junto con el progreso y el nombre): modo escucha (`listen`), texto en las opciones de posición (`posTxt`: `off` = solo imagen, por defecto; `on` = imagen + texto) y sonido.

Si la clave compartida no existe, la primera vez se migran los ajustes antiguos de `homefetch_map_v1`. Los cambios hechos en otro juego o pestaña se aplican aquí al instante (evento `storage`). Si el dispositivo no tiene voz en chino, aparece un aviso.

## Clasificación

Ranking en línea conectado al proyecto de Firebase `memorma-24dab` (compartido con Memorama y Ordena el Armario), con inicio de sesión anónimo: colecciones `homefetchmap_L1` … `homefetchmap_L9` (por ahora se usan L1 a L3), un documento por dispositivo y nivel con la mejor puntuación, y se muestran los 10 mejores. Si no se puede conectar, el juego usa un ranking local por nivel en este navegador (clave `hfm_board_L{nivel}`). La configuración está en la constante `FIREBASE_CONFIG` de `index.html`.

Desde 2026-10-21 también se registran visitas, inicios y partidas terminadas (colecciones `visits` y `plays` del mismo proyecto; GA no cambia).

## Prueba rápida

`index.html?seed=123` fija la casa; `&fast=1` acelera la caminata (útil para pruebas).

## 手機瀏覽器備註：捲動後回不到頂端（2026-10-24）
iPhone 版 Chrome 上，頁面可以捲動時，往下捲之後有時回不到最上面（Safari 正常）。
處理方式（已套用在本遊戲）：
- `<meta name="viewport">` 設 `maximum-scale=1`，不使用 `viewport-fit=cover`。
- `<html>` 加 `html{color-scheme:light}`。

兩項一起改後，手機 Chrome 測試恢復正常；尚未分開測是哪一項有效。新增頁面請照這個寫。

## Pruebas (carpeta `tests/`)
- `sh tests/run_all.sh` (necesita python3, playwright y chromium). Usa Firebase falso; no toca la base real.
- `test_play_all.py`: juega los 3 niveles (modo normal y modo escucha) sin errores.
- `test_name_required.py`: sin nombre no se guarda en el ranking.
- `test_tiebreak.py`: orden del ranking (más puntos primero; con los mismos puntos, menos tiempo primero), un solo registro por dispositivo, límites de los campos.
- Ranking: los documentos `homefetchmap_L1..L3` llevan `name, score, listen, secs, updatedAt`. Las reglas de Firestore (en el repo Memorama) aceptan `secs`; si aún no se actualizaron, el juego guarda sin `secs`.

## Pronunciación y palabras compartidas (2026-10-25 a 27)
- La pronunciación (pinyin y zhuyin) sigue la tabla de reglas de **GoodTeacher** (lectura de Taiwán). Cambios recientes: 鑰匙 se lee **yào shi** (ㄧㄠˋ ˙ㄕ); 枕頭 se lee **tóu**; 洗髮精 lleva **fǎ** (3.er tono). Al agregar objetos con caracteres de varias lecturas, revisa la tabla de GoodTeacher en game-kit.
- Seis palabras se comparten con el juego 墨龍飛天: 手機 (phone), 垃圾桶 (basurero), 浴缸 (bañera), 洗髮精 (champú), 臥室 (dormitorio) y 杯子 (taza). Este juego es la referencia: si cambias una, cambia también la otra.
- En `tests/` ya no se guardan los archivos `__pycache__`; el `.gitignore` los excluye.
