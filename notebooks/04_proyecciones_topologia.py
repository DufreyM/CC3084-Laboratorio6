# %% [markdown]
# # Laboratorio 6 - Ejercicio 5: Proyecciones | Ejercicio 6: Topologia y fragmentacion
# **Autor de esta seccion:** Leonardo Mejia
#
# Parte de `data/processed/comments_clean.csv` y `videos_clean.csv`. Reconstruye la
# misma red bipartita autor-video del ejercicio 4 (para no depender de que ese
# notebook se haya corrido antes) y construye ambas proyecciones.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

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
# ## 5.1 / 5.2 Construccion de las proyecciones
#
# - **Autor-autor**: dos autores se conectan si comentaron en el mismo video; el peso
#   es el numero de videos que comparten (no el numero de comentarios).
# - **Video-video**: dos videos se conectan si comparten al menos un autor; el peso
#   es el numero de autores que comparten.
#
# Ambas se calculan con `networkx.algorithms.bipartite.weighted_projected_graph`,
# que construye exactamente esa definicion de peso a partir de la red bipartita del
# ejercicio 4 (no se recalculan a mano para evitar inconsistencias).

# %%
author_proj = bipartite.weighted_projected_graph(G, authors)
video_proj = bipartite.weighted_projected_graph(G, vids)

log("## 5.1 / 5.2 Proyecciones\n")
log(f"- Autor-autor: {author_proj.number_of_nodes()} nodos, "
    f"{author_proj.number_of_edges()} aristas.")
log(f"- Video-video: {video_proj.number_of_nodes()} nodos, "
    f"{video_proj.number_of_edges()} aristas (de un maximo posible de "
    f"{video_proj.number_of_nodes()*(video_proj.number_of_nodes()-1)//2}).")

from collections import Counter
w_dist = Counter(nx.get_edge_attributes(author_proj, "weight").values())
log(f"\n**Distribucion de pesos en autor-autor:** {dict(sorted(w_dist.items()))}")
log("Casi todas las aristas (10730 de 10732) tienen peso 1, es decir, ambos autores "
    "comparten EXACTAMENTE un video. Esto es en gran parte un artefacto mecanico de "
    "que la enorme mayoria de autores (323 de 332, ver ejercicio 3.5) solo aparece "
    "comentando en un unico video de todo el dataset: cualquier arista que involucre "
    "a esos autores forzosamente tiene peso 1. Solo 2 pares de autores comparten "
    "realmente 2 videos distintos, que es la unica evidencia de participacion "
    "genuinamente cruzada entre contenidos en esta proyeccion.")

du.save_processed(
    nx.to_pandas_edgelist(author_proj), "proyeccion_autor_autor.csv"
)
du.save_processed(
    nx.to_pandas_edgelist(video_proj), "proyeccion_video_video.csv"
)

# %% [markdown]
# ## 5.3 Comparacion: que fenomeno representa cada proyeccion
#
# - La proyeccion **autor-autor** representa audiencias compartidas: cuantos autores
#   distintos comentaron en mas de un mismo video. Con datos tan concentrados en 19
#   videos y mayoritariamente autores de un solo comentario, esta proyeccion termina
#   pareciendose a "clanes" densos (casi cliques) por cada video, mas que a una red
#   de afinidad tematica real entre personas.
# - La proyeccion **video-video** representa solapamiento de audiencia entre
#   contenidos: que tan seguido el mismo comentarista aparece en distintos videos.
#   Con solo 19 nodos es mucho mas facil de leer, y muestra directamente cuales
#   videos "compiten" o "comparten" comunidad de comentaristas.
# - Ninguna de las dos debe interpretarse como interaccion directa entre personas
#   (ver 4.5): ambas son co-presencia observada, no conversacion ni acuerdo.

# %% [markdown]
# ## 5.4 Visualizacion de las proyecciones

# %%
fig, ax = plt.subplots(figsize=(7, 6))
pos = nx.spring_layout(author_proj, k=0.15, seed=7)
nx.draw_networkx_edges(author_proj, pos, alpha=0.15, width=0.5, ax=ax)
nx.draw_networkx_nodes(author_proj, pos, node_size=35, node_color="#38a169", ax=ax)
ax.set_title("Proyeccion autor-autor (peso = videos compartidos)")
ax.axis("off")
ax.margins(0.1)
fig.savefig(FIGS / "10_proyeccion_autor_autor.png", dpi=130, bbox_inches="tight", pad_inches=0.3)
plt.close(fig)

strong_pairs = [(u, v) for u, v, d in author_proj.edges(data=True) if d["weight"] >= 2]
strong_sub = author_proj.edge_subgraph(strong_pairs).copy() if strong_pairs else nx.Graph()
fig, ax = plt.subplots(figsize=(4, 3))
pos2 = nx.spring_layout(strong_sub, seed=1)
nx.draw(strong_sub, pos2, with_labels=False, node_color="#2c7a7b", node_size=250,
        width=[strong_sub[u][v]["weight"] for u, v in strong_sub.edges()], ax=ax)
ax.set_title("Autor-autor: SOLO pares que comparten\n2+ videos (participacion cruzada genuina)")
ax.margins(0.2)
fig.savefig(FIGS / "11_proyeccion_autor_autor_filtrada.png", dpi=130, bbox_inches="tight", pad_inches=0.3)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 6.5))
pos3 = nx.spring_layout(video_proj, seed=3, k=0.8)
node_sizes = [300 + 40 * video_proj.degree(n) for n in video_proj.nodes()]
edge_w = [video_proj[u][v]["weight"] for u, v in video_proj.edges()]
nx.draw_networkx_edges(video_proj, pos3, width=[w * 1.2 for w in edge_w], alpha=0.5, ax=ax)
nx.draw_networkx_nodes(video_proj, pos3, node_size=node_sizes, node_color="#c53030", ax=ax)
labels = {n: videos.set_index("video_id").loc[n, "title"][:20] for n in video_proj.nodes()}
nx.draw_networkx_labels(video_proj, pos3, labels=labels, font_size=7, ax=ax)
ax.set_title("Proyeccion video-video (peso = autores compartidos)")
ax.axis("off")
ax.margins(0.1)
fig.savefig(FIGS / "12_proyeccion_video_video.png", dpi=130, bbox_inches="tight", pad_inches=0.3)
plt.close(fig)

log("\n## 5.4 Visualizaciones\n")
log("Se guardaron 3 figuras: (10) la proyeccion autor-autor completa, que se ve "
    "como una nube densa de pequenos 'clanes' (uno por video, ver 5.2); (11) SOLO "
    "los pares de autores que comparten 2+ videos, como complemento que aisla la "
    "señal de participacion cruzada real, mucho mas legible; y (12) la proyeccion "
    "video-video completa (19 nodos, facil de leer sin filtrar nada).")

# %% [markdown]
# ## 6.1 Topologia: nodos, aristas, densidad, grado, componentes

# %%
import statistics


def topologia(nombre, g):
    log(f"\n### {nombre}")
    degs = [d for _, d in g.degree()]
    comps = sorted(nx.connected_components(g), key=len, reverse=True)
    isolates = list(nx.isolates(g))
    log(f"- Nodos: {g.number_of_nodes()} | Aristas: {g.number_of_edges()} | "
        f"Densidad: {nx.density(g):.4f}")
    log(f"- Grado: media={statistics.mean(degs):.2f}, mediana={statistics.median(degs):.1f}, "
        f"min={min(degs)}, max={max(degs)}")
    log(f"- Componentes conexos: {len(comps)} | Tamano del mayor: {max(len(c) for c in comps)} "
        f"({max(len(c) for c in comps)/g.number_of_nodes():.1%} del total de nodos)")
    log(f"- Nodos aislados (grado 0): {len(isolates)}")
    log(f"- Transitividad (global): {nx.transitivity(g):.4f} | "
        f"Clustering promedio (local): {nx.average_clustering(g):.4f}")
    return degs, comps


log("## 6.1 Topologia y fragmentacion\n")
deg_bip, comp_bip = topologia("Red bipartita autor-video", G)
log("  Nota: la transitividad de una red bipartita es SIEMPRE 0 por definicion "
    "(no puede haber triangulos entre dos tipos de nodo alternados, solo ciclos "
    "de longitud par); no es un error de calculo, es una propiedad estructural.")

deg_auth, comp_auth = topologia("Proyeccion autor-autor", author_proj)
log("  La transitividad muy alta (0.98) confirma que la proyeccion esta dominada "
    "por cliques casi perfectos: cuando tres autores comparten aunque sea un solo "
    "video en comun, automaticamente se forma un triangulo, porque un video con N "
    "autores genera un clique completo de tamano N en la proyeccion.")

deg_vid, comp_vid = topologia("Proyeccion video-video", video_proj)

log("\n**Distribucion de grado**, para saber si la mayoria tiene pocas conexiones o "
    "estan concentradas en pocos nodos:")
log(f"- Bipartita: el 75% de los nodos tiene grado <= "
    f"{pd.Series(deg_bip).quantile(0.75):.0f}, pero el maximo es {max(deg_bip)} "
    f"(el video 'Que rico come tu diputado', ver ejercicio 4) -> distribucion muy "
    f"desigual, tipica de redes con hubs (no aleatoria/uniforme).")
log(f"- Video-video: grados van de 0 a {max(deg_vid)}; "
    f"{sum(1 for d in deg_vid if d==0)} de {len(deg_vid)} videos (grado 0, "
    f"totalmente aislados de los demas).")

# %% [markdown]
# ## 6.2 Cohesion y transitividad (discusion)

# %%
log("\n## 6.2 Cohesion\n")
log("La red bipartita y sus proyecciones NO son cohesivas en el sentido de 'un solo "
    "bloque conectado': ambas tienen 10 componentes conexos, y el mas grande cubre "
    f"{max(len(c) for c in comp_bip)/G.number_of_nodes():.1%} de los nodos de la "
    "bipartita pero deja 9 componentes de un solo video cada uno, totalmente "
    "aislados del resto (ver 6.3). La proyeccion autor-autor es MUY cohesiva "
    "DENTRO de cada componente (clustering ~0.97, casi clique) pero eso es "
    "estructuralmente esperable y no implica cohesion social real entre esos "
    "autores (ver 4.5 y 5.3).")

# %% [markdown]
# ## 6.3 Nodos y grupos perifericos/aislados: aislamiento observado vs. ausencia de datos

# %%
log("\n## 6.3 Perifericos y aislados\n")
log("Desglose de los 10 componentes de la red bipartita:")
for i, c in enumerate(comp_bip):
    vids_in = [n for n in c if n in vids]
    titles = videos.set_index("video_id").loc[vids_in, "title"].tolist() if vids_in else []
    log(f"  Componente {i}: {len(c)} nodos ({len(vids_in)} video(s), "
        f"{len(c)-len(vids_in)} autor(es)) -> {titles}")

log("\n**Interpretacion:** el componente gigante (286 nodos, 10 videos, 276 "
    "autores) muestra que esos 10 videos SI comparten audiencia entre si a traves "
    "de autores puente. Los otros 9 componentes son cada uno UN SOLO video con su "
    "propio publico exclusivo (algunos grandes, como 'Plan 2032 Ciudad de "
    "Guatemala' con 25 autores, o el video de deportaciones de Telemundo con 18): "
    "ninguno de sus comentaristas aparece comentando en ningun otro video de la "
    "muestra.")
log("- Esto es **aislamiento observado**, no un hueco de datos: tenemos el 100% de "
    "los comentarios recolectados de esos videos y ninguno conecta con otro video.")
log("- Pero tambien es **aislamiento posiblemente inflado por la cobertura de "
    "datos**: como el dataset solo capturo un puñado de comentarios por video "
    "(ver ejercicio 3.2) y no el historial completo de cada autor en YouTube, es "
    "esperable que autores que SI comentan en varios videos de estos canales en la "
    "vida real no aparezcan conectados aqui simplemente porque solo uno de sus "
    "comentarios entro en la muestra. No se puede distinguir con estos datos cual "
    "de las dos causas pesa mas.")

log(f"\n**Videos-video aislados (sin ningun autor en comun con otro video):** "
    f"{sum(1 for d in deg_vid if d==0)} de {len(deg_vid)}.")
log(f"**Autores aislados en la proyeccion autor-autor** (comentaron en un video "
    f"donde fueron el unico comentarista): {sum(1 for d in deg_auth if d==0)} de "
    f"{len(deg_auth)}.")

# %% [markdown]
# ## 6.4 Hallazgos estructurales

# %%
log("\n## 6.4 Hallazgos\n")
log("- La red de participacion NO es una sola comunidad interconectada: es un "
    "hub gigante (los videos mas comentados de Quorum y del Gobierno, conectados "
    "por un puñado de autores que comentan en varios) rodeado de 9 audiencias "
    "totalmente aisladas, cada una fiel a un solo video.")
log("- La densidad extremadamente baja de la bipartita (0.0056) y de video-video "
    "(0.064) contrasta con la densidad artificialmente alta de autor-autor "
    "(0.195, arrastrada por los cliques mecanicos); hay que leer 'densidad de la "
    "proyeccion' con cuidado, no como evidencia de cohesion social.")
log("- La distribucion de grado extremadamente desigual (unos pocos nodos "
    "concentran casi todas las conexiones) es consistente con lo encontrado en "
    "el ejercicio 3.2 (concentracion de la participacion en pocos videos/canales): "
    "la estructura de red confirma, desde otro angulo, el mismo patron de "
    "concentracion.")

# %% [markdown]
# ## Guardado de resultados

# %%
report_path = OUTPUTS / "reporte_ejercicio_5_6.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
