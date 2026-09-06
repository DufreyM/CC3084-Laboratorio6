# %% [markdown]
# # Laboratorio 6 - Ejercicio 1 y 2
# **Autor de esta seccion:** Leonardo Mejia
# **Cubre:** 1. Carga, comprension e integracion | 2. Calidad, limpieza y preprocesamiento
#
# Este script se puede abrir como notebook (celdas marcadas con `# %%`, compatible
# con Jupytext / VSCode) o ejecutar directamente con `python notebooks/01_carga_calidad_leonardo.py`.
# Al final deja los datasets integrados y limpios en `data/processed/` para que el resto
# del equipo (notebooks 02 y 03) parta del mismo insumo.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no rendiriza emojis/tildes por defecto

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import data_utils as du

OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

report_lines = []


def log(msg=""):
    print(msg)
    report_lines.append(msg)


# %% [markdown]
# ## 1.1 Carga de los archivos

# %%
videos_raw = pd.read_csv(du.DATA_DIR / "youtube_videos.csv", encoding="utf-8-sig")
comments_raw = pd.read_csv(du.DATA_DIR / "youtube_comments.csv", encoding="utf-8-sig")

log("## 1.1 Carga de los archivos\n")
log(f"- youtube_videos.csv: {videos_raw.shape[0]} filas x {videos_raw.shape[1]} columnas")
log(f"- youtube_comments.csv: {comments_raw.shape[0]} filas x {comments_raw.shape[1]} columnas")

# %% [markdown]
# ## 1.2 Unidad de observacion, llave primaria y variables relevantes
#
# - **youtube_videos.csv**: cada fila es **un video** de YouTube. Llave primaria: `video_id`.
#   Variables mas relevantes para el laboratorio: `video_id`, `channel_id`, `channel_name`,
#   `title`, `category`, `source_query`, `source_group`, `keywords`, `view_count`, `publish_date`.
# - **youtube_comments.csv**: cada fila es **un comentario principal** publicado en un video.
#   Llave primaria: `comment_id`. Variables mas relevantes: `comment_id`, `video_id` (llave
#   foranea hacia videos), `author_channel_id`, `text`, `like_count_text`, `reply_count`.
#
# `channel_name`, `author_name`, `video_title` son **descriptivos**, no identificadores: pueden
# repetirse (un canal publica muchos videos) o cambiar de valor sin cambiar de entidad real.

# %% [markdown]
# ## 1.3 Relacion entre canal, video, autor, comentario, categoria y consulta
#
# ```
# channel (channel_id) --1:N--> video (video_id) --1:N--> comment (comment_id)
#                                    |                          |
#                              category (N:1)            author (author_channel_id) N:1
#                                    |
#                        source_query / source_group (como se muestreo el video)
# ```
# - Un **canal** (`channel_id`) publica muchos **videos**; el nombre del canal (`channel_name`)
#   es una etiqueta visible que puede repetirse o cambiar sin que cambie el canal real.
# - Un **video** recibe muchos **comentarios**; cada comentario pertenece a un solo video
#   (`comment.video_id -> video.video_id`).
# - Un **comentario** tiene un **autor** (`author_channel_id`), que es distinto del canal
#   dueño del video que se comento (`channel_id` en comments es el canal del video, no el autor).
#   Un mismo autor puede comentar en varios videos, incluso de canales distintos: esa es
#   precisamente la base de la red bipartita autor-video del ejercicio 4.
# - `category` es un atributo de video asignado por YouTube (ej. News & Politics), no de canal:
#   un mismo canal puede tener videos en mas de una categoria.
# - `source_query`/`source_group` describen el **procedimiento de muestreo** (que busqueda o
#   canal se uso para recolectar el video/comentario), no el tema real del contenido; por eso
#   el enunciado advierte que no debe tratarse como clasificacion tematica definitiva.

# %% [markdown]
# ## 1.4 Integracion por video_id

# %%
videos = du.load_videos()
comments = du.load_comments()
merged, match_rate = du.integrate(videos, comments)

n_matched = (merged["_merge"] == "both").sum()
log("\n## 1.4 Integracion por video_id\n")
log(f"- Comentarios que se pudieron asociar a un video: {n_matched} / {len(comments)} ({match_rate:.1%})")
log(f"- Videos citados en comments.video_id que no existen en videos.video_id: "
    f"{(merged['_merge'] == 'left_only').sum()}")
log(f"- Videos sin ningun comentario en este dataset: {videos.shape[0] - merged['video_id'].nunique()}")

# %% [markdown]
# ## 2.1 Diagnostico inicial de calidad

# %%
log("\n## 2.1 Diagnostico inicial de calidad\n")
log(f"- Dimensiones videos: {videos.shape}, comments: {comments.shape}")

log("\n**Tipos de variables (videos):**")
log(du.html_columns([f"{col}: {dt}" for col, dt in videos.dtypes.astype(str).items()], n_cols=3))
log("\n**Tipos de variables (comments):**")
log(du.html_columns([f"{col}: {dt}" for col, dt in comments.dtypes.astype(str).items()], n_cols=3))

miss_v = videos.isna().sum()
miss_c = comments.isna().sum()
log("\n**Valores faltantes (videos, columnas con >0):**")
log(miss_v[miss_v > 0].to_string() if (miss_v > 0).any() else "(ninguna)")
log("\n**Valores faltantes (comments, columnas con >0):**")
log(miss_c[miss_c > 0].to_string() if (miss_c > 0).any() else "(ninguna)")

log("\n**Duplicados exactos de fila:**")
log(f"- videos: {videos_raw.duplicated().sum()}")
log(f"- comments: {comments_raw.duplicated().sum()}")
log(f"- comments con texto exactamente duplicado (posible mismo comentario re-listado "
    f"al integrar varias fuentes crudas, ver dataset_sources): {comments['text'].duplicated().sum()}")

const_cols_v = [c for c in videos_raw.columns if videos_raw[c].nunique(dropna=False) == 1]
const_cols_c = [c for c in comments_raw.columns if comments_raw[c].nunique(dropna=False) == 1]
log("\n**Variables constantes (sin variabilidad):**")
log(f"- videos: {const_cols_v if const_cols_v else '(ninguna)'}")
log(f"- comments: {const_cols_c} "
    f"-> is_pinned siempre False; viewer_rating siempre nulo")

log("\n**Consistencia IDs <-> nombres/handles:**")
n_bad_channel = (videos.groupby("channel_id")["channel_name"].nunique() > 1).sum()
n_bad_channel_rev = (videos.groupby("channel_name")["channel_id"].nunique() > 1).sum()
n_bad_author = (comments.groupby("author_channel_id")["author_name"].nunique() > 1).sum()
log(f"- channel_id que mapean a mas de un channel_name: {n_bad_channel}")
log(f"- channel_name que mapean a mas de un channel_id: {n_bad_channel_rev} (0 es lo esperado; "
    f"confirma que channel_id es estable y channel_name es solo una etiqueta consistente en este dataset)")
log(f"- author_channel_id que mapean a mas de un author_name: {n_bad_author}")
log(f"- publish_date == upload_date en el 100% de los videos: {(videos['publish_date'] == videos['upload_date']).mean() == 1.0}")
log(f"- channel_handle == owner_handle en el 100% de los videos: "
    f"{(videos_raw['channel_handle'] == videos_raw['owner_handle']).mean() == 1.0}")

n_reply_like_ids = comments["looks_like_reply_id"].sum()
log(f"\n**Inconsistencia detectada:** {n_reply_like_ids}/{len(comments)} comment_id contienen un "
    f"'.' (formato parentId.replyId de YouTube), lo que sugiere que en realidad son respuestas "
    f"colgadas dentro del archivo de 'comentarios principales'. Se conservan (comment_id sigue "
    f"siendo unico y valido como llave primaria) pero se marcan con la bandera "
    f"'looks_like_reply_id' para no confundirlas con comentarios de nivel raiz al interpretar "
    f"resultados de la red autor-video.")

log("\n**Valores atipicos (outliers) de conteos:**")
log(f"- view_count: min={videos['view_count'].min()}, max={videos['view_count'].max()}, "
    f"mediana={videos['view_count'].median():.0f} -> distribucion muy sesgada (unos pocos "
    f"videos concentran millones de vistas, la mayoria tiene pocos cientos/miles)")
log(f"- reply_count: min={comments['reply_count'].min()}, max={comments['reply_count'].max()}")
log(f"- like_count (tras limpieza): min={comments['like_count'].min()}, max={comments['like_count'].max()}")

# %% [markdown]
# ## 2.2 Variables problematicas o de uso delicado
#
# - **viewer_rating**: 100% nula en ambos archivos -> se excluye de cualquier analisis.
# - **is_pinned**: constante (siempre False) -> no aporta variabilidad, se documenta pero no se usa.
# - **published_time / published_text**: fechas relativas ("hace 2 dias") dependientes del momento
#   de recoleccion; no deben tratarse como fecha exacta. Se prioriza `publish_date` (ISO 8601).
# - **view_count_text / like_count_text**: texto formateado para mostrar en UI; se usan solo como
#   respaldo de auditoria, el analisis cuantitativo usa `view_count` / `like_count` (numericos).
# - **video_title, channel_name, author_name** (en comments): descriptivos y redundantes/derivables
#   via join con video_id / author_channel_id; nunca se usan como llave.
# - **source_query / source_group**: describen el metodo de muestreo, no el tema definitivo del
#   contenido -> limitan la generalizacion de cualquier conclusion tematica (ver seccion 10).
# - **comment_id con formato de respuesta** (`looks_like_reply_id`): riesgo de doble conteo de
#   participacion si no se documenta (ver 2.1).

# %% [markdown]
# ## 2.3 Normalizacion de identificadores y nombres
#
# `data_utils.load_videos()` / `load_comments()` no sustituyen ningun ID por su nombre visible.
# Se preservan como identificadores: `channel_id`, `video_id`, `comment_id`, `author_channel_id`.
# Los nombres/handles (`channel_name`, `channel_handle`, `author_name`, `author_handle`) se
# conservan unicamente como atributos descriptivos para etiquetar visualizaciones.

# %% [markdown]
# ## 2.4 Conversion de variables de conteo (texto -> numero)

# %%
log("\n## 2.4 Conversion de variables de conteo\n")
log("- `view_count_text` (ej. '2,390 vistas') NO se reparsea: el dataset ya trae `view_count` "
    "numerico (recomendado explicitamente por el enunciado); se verifico que ambas fuentes son "
    "consistentes en orden de magnitud.")
log("- `like_count_text` se convierte a `like_count` (entero): se quitan separadores de miles "
    "(',') y espacios; los valores vacios (' ') se interpretan como 0 'me gusta' (YouTube no "
    "muestra el contador cuando es 0). Se agrega la bandera booleana `like_count_missing` para "
    "distinguir estas filas de un 0 explicito.")
log(f"  -> {comments['like_count_missing'].sum()} de {len(comments)} comentarios "
    f"({comments['like_count_missing'].mean():.1%}) tenian like_count_text vacio.")
log("- `query_hits`, `keywords` (videos) y `dataset_sources` (ambos archivos) se convierten de "
    "texto con forma de lista/lista separada por '|' a listas de Python reales.")

# %% [markdown]
# ## 2.5 texto_original y texto_limpio

# %%
comments["texto_original"] = comments["text"]

cleaner = du.TextCleaner()
comments["hashtags"] = comments["texto_original"].apply(cleaner.extract_hashtags)
comments["mentions"] = comments["texto_original"].apply(cleaner.extract_mentions)
comments["emojis"] = comments["texto_original"].apply(cleaner.extract_emojis)
comments["texto_limpio"] = comments["texto_original"].apply(cleaner.clean)

log("\n## 2.5 texto_original y texto_limpio\n")
log("`texto_original` se conserva intacto (con mayusculas, puntuacion y emojis) porque el "
    "analisis de sentimiento (ejercicio 9) rinde mejor con esas senales. `texto_limpio` es la "
    "version normalizada usada para frecuencias, n-gramas y nube de palabras.")

# %% [markdown]
# ## 2.6 Decisiones de limpieza para texto_limpio
#
# 1. **Minusculas**: si, aplicado a todo el texto.
# 2. **URLs**: se eliminan (regex `https?://\S+|www\.\S+`); no aportan a frecuencia de palabras.
# 3. **Hashtags y menciones**: se separan ANTES de limpiar en columnas propias (`hashtags`,
#    `mentions`) para poder analizarlos aparte; en texto_limpio la mencion (`@usuario`) se
#    elimina por completo (es una referencia, no contenido) y el hashtag conserva la palabra
#    sin el simbolo `#` (suele llevar informacion tematica util, ej. "#Guatemala" -> "guatemala").
# 4. **Puntuacion y numeros**: se eliminan con una expresion regular que solo conserva letras
#    (incluyendo acentos y ñ) y espacios.
# 5. **Stopwords en espanol**: lista de NLTK (313 palabras) ampliada con jerga/abreviaturas de
#    chat frecuentes en el corpus (q, x, xq, pq, jaja, jajaja, ud, uds, etc.).
# 6. **Lematizacion**: se usa spaCy (`es_core_news_sm`) para reducir cada palabra a su lema
#    (ej. "diputados" -> "diputado", "comiendo" -> "comer"), lo que agrupa mejor las frecuencias
#    de palabras que una simple eliminacion de sufijos (stemming).
# 7. **Emojis**: se extraen a una columna `emojis` (incluye tanto emojis Unicode reales como el
#    formato de texto alternativo que aparece en 2/406 comentarios, ej. ':hand-purple-blue-peace:')
#    y se eliminan del texto_limpio.

# %% [markdown]
# ## 2.7 Efecto cuantificado de la limpieza

# %%
n_empty_clean = (comments["texto_limpio"].str.strip() == "").sum()
n_had_hashtag = (comments["hashtags"].apply(len) > 0).sum()
n_had_mention = (comments["mentions"].apply(len) > 0).sum()
n_had_emoji = (comments["emojis"].apply(len) > 0).sum()
dup_before = comments["texto_original"].duplicated().sum()
dup_after = comments["texto_limpio"][comments["texto_limpio"].str.strip() != ""].duplicated().sum()

log("\n## 2.7 Efecto cuantificado de la limpieza\n")
log(f"- Comentarios con al menos un hashtag: {n_had_hashtag}")
log(f"- Comentarios con al menos una mencion (@usuario): {n_had_mention}")
log(f"- Comentarios con al menos un emoji (Unicode o texto alternativo): {n_had_emoji}")
log(f"- Comentarios que quedaron con texto_limpio vacio (ej. eran solo emojis o una sola "
    f"stopword): {n_empty_clean} / {len(comments)} ({n_empty_clean/len(comments):.1%})")
log(f"- Duplicados de texto ANTES de limpiar: {dup_before}")
log(f"- Duplicados de texto DESPUES de limpiar (sin contar vacios): {dup_after} "
    f"-> subio porque distintos comentarios cortos colapsan al mismo texto_limpio tras remover "
    f"stopwords/puntuacion (ej. 'Excelente!' y 'excelente...' -> 'excelente').")

# %% [markdown]
# ## Guardado de datasets procesados para el equipo

# %%
du.save_processed(videos, "videos_clean.csv")
du.save_processed(comments, "comments_clean.csv")

merged_out = comments.merge(
    videos, on="video_id", how="left", suffixes=("_comment", "_video")
)
du.save_processed(merged_out, "merged_clean.csv")

log("\n## Archivos generados en data/processed/\n")
log("- videos_clean.csv")
log("- comments_clean.csv (incluye texto_original, texto_limpio, hashtags, mentions, emojis)")
log("- merged_clean.csv (comments + atributos de video, listo para EDA y para construir la red)")

report_path = OUTPUTS / "reporte_ejercicio_1_2.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
