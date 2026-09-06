# %% [markdown]
# # Laboratorio 6 - Ejercicio 7: Comunidades | Ejercicio 8: Nodos centrales y puentes
# **Autor de esta seccion:** Leonardo Mejia
#
# Parte de `data/processed/comments_clean.csv` y `videos_clean.csv`, reconstruyendo
# la misma red bipartita autor-video del ejercicio 4. De paso calcula el sentimiento
# de cada comentario (pysentimiento) y lo guarda en `data/processed/comments_sentiment.csv`
# para caracterizar comunidades aqui y para el analisis completo del ejercicio 9.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.algorithms.community import louvain_communities, modularity

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

edges = comments.groupby(["author_channel_id", "video_id"]).size().reset_index(name="weight")
authors = set(comments["author_channel_id"])
vids = set(comments["video_id"])

G = nx.Graph()
G.add_nodes_from(authors, bipartite=0)
G.add_nodes_from(vids, bipartite=1)
for _, e in edges.iterrows():
    G.add_edge(e["author_channel_id"], e["video_id"], weight=e["weight"])

# %% [markdown]
# ## Sentimiento por comentario (insumo para 7.5 y para el ejercicio 9)

# %%
sentiment_path = ROOT / "data" / "processed" / "comments_sentiment.csv"
if sentiment_path.exists():
    sent_df = pd.read_csv(sentiment_path)
else:
    from pysentimiento import create_analyzer

    analyzer = create_analyzer(task="sentiment", lang="es")
    results = analyzer.predict(comments["texto_original"].fillna("").tolist())
    sent_df = pd.DataFrame({
        "comment_id": comments["comment_id"],
        "sentimiento": [r.output for r in results],
        "prob_neg": [r.probas["NEG"] for r in results],
        "prob_neu": [r.probas["NEU"] for r in results],
        "prob_pos": [r.probas["POS"] for r in results],
    })
    du.save_processed(sent_df, "comments_sentiment.csv")

comments = comments.merge(sent_df, on="comment_id", how="left")
log("## Sentimiento por comentario\n")
log(comments["sentimiento"].value_counts().to_string())

# %% [markdown]
# ## 7.1 Seleccion de la red para deteccion de comunidades
#
# Se usa la **red bipartita autor-video** completa (no una de las proyecciones del
# ejercicio 5), por dos razones:
# 1. La proyeccion autor-autor esta dominada por cliques casi perfectos que se forman
#    mecanicamente cuando varios autores comparten un solo video (ver ejercicio 5.3,
#    5.2: transitividad 0.98); optimizar modularidad ahi solo re-descubriria los
#    mismos grupos que ya identificamos como componentes conexos en el ejercicio 6,
#    sin aportar nada nuevo.
# 2. Detectar comunidades directamente en la bipartita agrupa autores Y videos en la
#    misma comunidad, que es justo lo que pide el ejercicio 7.5 (caracterizar cada
#    comunidad por videos, canales, autores, temas y sentimiento a la vez).

# %% [markdown]
# ## 7.2 Algoritmo, supuestos y tratamiento de pesos
#
# Se usa **Louvain** (`networkx.algorithms.community.louvain_communities`), que
# optimiza la modularidad de forma jerarquica/greedy. Supuestos: maximiza la
# modularidad ponderada (asume que una buena particion tiene mas peso de aristas
# DENTRO de cada grupo que el esperado al azar); es no determinista entre corridas
# sin fijar semilla (se fija `seed=42` para reproducibilidad) y puede converger a un
# optimo local, no necesariamente el global. El peso de cada arista (numero de
# comentarios de ese autor en ese video) se usa directamente como `weight` en el
# calculo de modularidad, de forma que un autor con varios comentarios en el mismo
# video pesa mas en la particion que uno con un solo comentario.

# %%
commts = louvain_communities(G, weight="weight", seed=42, resolution=1.0)
mod = modularity(G, commts, weight="weight")
commts = sorted(commts, key=len, reverse=True)

node_to_comm = {n: i for i, c in enumerate(commts) for n in c}

log("\n## 7.3 Numero de comunidades, tamanos y modularidad\n")
log(f"- Numero de comunidades: {len(commts)}")
log(f"- Modularidad: {mod:.4f} (valores > 0.3 ya se consideran estructura de "
    f"comunidad fuerte; 0.78 es muy alto, esperable dado lo fragmentada que ya "
    f"vimos que es la red en el ejercicio 6).")
log("- Tamanos (de mayor a menor):")
for i, c in enumerate(commts):
    vids_in = [n for n in c if n in vids]
    titles = videos.set_index("video_id").loc[vids_in, "title"].tolist() if vids_in else []
    log(f"  Comunidad {i}: {len(c)} nodos ({len(vids_in)} video(s)) -> {titles}")

# %% [markdown]
# ## 7.4 Visualizacion de todas las comunidades

# %%
pos = nx.spring_layout(G, k=0.35, seed=42)
colors = plt.colormaps.get_cmap("tab20").resampled(len(commts))

plt.figure(figsize=(13, 11))
for i, c in enumerate(commts):
    node_sizes = [350 if n in vids else 20 for n in c]
    nx.draw_networkx_nodes(G, pos, nodelist=list(c), node_size=node_sizes,
                            node_color=[colors(i)] * len(c), label=f"Com. {i} (n={len(c)})")
nx.draw_networkx_edges(G, pos, alpha=0.12, width=0.5)
plt.legend(scatterpoints=1, fontsize=7, loc="lower left", ncol=2)
plt.title(f"Comunidades (Louvain, modularidad={mod:.3f}) sobre la red bipartita")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGS / "13_comunidades.png", dpi=130)
plt.close()

log("\n## 7.4 Visualizacion\n")
log("Guardada en outputs/figs/13_comunidades.png: cada color es una comunidad, "
    "los nodos grandes son videos y los pequenos autores. Se observa que casi "
    "todas las comunidades coinciden con un solo video (igual que los componentes "
    "conexos del ejercicio 6.3), EXCEPTO una comunidad que fusiona 3 videos "
    "distintos de Quorum en un solo grupo (ver 7.5), lo que confirma que Louvain "
    "SI encontro una subestructura mas fina que la mera conectividad.")

# %% [markdown]
# ## 7.5 Caracterizacion de las 3 comunidades principales

# %%
comments["comunidad"] = comments["author_channel_id"].map(node_to_comm)


def caracterizar(i):
    c = commts[i]
    vids_in = [n for n in c if n in vids]
    titles = videos.set_index("video_id").loc[vids_in, ["title", "channel_name", "category"]]
    sub = comments[comments["video_id"].isin(vids_in)]
    log(f"\n**Comunidad {i}** ({len(c)} nodos: {len(vids_in)} video(s), "
        f"{len(c)-len(vids_in)} autor(es))")
    log(f"- Videos/canales: {titles.to_dict('records')}")
    log(f"- Comentarios en esta comunidad: {len(sub)}")
    top_words = pd.Series(
        [tok for t in sub["texto_limpio"].dropna() for tok in t.split()]
    ).value_counts().head(8)
    log(f"- Palabras mas frecuentes: {top_words.to_dict()}")
    log(f"- Sentimiento: {sub['sentimiento'].value_counts(normalize=True).round(2).to_dict()}")
    log(f"- Intensidad de participacion (comentarios/autor): "
        f"{len(sub)/max(1,(len(c)-len(vids_in))):.2f}")


log("\n## 7.5 Caracterizacion\n")
for i in range(min(3, len(commts))):
    caracterizar(i)

log("\n**Nota sobre la comunidad multi-video (la de 'Arroz con pollo a la "
    "MONOPOLIO' + 'Internet: escoger el menos malo' + 'Caminar en una ciudad "
    "hecha para carros'):** las tres son videos de Quorum sobre temas de "
    "consumidor/servicios/movilidad urbana (no politica-escandalo como el video "
    "mas grande), y comparten un nucleo de autores fieles a ese tipo de contenido "
    "de Quorum; es la evidencia mas clara de una 'comunidad tematica' real en "
    "este dataset, distinta de simplemente 'la audiencia de un video viral'.")

# %% [markdown]
# ## 8.1 Medidas de centralidad
#
# Se calculan tres medidas complementarias sobre la red bipartita:
# - **Grado** (degree centrality): cuantos videos distintos comento un autor, o
#   cuantos autores distintos comentaron un video. Mide alcance directo/recurrencia.
# - **Intermediacion** (betweenness centrality): que tanto un nodo esta en el camino
#   mas corto entre otros pares de nodos. Es la medida clave para encontrar autores
#   puente y videos articuladores (8.3).
# - **PageRank**: version ponderada por importancia de los vecinos (no solo cuenta
#   conexiones, sino la importancia de con quien te conectas); util para ver que
#   videos concentran influencia estructural aun con pocos autores, si esos autores
#   tambien comentan en otros videos importantes.

# %%
deg = nx.degree_centrality(G)
btw = nx.betweenness_centrality(G, weight=None, normalized=True)
pr = nx.pagerank(G, weight="weight")

cent_df = pd.DataFrame({"grado": deg, "intermediacion": btw, "pagerank": pr})
cent_df["tipo"] = ["autor" if n in authors else "video" for n in cent_df.index]
du.save_processed(cent_df.reset_index(names="id"), "centralidad.csv")

# %% [markdown]
# ## 8.2 Interpretacion separada para autores y videos

# %%
names = comments.drop_duplicates("author_channel_id").set_index("author_channel_id")["author_name"]
titles = videos.set_index("video_id")["title"]

log("\n## 8.2 Centralidad\n")
log("**Top 8 autores por intermediacion** (recurrencia + diversidad: comentan en "
    "mas de un video, de comunidades distintas):")
top_auth = cent_df[cent_df.tipo == "autor"].sort_values("intermediacion", ascending=False).head(8).copy()
top_auth["nombre"] = top_auth.index.map(names)
log(top_auth[["nombre", "grado", "intermediacion", "pagerank"]].to_string())

log("\n**Top 8 videos por intermediacion** (alcance dentro de la red + capacidad de "
    "conectar audiencias distintas):")
top_vid = cent_df[cent_df.tipo == "video"].sort_values("intermediacion", ascending=False).head(8).copy()
top_vid["titulo"] = top_vid.index.map(titles)
log(top_vid[["titulo", "grado", "intermediacion", "pagerank"]].to_string())

log("\nPara **autores**: la intermediacion alta identifica a quienes comentan en "
    "videos de comunidades distintas (puentes reales), mientras que el grado por "
    "si solo en una bipartita autor-video rara vez pasa de 2-3 para autores (nadie "
    "comenta en decenas de videos), asi que la intermediacion es mas informativa "
    "que el grado para 'diversidad de participacion' en este dataset especifico.")
log("\nPara **videos**: el grado (numero de autores distintos) ya identifica alcance "
    "directo, pero la intermediacion identifica algo distinto: cuales videos, si se "
    "quitaran, fragmentarian mas la red. 'Que rico come tu diputado' domina ambas "
    "medidas (grado Y intermediacion), consistente con ser el hub central de todo "
    "el dataset.")

# %% [markdown]
# ## 8.3 Participantes recurrentes, autores puente y videos articuladores

# %%
articulation = set(nx.articulation_points(G))
art_videos = [n for n in articulation if n in vids]
art_authors = [n for n in articulation if n in authors]

log("\n## 8.3 Puentes y articuladores\n")
log(f"- **Puntos de articulacion totales** (nodos cuya eliminacion desconecta la "
    f"red en mas piezas): {len(articulation)} de {G.number_of_nodes()}.")
log(f"- **Videos articuladores**: {len(art_videos)} de {len(vids)} "
    f"-> {[titles.get(v) for v in art_videos]}")
log("  Esto incluye a casi todos los videos con comentarios: es un efecto "
    "esperado de la estructura bipartita en estrella (ver ejercicio 6), donde "
    "cada video es el unico puente hacia sus propios autores exclusivos, asi que "
    "removerlo siempre desconecta a esos autores del resto.")
log(f"- **Autores puente (articulacion)**: {len(art_authors)} -> "
    f"{[names.get(a) for a in art_authors]}. Estos SI son un hallazgo mas "
    "interesante: son los pocos autores que unen dos videos/comunidades que de "
    "otro modo quedarian separados (coinciden con el top de intermediacion de "
    "8.2).")
log("\n- **Participantes recurrentes** (comentaron en mas de un video, ver "
    f"ejercicio 3.5): {sum(1 for n in authors if G.degree(n) > 1)} autores.")

# %% [markdown]
# ## Guardado de resultados

# %%
report_path = OUTPUTS / "reporte_ejercicio_7_8.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
