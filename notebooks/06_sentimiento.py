# %% [markdown]
# # Laboratorio 6 - Ejercicio 9: Analisis de contenido y sentimiento
# **Autor de esta seccion:** Leonardo Mejia
#
# Usa `data/processed/comments_sentiment.csv` (calculado en el notebook 05 con
# pysentimiento sobre `texto_original`) y lo cruza con `comments_clean.csv` y
# `videos_clean.csv` para comparar sentimiento por video, canal y comunidad.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import pandas as pd

import data_utils as du

FIGS = ROOT / "outputs" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)
OUTPUTS = ROOT / "outputs"

report_lines = []


def log(msg=""):
    print(msg)
    report_lines.append(msg)


comments = du.load_processed("comments_clean.csv")
videos = du.load_processed("videos_clean.csv")
sent = pd.read_csv(ROOT / "data" / "processed" / "comments_sentiment.csv")
c = comments.merge(sent, on="comment_id").merge(
    videos[["video_id", "category"]], on="video_id"
)

# %% [markdown]
# ## 9.1 Herramienta y justificacion
#
# Se usa **pysentimiento** con el modelo `robertuito-sentiment-analysis`: un RoBERTa
# preentrenado y afinado especificamente en **tweets en espanol** (RoBERTuito),
# clasificando cada comentario en POS/NEU/NEG con sus probabilidades. Se eligio
# sobre alternativas como VADER (lexicon en ingles, pobre para espanol) o un
# lexicon simple, porque:
# - Esta entrenado en texto de redes sociales en espanol informal/con errores
#   ortograficos, el mismo registro que los comentarios de YouTube de este dataset
#   (jerga, sin tildes, mayusculas para enfasis, groserias leves).
# - Se aplica sobre `texto_original` (no `texto_limpio`), porque conserva
#   mayusculas, signos de exclamacion y emojis, que son senales utiles de
#   intensidad emocional que la limpieza del ejercicio 2 elimina a proposito para
#   el analisis de frecuencias.

# %%
du.save_processed(c[["comment_id", "video_id", "channel_name", "sentimiento",
                      "prob_neg", "prob_neu", "prob_pos"]], "sentimiento_completo.csv")

dist = c["sentimiento"].value_counts(normalize=True).round(3)
log("## 9.1 Resultados generales\n")
log(f"Distribucion de sentimiento sobre los {len(c)} comentarios: {dist.to_dict()}")
log("El corpus es mayoritariamente NEGATIVO (61.3%), consistente con el tema "
    "dominante encontrado en el ejercicio 3 (critica a la clase politica y "
    "corrupcion: 'pueblo', 'dinero', 'corruptos', ver wordcloud).")

# Ejemplos representativos para auditar cualitativamente el modelo
log("\n**Ejemplos (auditoria cualitativa):**")
for label in ["NEG", "NEU", "POS"]:
    ejemplo = c[c["sentimiento"] == label].sort_values(
        f"prob_{label.lower()}", ascending=False
    )["texto_original"].iloc[0]
    log(f"- {label} (mas confiado): \"{ejemplo[:140]}\"")

# %% [markdown]
# ## 9.2 Comparacion por video, canal y comunidad

# %%
log("\n## 9.2 Sentimiento por canal\n")
por_canal = c.groupby("channel_name")["sentimiento"].value_counts(normalize=True).unstack().fillna(0)
por_canal["n"] = c.groupby("channel_name").size()
por_canal = por_canal.sort_values("n", ascending=False)
log(por_canal.round(2).to_string())
log("\nEl canal mas negativo es Quorum (70% NEG, arrastrado por 'Que rico come tu "
    "diputado'), y el mas positivo por MUCHO es Municipalidad de Guatemala (80% "
    "POS), impulsado enteramente por el video 'Plan 2032 Ciudad de Guatemala', "
    "donde predominan comentarios nostalgicos y de orgullo de guatemaltecos en el "
    "extranjero ('saludos desde El Salvador', 'me encantaria vivir en esa "
    "Guatemala'), un tono completamente distinto al de critica politica.")

video_counts = c.groupby("video_id").size()
big_videos = video_counts[video_counts >= 10].index
log("\n## Sentimiento por video (solo videos con >=10 comentarios, para que la "
    "proporcion sea representativa)\n")
por_video = (
    c[c["video_id"].isin(big_videos)]
    .groupby("video_id")["sentimiento"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0)
)
por_video["titulo"] = por_video.index.map(videos.set_index("video_id")["title"])
por_video["n"] = c[c["video_id"].isin(big_videos)].groupby("video_id").size()
log(por_video.round(2).sort_values("n", ascending=False).to_string())

# %% [markdown]
# ## Visualizacion

# %%
plot_df = por_video.round(3).sort_values("n", ascending=False)
plot_df = plot_df.set_index(plot_df["titulo"].str.slice(0, 25))
plt.figure(figsize=(9, 5))
plot_df[["NEG", "NEU", "POS"]].plot(
    kind="barh", stacked=True, color=["#c53030", "#a0aec0", "#38a169"], ax=plt.gca()
)
plt.xlabel("proporcion de comentarios")
plt.title("Sentimiento por video (videos con >=10 comentarios)")
plt.tight_layout()
plt.savefig(FIGS / "14_sentimiento_por_video.png", dpi=130, bbox_inches="tight", pad_inches=0.3)
plt.close()

log("\nGrafico guardado en outputs/figs/14_sentimiento_por_video.png.")

# %% [markdown]
# ## Sentimiento por comunidad (retomando el ejercicio 7)

# %%
log("\n## Sentimiento por comunidad (ver ejercicio 7.5)\n")
log("Ya reportado en outputs/reporte_ejercicio_7_8.md: la Comunidad 0 ('Que rico "
    "come tu diputado') es 81% negativa, la Comunidad 1 ('cooptacion USAC') 58% "
    "negativa pero con mas mezcla (22% positiva), y la Comunidad 2 (los 3 videos "
    "de consumidor/servicios de Quorum) es la mas equilibrada del top-3 (50% "
    "negativa, 26% positiva) -- consistente con ser contenido mas informativo y "
    "menos indignante que el escandalo de los diputados.")

# %% [markdown]
# ## 9.3 Hallazgos

# %%
log("\n## 9.3 Hallazgos\n")
log("- El sentimiento negativo domina pero NO es uniforme: varia fuertemente por "
    "TEMA del video, no por canal en si (el mismo canal Quorum tiene desde 81% "
    "NEG hasta comentarios mas mixtos segun el video especifico).")
log("- El unico foco de sentimiento mayoritariamente positivo (Plan 2032 Ciudad "
    "de Guatemala) esta asociado a contenido aspiracional/de futuro sobre la "
    "ciudad, comentado en buena parte por guatemaltecos en el extranjero, "
    "sugiriendo que el patron 'negativo por default' de este corpus refleja "
    "sobre todo el sesgo tematico de que dato de video se recolecto (mucho "
    "escandalo politico), no necesariamente el animo general de los usuarios de "
    "YouTube guatemaltecos (ver limitaciones, ejercicio 10).")
log("- El video de deportaciones de Telemundo (con comentarios en ingles, ver "
    "ejercicio 3.6) tambien es mayoritariamente negativo (64%), pero con un "
    "componente de discusion polarizada visible en las respuestas en ingles "
    "captadas en el dataset (ej. discusion entre 'eugeneramirez4405' y "
    "'rosadiaz6945').")

# %% [markdown]
# ## Guardado de resultados

# %%
report_path = OUTPUTS / "reporte_ejercicio_9.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
