"""
Utilidades compartidas de carga, integracion y limpieza para el Laboratorio 6.

Este modulo es usado por los tres notebooks del equipo (uno por integrante)
para no repetir la logica de carga/limpieza tres veces y para garantizar que
los tres analisis parten exactamente del mismo dataset integrado.
"""
import ast
import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"

# Identificadores: NUNCA se sustituyen por nombres visibles (channel_name,
# author_name, video_title son solo descriptivos y pueden repetirse o cambiar).
VIDEO_ID_COLS = ["video_id", "channel_id"]
COMMENT_ID_COLS = ["comment_id", "video_id", "channel_id", "author_channel_id"]


def _parse_list_literal(value):
    """Convierte columnas tipo '[\"a\", \"b\"]' o '[]' a listas de Python."""
    if pd.isna(value):
        return []
    try:
        parsed = ast.literal_eval(value)
        return parsed if isinstance(parsed, list) else [parsed]
    except (ValueError, SyntaxError):
        return []


def _parse_pipe_list(value):
    """Convierte columnas tipo 'a.csv | b.csv | c.csv' a listas de Python."""
    if pd.isna(value):
        return []
    return [p.strip() for p in str(value).split("|") if p.strip()]


def load_videos(path=None):
    """Carga youtube_videos.csv y normaliza tipos/listas.

    Decisiones de limpieza:
    - encoding utf-8-sig porque el archivo trae BOM.
    - query_hits y keywords: de texto con forma de lista a list[str].
    - dataset_sources: de 'a.csv | b.csv' a list[str].
    - publish_date/upload_date: a datetime (coinciden 100% de las veces,
      ver diagnostico de calidad; se conservan ambas columnas para no
      alterar el archivo original, pero para analisis se recomienda usar
      publish_date).
    """
    path = path or (DATA_DIR / "youtube_videos.csv")
    df = pd.read_csv(path, encoding="utf-8-sig")

    df["query_hits"] = df["query_hits"].apply(_parse_list_literal)
    df["keywords"] = df["keywords"].apply(_parse_list_literal)
    df["dataset_sources"] = df["dataset_sources"].apply(_parse_pipe_list)
    df["publish_date"] = pd.to_datetime(df["publish_date"], utc=True, errors="coerce")
    df["upload_date"] = pd.to_datetime(df["upload_date"], utc=True, errors="coerce")
    df["n_keywords"] = df["keywords"].apply(len)
    df["n_query_hits"] = df["query_hits"].apply(len)

    return df


def load_comments(path=None):
    """Carga youtube_comments.csv y normaliza tipos/conteos.

    Decisiones de limpieza:
    - like_count_text llega como texto y puede venir vacio (' '). YouTube
      no muestra el contador cuando este es 0, por lo que un valor vacio
      se interpreta como 0 likes. Se documenta con la bandera
      'like_count_missing' para no perder el rastro de cuales filas no
      traian el dato explicito (aislamiento observado vs ausencia real).
    - dataset_sources: igual que en videos, a list[str].
    - is_pinned y viewer_rating: is_pinned es constante (siempre False) y
      viewer_rating esta vacia en el 100% de los registros; ambas se
      conservan en el dataframe pero se marcan como no utilizables para
      analisis (ver notebook 01, seccion 2.2).
    - comment_id con un '.' en medio sigue el formato de IDs de respuesta
      de YouTube (parentId.replyId), lo cual contradice la descripcion del
      dataset ('solo comentarios principales'). Se agrega la bandera
      'looks_like_reply_id' para dejar constancia de esta inconsistencia;
      NO se usa para construir aristas de respuesta (el enunciado prohibe
      inferir quien respondio a quien a partir de reply_count).
    """
    path = path or (DATA_DIR / "youtube_comments.csv")
    df = pd.read_csv(path, encoding="utf-8-sig")

    df["like_count_missing"] = df["like_count_text"].astype(str).str.strip().eq("")
    like_clean = (
        df["like_count_text"].astype(str).str.strip().str.replace(",", "", regex=False)
    )
    df["like_count"] = pd.to_numeric(like_clean, errors="coerce").fillna(0).astype(int)

    df["dataset_sources"] = df["dataset_sources"].apply(_parse_pipe_list)
    df["looks_like_reply_id"] = df["comment_id"].str.contains(r"\.", regex=True)

    return df


def integrate(videos=None, comments=None):
    """Integra ambos datasets por video_id (llave foranea en comments).

    Se usa un left join partiendo de comments porque el objetivo del
    laboratorio es analizar comentarios en contexto de su video; el 100%
    de los comment.video_id existen en videos (verificado en el
    diagnostico de calidad), por lo que no se pierden filas en el cruce.
    Las columnas duplicadas descriptivas de video (video_title,
    channel_name, channel_id) que ya vienen en comments se conservan con
    sufijo '_comment' para poder contrastarlas contra las de videos.
    """
    videos = videos if videos is not None else load_videos()
    comments = comments if comments is not None else load_comments()

    merged = comments.merge(
        videos,
        on="video_id",
        how="left",
        suffixes=("_comment", "_video"),
        indicator=True,
    )

    match_rate = (merged["_merge"] == "both").mean()
    return merged, match_rate


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE,
)
EMOJI_SHORTCODE_PATTERN = re.compile(r":[a-z0-9_+-]+:")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
MENTION_PATTERN = re.compile(r"@(\w+)")
PUNCT_NUMBERS_PATTERN = re.compile(r"[^a-záéíóúñü\s]")


def build_stopwords():
    """Stopwords en espanol (NLTK) + jerga/abreviaturas frecuentes en el
    corpus (chat/coloquial guatemalteco) que no aportan al analisis de
    tema/sentimiento."""
    import nltk

    try:
        from nltk.corpus import stopwords as nltk_stopwords

        base = set(nltk_stopwords.words("spanish"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        from nltk.corpus import stopwords as nltk_stopwords

        base = set(nltk_stopwords.words("spanish"))

    extra = {
        "q", "x", "xq", "pq", "d", "k", "ke", "jaja", "jajaja", "jeje", "ud", "uds",
        # el corpus es informal y casi nunca usa tildes: "si" (sin tilde) funciona la
        # mayoria de veces como el "si" afirmativo/condicional (con tilde), que SI esta
        # en la lista de NLTK; sin este agregado quedaba como la palabra mas frecuente
        # del corpus sin aportar contenido tematico (detectado en el analisis de
        # frecuencias del ejercicio 3).
        "si",
    }
    return base | extra


class TextCleaner:
    """Aplica la limpieza de texto documentada en el inciso 2.6 del enunciado.

    Se conserva SIEMPRE texto_original sin tocar (para auditoria y
    analisis de sentimiento, que se beneficia de puntuacion/mayusculas/
    emojis). texto_limpio es la version normalizada para frecuencias,
    n-gramas y nube de palabras.
    """

    def __init__(self):
        self.stopwords = build_stopwords()
        try:
            import spacy

            self.nlp = spacy.load(
                "es_core_news_sm", disable=["parser", "ner", "morphologizer"]
            )
            self.has_spacy = True
        except (ImportError, OSError):
            self.nlp = None
            self.has_spacy = False

    def extract_hashtags(self, text):
        return HASHTAG_PATTERN.findall(text)

    def extract_mentions(self, text):
        return MENTION_PATTERN.findall(text)

    def extract_emojis(self, text):
        """Devuelve tanto emojis Unicode reales (ej. 'gato') como emojis en
        formato de texto alternativo (ej. ':hand-purple-blue-peace:'), que
        aparecen en una fraccion pequena del corpus (2/406 comentarios) y
        provienen del texto alternativo que YouTube asigna a algunos
        emojis al momento de la extraccion."""
        return EMOJI_PATTERN.findall(text) + EMOJI_SHORTCODE_PATTERN.findall(text.lower())

    def clean(self, text):
        if not isinstance(text, str) or not text.strip():
            return ""

        t = text.lower()
        t = URL_PATTERN.sub(" ", t)
        t = MENTION_PATTERN.sub(" ", t)
        t = HASHTAG_PATTERN.sub(r"\1", t)
        t = EMOJI_SHORTCODE_PATTERN.sub(" ", t)
        t = EMOJI_PATTERN.sub(" ", t)
        t = PUNCT_NUMBERS_PATTERN.sub(" ", t)
        t = re.sub(r"\s+", " ", t).strip()

        tokens = [tok for tok in t.split() if tok not in self.stopwords and len(tok) > 1]

        if self.has_spacy and tokens:
            doc = self.nlp(" ".join(tokens))
            tokens = [tok.lemma_ for tok in doc if tok.lemma_ not in self.stopwords]

        return " ".join(tokens)


def save_processed(df, name):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / name
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    return out_path


LIST_COLUMNS = [
    "hashtags", "mentions", "emojis", "keywords", "query_hits",
    "dataset_sources", "dataset_sources_comment", "dataset_sources_video",
]


def load_processed(name):
    """Lee un CSV de data/processed/ y reconstruye a list[str] las columnas
    que save_processed() guardo como texto con forma de lista (ej. "['a']").
    Usado por los notebooks 02 y 03 para no volver a parsear a mano."""
    df = pd.read_csv(PROCESSED_DIR / name, encoding="utf-8-sig")
    for col in LIST_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(_parse_list_literal)
    return df
