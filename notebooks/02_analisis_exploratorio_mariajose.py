# %% [markdown]
# # Laboratorio 6 - Ejercicio 3: Analisis exploratorio
# **Autora de esta seccion:** Maria Jose
#
# Parte de `data/processed/merged_clean.csv` y `videos_clean.csv` (generados por
# `01_carga_calidad_leonardo.py`), no de los CSV crudos, para usar exactamente el
# mismo dataset integrado y limpio que el resto del equipo.

# %%
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import pandas as pd
from langdetect import DetectorFactory, detect
from wordcloud import WordCloud

import data_utils as du

DetectorFactory.seed = 0  # langdetect es no determinista sin esto

FIGS = ROOT / "outputs" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)
OUTPUTS = ROOT / "outputs"

report_lines = []


def log(msg=""):
    print(msg)
    report_lines.append(msg)


videos = du.load_processed("videos_clean.csv")
comments = du.load_processed("comments_clean.csv")
m = du.load_processed("merged_clean.csv")

# %% [markdown]
# ## 3.1 Descriptivos minimos

# %%
n_videos = videos["video_id"].nunique()
n_channels = videos["channel_id"].nunique()
n_comments = comments["comment_id"].nunique()
n_authors = comments["author_channel_id"].nunique()
n_videos_con_comentarios = m["video_id"].nunique()

log("## 3.1 Descriptivos minimos\n")
log(f"- Videos: {n_videos} | Canales: {n_channels} | Comentarios: {n_comments} | "
    f"Autores unicos: {n_authors}")
log(f"- De los {n_videos} videos del dataset, solo {n_videos_con_comentarios} "
    f"({n_videos_con_comentarios/n_videos:.1%}) tienen al menos un comentario en "
    f"este dataset (la recoleccion de comentarios fue selectiva, no exhaustiva).")

videos_por_canal = videos["channel_id"].value_counts()
log(f"\n**Videos por canal:** media={videos_por_canal.mean():.2f}, "
    f"mediana={videos_por_canal.median():.0f}, max={videos_por_canal.max()} "
    f"(canal con mas videos: {videos.loc[videos['channel_id']==videos_por_canal.idxmax(),'channel_name'].iloc[0]})")

por_video = m.groupby("video_id").agg(
    n_comentarios=("comment_id", "size"),
    n_autores=("author_channel_id", "nunique"),
    view_count=("view_count", "first"),
    channel_name=("channel_name_video", "first"),
    category=("category", "first"),
).reset_index()
log(f"\n**Comentarios por video** (solo los {n_videos_con_comentarios} con al menos uno): "
    f"media={por_video['n_comentarios'].mean():.1f}, mediana={por_video['n_comentarios'].median():.0f}, "
    f"max={por_video['n_comentarios'].max()}")
log(f"**Autores unicos por video:** media={por_video['n_autores'].mean():.1f}, "
    f"max={por_video['n_autores'].max()}")

log(f"\n**Visualizaciones (view_count, a nivel video):** media={videos['view_count'].mean():.0f}, "
    f"mediana={videos['view_count'].median():.0f}, max={videos['view_count'].max()}")
log(f"**Respuestas (reply_count, a nivel comentario):** media={comments['reply_count'].mean():.2f}, "
    f"max={comments['reply_count'].max()}, comentarios con >=1 respuesta: "
    f"{(comments['reply_count']>0).sum()} ({(comments['reply_count']>0).mean():.1%})")
log(f"**Me gusta (like_count):** media={comments['like_count'].mean():.2f}, "
    f"mediana={comments['like_count'].median():.0f}, max={comments['like_count'].max()}")

log("\n**Categorias de video** (nivel video vs. nivel comentario, es decir "
    "ponderado por cuantos comentarios trajo cada categoria):")
cat_video = videos["category"].value_counts()
cat_comment = m["category"].value_counts()
cat_compare = pd.DataFrame({"n_videos": cat_video, "n_comentarios": cat_comment}).fillna(0).astype(int)
cat_compare["%_videos"] = (cat_compare["n_videos"] / cat_compare["n_videos"].sum() * 100).round(1)
cat_compare["%_comentarios"] = (cat_compare["n_comentarios"] / cat_compare["n_comentarios"].sum() * 100).round(1)
log(cat_compare.sort_values("n_comentarios", ascending=False).to_string())

log("\n**Consultas de busqueda (source_query, a nivel video):**")
log(du.html_columns(
    [f"{q}: {c}" for q, c in videos["source_query"].value_counts().head(8).items()], n_cols=2
))

all_hashtags = [h for row in comments["hashtags"] for h in row]
log(f"\n**Hashtags:** {len(all_hashtags)} hashtags en total, en "
    f"{(comments['hashtags'].apply(len) > 0).sum()} de {len(comments)} comentarios "
    f"(el corpus casi no usa hashtags propios; los que aparecen vienen sobre todo de "
    f"las descripciones/titulos de video, no de los comentarios de la audiencia).")
if all_hashtags:
    log(Counter(all_hashtags).most_common(10))

all_tokens = [tok for text in m["texto_limpio"].dropna() for tok in text.split()]
word_freq = Counter(all_tokens)
log(f"\n**Palabras mas frecuentes (texto_limpio, {len(all_tokens)} tokens en total):**")
log(du.html_columns([f"{w}: {c}" for w, c in word_freq.most_common(15)], n_cols=3))

bigram_freq = Counter()
for text in m["texto_limpio"].dropna():
    toks = text.split()
    for i in range(len(toks) - 1):
        bigram_freq[f"{toks[i]} {toks[i+1]}"] += 1
log("\n**Bigramas mas frecuentes:**")
log(du.html_columns([f"{b}: {c}" for b, c in bigram_freq.most_common(15)], n_cols=2))

# %% [markdown]
# ## 3.2 Concentracion de la participacion

# %%
top_n = 10
top_videos = por_video.sort_values("n_comentarios", ascending=False)
share_top10_videos = top_videos.head(top_n)["n_comentarios"].sum() / top_videos["n_comentarios"].sum()

por_canal = m.groupby("channel_name_video")["comment_id"].size().sort_values(ascending=False)
share_top3_canales = por_canal.head(3).sum() / por_canal.sum()

log("\n## 3.2 Concentracion de la participacion\n")
log(f"- Los {top_n} videos con mas comentarios (de {n_videos_con_comentarios} con al menos uno, "
    f"de {n_videos} en total) concentran el {share_top10_videos:.1%} de todos los comentarios.")
log(f"- Los 3 canales con mas comentarios ({', '.join(por_canal.head(3).index)}) concentran el "
    f"{share_top3_canales:.1%} de todos los comentarios, de solo {por_canal.shape[0]} canales "
    f"con algun comentario (de {n_channels} canales en total).")
log("- Conclusion: la participacion observada NO esta repartida entre los 293 videos del "
    "dataset, sino extremadamente concentrada en un puñado de videos/canales; cualquier "
    "conclusion sobre 'la audiencia de YouTube en Guatemala' debe leerse como participacion "
    "en ese pequeño subconjunto, no como muestra representativa (ver seccion 10, limitaciones).")

# %% [markdown]
# ## 3.3 Popularidad (visualizaciones) vs. participacion (comentarios)

# %%
corr_spearman = por_video[["view_count", "n_comentarios"]].corr(method="spearman").iloc[0, 1]
corr_pearson = por_video[["view_count", "n_comentarios"]].corr(method="pearson").iloc[0, 1]
log("\n## 3.3 Popularidad vs. participacion\n")
log(f"- Correlacion de Spearman (por rango) entre view_count y numero de comentarios, a nivel "
    f"video (solo los 19 con >=1 comentario): {corr_spearman:.2f}. "
    f"Correlacion de Pearson (lineal): {corr_pearson:.2f}.")
log("- La diferencia entre ambas es el hallazgo interesante: en general, un video con mas "
    "vistas SI tiende a tener mas comentarios (Spearman alto), pero la relacion lineal es casi "
    "nula porque dos videos rompen el patron: 'Plan 2032 Ciudad de Guatemala' tiene, por mucho, "
    "las mas vistas (~304 mil) pero un numero de comentarios apenas mediano (25); y "
    "'Que rico come tu diputado' (Quorum) tiene, por mucho, mas comentarios que cualquier otro "
    "(161) con vistas relativamente bajas (~11.8 mil). Esto sugiere que las vistas miden alcance "
    "pasivo mientras que comentar refleja un tipo distinto de involucramiento "
    "(indignacion/controversia politica, en el caso de Quorum), que no escala linealmente con "
    "el alcance.")
log("- Limitaciones de ambos conteos: `view_count` se congelo en el momento de la "
    "recoleccion (no representa vistas actuales) y los comentarios en este dataset son una "
    "MUESTRA (solo 19 de 293 videos tienen algun comentario), no el total real de comentarios "
    "de cada video en YouTube.")

# %% [markdown]
# ## 3.4 Visualizaciones

# %%
plt.figure(figsize=(8, 5))
por_canal.head(10).sort_values().plot(kind="barh", color="#2b6cb0")
plt.title("Top 10 canales por numero de comentarios recibidos")
plt.xlabel("Numero de comentarios")
plt.tight_layout()
plt.savefig(FIGS / "01_top_canales_comentarios.png", dpi=120)
plt.close()

plt.figure(figsize=(8, 5))
labels = top_videos.head(10).assign(
    label=lambda d: d["channel_name"].str.slice(0, 12) + " (" + d["video_id"].str.slice(0, 6) + ")"
)
plt.barh(labels["label"][::-1], labels["n_comentarios"][::-1], color="#c53030")
plt.title("Top 10 videos por numero de comentarios")
plt.xlabel("Numero de comentarios")
plt.tight_layout()
plt.savefig(FIGS / "02_top_videos_comentarios.png", dpi=120)
plt.close()

plt.figure(figsize=(7, 5))
plt.hist(videos["view_count"], bins=30, color="#38a169")
plt.yscale("log")
plt.xlabel("view_count")
plt.ylabel("numero de videos (escala log)")
plt.title("Distribucion de visualizaciones por video (293 videos)")
plt.tight_layout()
plt.savefig(FIGS / "03_histograma_views.png", dpi=120)
plt.close()

plt.figure(figsize=(8, 5))
cat_plot = cat_compare.sort_values("n_comentarios", ascending=False).head(6)
x = range(len(cat_plot))
plt.bar([i - 0.2 for i in x], cat_plot["%_videos"], width=0.4, label="% de videos", color="#4a5568")
plt.bar([i + 0.2 for i in x], cat_plot["%_comentarios"], width=0.4, label="% de comentarios", color="#dd6b20")
plt.xticks(list(x), cat_plot.index, rotation=30, ha="right")
plt.ylabel("%")
plt.title("Categoria: participacion en videos vs. en comentarios")
plt.legend()
plt.tight_layout()
plt.savefig(FIGS / "04_categorias_video_vs_comentario.png", dpi=120)
plt.close()

plt.figure(figsize=(7, 5))
plt.scatter(por_video["view_count"], por_video["n_comentarios"], color="#805ad5")
plt.xscale("log")
plt.xlabel("view_count (escala log)")
plt.ylabel("numero de comentarios")
plt.title("Popularidad vs. participacion por video")
plt.tight_layout()
plt.savefig(FIGS / "05_scatter_views_vs_comentarios.png", dpi=120)
plt.close()

top_words = pd.Series(dict(word_freq.most_common(15)))
plt.figure(figsize=(8, 5))
top_words.sort_values().plot(kind="barh", color="#2c7a7b")
plt.title("15 palabras mas frecuentes (texto_limpio)")
plt.xlabel("frecuencia")
plt.tight_layout()
plt.savefig(FIGS / "06_top_palabras.png", dpi=120)
plt.close()

top_bigrams = pd.Series(dict(bigram_freq.most_common(15)))
plt.figure(figsize=(8, 5))
top_bigrams.sort_values().plot(kind="barh", color="#975a16")
plt.title("15 bigramas mas frecuentes (texto_limpio)")
plt.xlabel("frecuencia")
plt.tight_layout()
plt.savefig(FIGS / "07_top_bigramas.png", dpi=120)
plt.close()

wc_text = " ".join(all_tokens)
wc = WordCloud(width=1000, height=600, background_color="white", collocations=False).generate(wc_text)
plt.figure(figsize=(10, 6))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Nube de palabras - comentarios (texto_limpio)")
plt.tight_layout()
plt.savefig(FIGS / "08_wordcloud.png", dpi=120)
plt.close()

log("\n## 3.4 Visualizaciones\n")
log("Graficos guardados en outputs/figs/: top canales, top videos, histograma de vistas, "
    "categoria (video vs. comentario), dispersion vistas-vs-comentarios, top palabras, "
    "top bigramas y nube de palabras (esta ultima como complemento, no como grafico principal).")

# %% [markdown]
# ## 3.5 Preguntas obligatorias del enunciado

# %%
log("\n## 3.5 Preguntas obligatorias\n")

log("**¿Que videos y canales concentran la mayor participacion observada?**")
log(f"El video 'Que rico come tu diputado' (canal Quorum) concentra el mayor numero de "
    f"comentarios (161, 39.7% del total). A nivel canal, Quorum por si solo recibe "
    f"{por_canal['Quorum']} comentarios ({por_canal['Quorum']/por_canal.sum():.1%} del total), "
    f"seguido de Gobierno de la Republica de Guatemala y Noticias Telemundo/Municipalidad de "
    f"Guatemala. Ver 3.2.")

log("\n**¿Existen audiencias compartidas entre videos, canales o temas?**")
n_autores_multi_video = m.groupby("author_channel_id")["video_id"].nunique()
n_multi = (n_autores_multi_video > 1).sum()
log(f"Si: {n_multi} de {n_authors} autores ({n_multi/n_authors:.1%}) comentaron en mas de un "
    f"video del dataset, lo que confirma que existe una audiencia compartida entre videos (y en "
    f"varios casos entre canales distintos). Esta es precisamente la base para la red bipartita "
    f"autor-video del ejercicio 4 y sus proyecciones.")

log("\n**¿Que autores funcionan como puentes entre contenidos que de otra forma permanecerian "
    "separados?**")
log("Se identifican con precision en el ejercicio 8 (centralidad de intermediacion sobre la "
    "red construida en el ejercicio 4/5), pero en este EDA ya se observa la señal: autores como "
    "@ManuelEdran, @byronpontaza y @HaroldoCastillo-rh9iw aparecen comentando en mas de un video "
    "de Quorum, y @albertoshernandez5251 concentra varios comentarios en el video del Puente "
    "Belice II del canal de Gobierno.")

log("\n**¿Que temas y sentimientos caracterizan las principales comunidades de participacion?**")
log("Se profundiza en los ejercicios 7 y 9 (comunidades y sentimiento), pero el analisis de "
    "palabras/bigramas frecuentes ya apunta a un tema dominante de critica a la clase politica y "
    "corrupcion ('pueblo', 'dinero', 'diputados', 'corruptos', 'presidente bernardo', "
    "'pacto corruptos'), junto a un nucleo minoritario de comentarios de apoyo/orgullo nacional "
    "('viva guatemala', 'excelente trabajo').")

log("\n**¿La visibilidad medida mediante visualizaciones coincide con la participacion "
    "observada?**")
log(f"Parcialmente. Por rango de posicion (Spearman={corr_spearman:.2f}) hay una asociacion "
    f"positiva bastante fuerte, pero linealmente (Pearson={corr_pearson:.2f}) practicamente no "
    "hay relacion: el video mas visto del subconjunto no es el mas comentado. Ver 3.3.")

log("\n**¿Que conclusiones estan limitadas por el procedimiento de recoleccion y la cobertura "
    "de los datos?**")
log("Todas las relacionadas con 'participacion promedio' o 'temas dominantes en Guatemala': solo "
    f"{n_videos_con_comentarios}/{n_videos} videos tienen comentarios en este dataset y estan "
    "fuertemente sesgados hacia contenido politico/de noticias (ver 3.2 y seccion 10).")

# %% [markdown]
# ## 3.6 Tres preguntas adicionales

# %%
log("\n## 3.6 Tres preguntas adicionales\n")

# --- Pregunta adicional 1: source_group ---
like_by_group = m.groupby("source_group_video")["like_count"].mean()
log("**1. ¿Los videos encontrados por busqueda tematica (source_group='topic') generan "
    "comentarios con mas 'me gusta' en promedio que los encontrados navegando directamente "
    "el canal (source_group='channel')?**")
log(f"Si, la diferencia es grande: {like_by_group['topic']:.2f} likes promedio por comentario "
    f"en videos 'topic' vs. {like_by_group['channel']:.2f} en videos 'channel' "
    f"({m[m.source_group_video=='topic'].shape[0]} vs. {m[m.source_group_video=='channel'].shape[0]} "
    f"comentarios respectivamente). Es coherente con que la busqueda tematica trajo videos mas "
    f"virales/controversiales (ej. 'Que rico come tu diputado'), mientras que navegar canal por "
    f"canal trajo mas contenido institucional con poca interaccion.")

# --- Pregunta adicional 2: idioma ---
def safe_detect(t):
    if not isinstance(t, str) or len(t.strip()) < 20:
        return "muy_corto"
    try:
        return detect(t)
    except Exception:
        return "desconocido"


m["idioma_detectado"] = m["texto_original"].apply(safe_detect)
en_rows = m[m["idioma_detectado"] == "en"]
en_video_counts = en_rows["video_id"].value_counts()
log("\n**2. ¿En que videos aparecen comentarios en ingles y que los caracteriza?**")
log(f"Deteccion automatica de idioma (langdetect, poco confiable en textos muy cortos, por eso "
    f"se excluyen los de menos de 20 caracteres) encuentra {len(en_rows)} comentarios en ingles "
    f"sobre {m['idioma_detectado'].notna().sum()} evaluados. Se concentran casi todos "
    f"({en_video_counts.iloc[0] if len(en_video_counts) else 0} de {len(en_rows)}) en el video "
    "'EE.UU. envia a mexicanos deportados a Guatemala... | Noticias Telemundo': tiene sentido, "
    "es un tema de politica migratoria de EE.UU. que atrae a comentaristas angloparlantes, "
    "distinto del resto del corpus que es abrumadoramente en español.")

# --- Pregunta adicional 3: comentarios editados ---
m["editado"] = m["published_text"].astype(str).str.contains("editado")
like_by_edit = m.groupby("editado")["like_count"].mean()
log("\n**3. ¿Los comentarios editados reciben, en promedio, menos 'me gusta' que los no "
    "editados?**")
log(f"{m['editado'].sum()} de {len(m)} comentarios ({m['editado'].mean():.1%}) fueron editados "
    f"despues de publicarse. Reciben en promedio {like_by_edit[True]:.2f} likes vs. "
    f"{like_by_edit[False]:.2f} de los no editados. Es una tendencia descriptiva sobre una "
    "muestra pequeña (18 comentarios editados), no se puede afirmar causalidad, pero es "
    "consistente con la idea de que la edicion suele ocurrir en comentarios menos visibles/con "
    "menos interaccion previa (el autor corrige sin presion de una audiencia grande observando).")

# %% [markdown]
# ## Guardado de resultados

# %%
report_path = OUTPUTS / "reporte_ejercicio_3.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
print(f"Figuras guardadas en {FIGS}")
