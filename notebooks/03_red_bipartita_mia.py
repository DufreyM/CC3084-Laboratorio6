# %% [markdown]
# # Laboratorio 6 - Ejercicio 4: Red bipartita autor-video
# **Autora de esta seccion:** Mia Flores
#
# Partir SIEMPRE de `data/processed/comments_clean.csv` (generado por
# `01_carga_calidad_leonardo.py`). Cada fila es un comentario, con
# `author_channel_id` (autor) y `video_id` (video) ya listos para construir
# la red sin volver a limpiar nada.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import networkx as nx

comments = pd.read_csv(ROOT / "data" / "processed" / "comments_clean.csv")
videos = pd.read_csv(ROOT / "data" / "processed" / "videos_clean.csv")

# %% [markdown]
# ## 4.1 / 4.2 Construccion de la red bipartita (pendiente)
# - Nodos tipo "autor" (author_channel_id) y nodos tipo "video" (video_id).
# - Arista autor-video SOLO si el autor comento en ese video; peso = numero
#   de comentarios de ese autor en ese video (`comments.groupby(['author_channel_id','video_id']).size()`).
# - Recordar: NO usar reply_count para crear aristas entre autores (el
#   enunciado prohibe expresamente inferir "quien respondio a quien").

# %% [markdown]
# ## 4.3 Tablas de nodos y aristas (pendiente)
# - Tabla de nodos: id, tipo ('autor'/'video'), atributos relevantes
#   (para autor: author_name/author_handle, num. de videos distintos donde comento;
#   para video: title, channel_name, category, view_count).
# - Tabla de aristas: source, target, weight (num. comentarios).

# %% [markdown]
# ## 4.4 Visualizacion de la red completa (pendiente)

# %% [markdown]
# ## 4.5 Interpretacion de la arista (pendiente)
# Una arista autor-video significa unicamente "este autor publico al menos
# un comentario principal en este video". NO implica conversacion directa
# con otros autores del mismo video, ni aprobacion/desaprobacion del
# contenido, ni relacion de amistad entre autores que comparten un video.
