# %% [markdown]
# # Laboratorio 6 - Ejercicio 4: Red bipartita autor-video
# **Autora de esta seccion:** Mia Fuentes
#
# Parte de `data/processed/comments_clean.csv` y `videos_clean.csv` (generados por
# `01_carga_calidad_leonardo.py`). Cada fila de comments es un comentario, con
# `author_channel_id` (autor) y `video_id` (video) ya limpios, listos para construir
# la red sin volver a procesar nada.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import networkx as nx
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

# %% [markdown]
# ## 4.1 / 4.2 Construccion de la red bipartita
#
# Nodos de dos tipos: **autor** (`author_channel_id`) y **video** (`video_id`).
# Una arista autor-video existe si ese autor publico al menos un comentario principal
# en ese video; el peso de la arista es el numero de comentarios de ese autor en ese
# video especifico (no el total de comentarios del autor en todo el dataset).
#
# **No se usa `reply_count` para nada aqui**: el enunciado prohibe expresamente
# inferir "quien respondio a quien" a partir de esa columna, asi que la red conecta
# unicamente autor<->video, nunca autor<->autor directamente en esta seccion (eso se
# hace de forma correcta, vecino-en-comun, en las proyecciones del ejercicio 5).

# %%
edges = (
    comments.groupby(["author_channel_id", "video_id"])
    .size()
    .reset_index(name="weight")
)

log("## 4.1 / 4.2 Construccion de la red bipartita\n")
log(f"- Pares autor-video distintos (aristas): {len(edges)}")
log(f"- Aristas con peso > 1 (mismo autor con mas de un comentario principal en el "
    f"mismo video): {(edges['weight'] > 1).sum()} de {len(edges)} "
    f"({(edges['weight'] > 1).mean():.1%})")
log("  Nota de interpretacion: parte de estos pesos altos coincide con videos donde ya "
    "se detecto (ejercicio 2.1) un numero alto de `comment_id` con formato de respuesta "
    "de YouTube (`looks_like_reply_id`); es probable que reflejen a una misma persona "
    "respondiendo varias veces DENTRO de un hilo de discusion (ej. 6 comentarios de un "
    "mismo autor en el video del Puente Belice II), no 6 comentarios independientes "
    "sin relacion entre si.")

G = nx.Graph()
for author_id, group in comments.groupby("author_channel_id"):
    row = group.iloc[0]
    G.add_node(
        author_id,
        tipo="autor",
        nombre=row["author_name"],
        handle=row["author_handle"],
    )
for video_id, row in videos.set_index("video_id").iterrows():
    if video_id in set(comments["video_id"]):
        G.add_node(
            video_id,
            tipo="video",
            titulo=row["title"],
            canal=row["channel_name"],
            categoria=row["category"],
            view_count=row["view_count"],
        )
for _, e in edges.iterrows():
    G.add_edge(e["author_channel_id"], e["video_id"], weight=e["weight"])

n_autor_nodes = sum(1 for _, d in G.nodes(data=True) if d["tipo"] == "autor")
n_video_nodes = sum(1 for _, d in G.nodes(data=True) if d["tipo"] == "video")
log(f"\n- Nodos tipo autor: {n_autor_nodes}")
log(f"- Nodos tipo video: {n_video_nodes}")
log(f"- Total de nodos: {G.number_of_nodes()} | Total de aristas: {G.number_of_edges()}")
log(f"- ¿Es bipartita? {nx.is_bipartite(G)}")

# %% [markdown]
# ## 4.3 Tabla de nodos y tabla de aristas

# %%
n_videos_por_autor = edges.groupby("author_channel_id")["video_id"].nunique()
n_autores_por_video = edges.groupby("video_id")["author_channel_id"].nunique()
comentarios_por_autor = comments.groupby("author_channel_id").size()
comentarios_por_video = comments.groupby("video_id").size()

nodes_autor = pd.DataFrame({
    "id": list(n_videos_por_autor.index),
}).assign(
    tipo="autor",
    nombre=lambda d: d["id"].map(comments.drop_duplicates("author_channel_id").set_index("author_channel_id")["author_name"]),
    handle=lambda d: d["id"].map(comments.drop_duplicates("author_channel_id").set_index("author_channel_id")["author_handle"]),
    n_videos_distintos=lambda d: d["id"].map(n_videos_por_autor),
    n_comentarios_totales=lambda d: d["id"].map(comentarios_por_autor),
)

nodes_video = pd.DataFrame({
    "id": list(n_autores_por_video.index),
}).assign(
    tipo="video",
    titulo=lambda d: d["id"].map(videos.set_index("video_id")["title"]),
    canal=lambda d: d["id"].map(videos.set_index("video_id")["channel_name"]),
    categoria=lambda d: d["id"].map(videos.set_index("video_id")["category"]),
    view_count=lambda d: d["id"].map(videos.set_index("video_id")["view_count"]),
    n_autores_distintos=lambda d: d["id"].map(n_autores_por_video),
    n_comentarios=lambda d: d["id"].map(comentarios_por_video),
)

nodes_table = pd.concat([nodes_video, nodes_autor], ignore_index=True)
edges_table = edges.rename(columns={"author_channel_id": "source", "video_id": "target"})

du.save_processed(nodes_table, "red_bipartita_nodos.csv")
du.save_processed(edges_table, "red_bipartita_aristas.csv")

log("\n## 4.3 Tabla de nodos y aristas\n")
log(f"- Tabla de nodos guardada en data/processed/red_bipartita_nodos.csv "
    f"({len(nodes_table)} filas: {n_video_nodes} videos + {n_autor_nodes} autores).")
log(f"- Tabla de aristas guardada en data/processed/red_bipartita_aristas.csv "
    f"({len(edges_table)} filas: source=autor, target=video, weight=num. comentarios).")
log("\n**Top 5 videos por numero de autores distintos que le comentaron:**")
log(nodes_video.sort_values("n_autores_distintos", ascending=False)
    .head(5)[["id", "titulo", "canal", "n_autores_distintos", "n_comentarios"]]
    .to_string(index=False))
log("\n**Top 5 autores por numero de videos distintos donde comentaron:**")
log(nodes_autor.sort_values("n_videos_distintos", ascending=False)
    .head(5)[["id", "nombre", "n_videos_distintos", "n_comentarios_totales"]]
    .to_string(index=False))

# %% [markdown]
# ## 4.4 Visualizacion de la red completa

# %%
pos = nx.spring_layout(G, k=0.35, seed=42, weight=None)

video_nodes = [n for n, d in G.nodes(data=True) if d["tipo"] == "video"]
author_nodes = [n for n, d in G.nodes(data=True) if d["tipo"] == "autor"]

plt.figure(figsize=(13, 11))
nx.draw_networkx_edges(G, pos, alpha=0.15, width=0.6)
nx.draw_networkx_nodes(G, pos, nodelist=author_nodes, node_size=25,
                        node_color="#63b3ed", label=f"autores ({len(author_nodes)})")
nx.draw_networkx_nodes(G, pos, nodelist=video_nodes, node_size=350,
                        node_color="#c53030", label=f"videos ({len(video_nodes)})")

video_labels = {n: d["titulo"][:22] for n, d in G.nodes(data=True) if d["tipo"] == "video"}
nx.draw_networkx_labels(G, pos, labels=video_labels, font_size=6.5)

plt.legend(scatterpoints=1, loc="lower left")
plt.title("Red bipartita autor-video (todos los autores y videos con comentarios)")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGS / "09_red_bipartita_completa.png", dpi=130)
plt.close()

log("\n## 4.4 Visualizacion\n")
log("Se guardo en outputs/figs/09_red_bipartita_completa.png. Se grafican TODOS los "
    f"{G.number_of_nodes()} nodos y {G.number_of_edges()} aristas (sin filtrar ni "
    "podar nada por estetica); los videos (rojo, mas grandes, etiquetados con el "
    "titulo del video, mas informativo que el canal ya que 8 de los 19 videos con "
    "comentarios son de Quorum) actuan como 'hubs' claramente visibles, rodeados de "
    "sus autores (azul, pequeños). Los autores que comentaron en mas de un video "
    "aparecen conectados a mas de un hub rojo, y son visualmente identificables como "
    "los pocos nodos azules que caen ENTRE dos o mas grupos en vez de pegados a un "
    "solo hub.")

# %% [markdown]
# ## 4.5 Que significa (y que NO significa) una arista

# %%
log("\n## 4.5 Interpretacion de la arista\n")
log("Una arista autor-video significa UNICAMENTE que ese autor publico al menos un "
    "comentario principal en ese video, y su peso es cuantos comentarios principales "
    "publico ahi (no respuestas, ver 4.1). Esto NO implica:")
log("- que el autor haya conversado con otros autores que comentaron el mismo video "
    "(los datos no permiten saber si se leyeron entre si, ver advertencia del "
    "enunciado sobre reply_count);")
log("- aprobacion o rechazo del contenido del video (un comentario muy critico genera "
    "la misma arista que uno elogioso);")
log("- ninguna relacion de amistad, seguimiento o conocimiento mutuo entre autores que "
    "comparten un video comentado; solo indica co-participacion observada en el mismo "
    "espacio publico, en la ventana de tiempo/muestra que cubre este dataset.")

# %% [markdown]
# ## Guardado de resultados

# %%
report_path = OUTPUTS / "reporte_ejercicio_4.md"
report_path.write_text("\n".join(str(l) for l in report_lines), encoding="utf-8")
print(f"\nReporte guardado en {report_path}")
