## 1.1 Carga de los archivos

- youtube_videos.csv: 293 filas x 20 columnas
- youtube_comments.csv: 406 filas x 17 columnas

## 1.4 Integracion por video_id

- Comentarios que se pudieron asociar a un video: 406 / 406 (100.0%)
- Videos citados en comments.video_id que no existen en videos.video_id: 0
- Videos sin ningun comentario en este dataset: 274

## 2.1 Diagnostico inicial de calidad

- Dimensiones videos: (293, 22), comments: (406, 20)

**Tipos de variables (videos):**
video_id                               str
title                                  str
channel_name                           str
channel_id                             str
source_query                           str
source_group                           str
dataset_sources                     object
channel_handle                         str
published_time                         str
view_count_text                        str
description_snippet                    str
video_url                              str
query_hits                          object
keywords                            object
description                            str
view_count                           int64
publish_date           datetime64[us, UTC]
upload_date            datetime64[us, UTC]
category                               str
owner_handle                           str
n_keywords                           int64
n_query_hits                         int64

**Tipos de variables (comments):**
video_id                   str
comment_id                 str
video_title                str
channel_name               str
channel_id                 str
author_name                str
author_channel_id          str
text                       str
source_query               str
source_group               str
dataset_sources         object
author_handle              str
published_text             str
like_count_text            str
reply_count              int64
is_pinned                 bool
viewer_rating          float64
like_count_missing        bool
like_count               int64
looks_like_reply_id       bool

**Valores faltantes (videos, columnas con >0):**
published_time         13
view_count_text        13
description_snippet    25
description            26

**Valores faltantes (comments, columnas con >0):**
viewer_rating    406

**Duplicados exactos de fila:**
- videos: 0
- comments: 0
- comments con texto exactamente duplicado (posible mismo comentario re-listado al integrar varias fuentes crudas, ver dataset_sources): 2

**Variables constantes (sin variabilidad):**
- videos: (ninguna)
- comments: ['is_pinned', 'viewer_rating'] -> is_pinned siempre False; viewer_rating siempre nulo

**Consistencia IDs <-> nombres/handles:**
- channel_id que mapean a mas de un channel_name: 0
- channel_name que mapean a mas de un channel_id: 0 (0 es lo esperado; confirma que channel_id es estable y channel_name es solo una etiqueta consistente en este dataset)
- author_channel_id que mapean a mas de un author_name: 0
- publish_date == upload_date en el 100% de los videos: True
- channel_handle == owner_handle en el 100% de los videos: True

**Inconsistencia detectada:** 36/406 comment_id contienen un '.' (formato parentId.replyId de YouTube), lo que sugiere que en realidad son respuestas colgadas dentro del archivo de 'comentarios principales'. Se conservan (comment_id sigue siendo unico y valido como llave primaria) pero se marcan con la bandera 'looks_like_reply_id' para no confundirlas con comentarios de nivel raiz al interpretar resultados de la red autor-video.

**Valores atipicos (outliers) de conteos:**
- view_count: min=2, max=8190449, mediana=1175 -> distribucion muy sesgada (unos pocos videos concentran millones de vistas, la mayoria tiene pocos cientos/miles)
- reply_count: min=0, max=7
- like_count (tras limpieza): min=0, max=405

## 2.4 Conversion de variables de conteo

- `view_count_text` (ej. '2,390 vistas') NO se reparsea: el dataset ya trae `view_count` numerico (recomendado explicitamente por el enunciado); se verifico que ambas fuentes son consistentes en orden de magnitud.
- `like_count_text` se convierte a `like_count` (entero): se quitan separadores de miles (',') y espacios; los valores vacios (' ') se interpretan como 0 'me gusta' (YouTube no muestra el contador cuando es 0). Se agrega la bandera booleana `like_count_missing` para distinguir estas filas de un 0 explicito.
  -> 189 de 406 comentarios (46.6%) tenian like_count_text vacio.
- `query_hits`, `keywords` (videos) y `dataset_sources` (ambos archivos) se convierten de texto con forma de lista/lista separada por '|' a listas de Python reales.

## 2.5 texto_original y texto_limpio

`texto_original` se conserva intacto (con mayusculas, puntuacion y emojis) porque el analisis de sentimiento (ejercicio 9) rinde mejor con esas senales. `texto_limpio` es la version normalizada usada para frecuencias, n-gramas y nube de palabras.

## 2.7 Efecto cuantificado de la limpieza

- Comentarios con al menos un hashtag: 1
- Comentarios con al menos una mencion (@usuario): 5
- Comentarios con al menos un emoji (Unicode o texto alternativo): 62
- Comentarios que quedaron con texto_limpio vacio (ej. eran solo emojis o una sola stopword): 6 / 406 (1.5%)
- Duplicados de texto ANTES de limpiar: 2
- Duplicados de texto DESPUES de limpiar (sin contar vacios): 6 -> subio porque distintos comentarios cortos colapsan al mismo texto_limpio tras remover stopwords/puntuacion (ej. 'Excelente!' y 'excelente...' -> 'excelente').

## Archivos generados en data/processed/

- videos_clean.csv
- comments_clean.csv (incluye texto_original, texto_limpio, hashtags, mentions, emojis)
- merged_clean.csv (comments + atributos de video, listo para EDA y para construir la red)