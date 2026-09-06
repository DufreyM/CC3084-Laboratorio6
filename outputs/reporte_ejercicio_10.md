
## 10. Interpretacion, limitaciones y conclusiones

### 10.1 Los hallazgos en el contexto de participacion y consumo en YouTube

Este dataset no describe "la audiencia de YouTube en Guatemala": describe la
participacion observada en los comentarios de **19 videos de 293 recolectados**,
casi todos de tematica politica/noticiosa. Dentro de esa ventana, el patron mas
claro es que **ver un video y comentarlo son comportamientos distintos**: el video
mas visto del subconjunto (Plan 2032 Ciudad de Guatemala, ~304 mil vistas) no es
el mas comentado, y viceversa (Que rico come tu diputado, ~11.8 mil vistas, 161
comentarios). Esto sugiere que comentar en este corpus esta ligado a la
indignacion/controversia del contenido (escandalos de corrupcion, gastos
publicos) mas que al alcance/popularidad general del video.

La estructura de red confirma la misma historia desde otro angulo: la
participacion se concentra en un componente gigante alrededor de un solo video
("Que rico come tu diputado", que domina grado, intermediacion y PageRank), y el
resto son 9 audiencias-isla que nunca se cruzan entre si. Esto es consistente con
una dinamica de "indignacion viral puntual" mas que con una comunidad estable de
comentaristas politicos que sigue multiples contenidos.

### 10.2 Limitaciones

- **Cobertura de comentarios**: solo 19 de 293 videos (6.5%) tienen algun
  comentario en el dataset, y de esos, la mitad del volumen de comentarios viene
  de un solo video. No se puede asumir que los otros 274 videos no reciben
  comentarios en la realidad; simplemente no fueron recolectados aqui.
- **Seleccion por consultas de busqueda (`source_query`/`source_group`)**: el
  metodo de muestreo (topic vs. channel) determino que tipo de contenido entro al
  dataset; el ejercicio 3.6 muestra que el like promedio por comentario difiere
  6x entre ambos grupos (6.32 vs. 0.72), evidencia de que el metodo de
  recoleccion, no solo el contenido, explica parte de los patrones observados.
- **Fechas relativas**: `published_text` de los comentarios ("hace 2 años") no es
  una fecha exacta y depende del momento de scraping; no se pudo, por ejemplo,
  ordenar comentarios cronologicamente con precision ni analizar series de tiempo
  reales de participacion.
- **Conteos observados al momento de recoleccion**: `view_count`, `like_count` y
  `reply_count` son una fotografia de un instante, no el estado actual; dos
  videos "iguales" en el dataset pueden haber sido scrapeados en momentos muy
  distintos de su ciclo de vida (recien publicado vs. con años online).
- **Falta de relaciones explicitas entre autores**: como advierte el enunciado,
  `reply_count` no identifica a quien respondio; toda arista construida en este
  laboratorio es co-participacion (mismo video), nunca conversacion directa. El
  hallazgo de 36/406 `comment_id` con formato de respuesta de YouTube
  (`looks_like_reply_id`, ejercicio 2.1) sugiere ademas que el propio proceso de
  recoleccion mezclo accidentalmente algunas respuestas dentro del archivo de
  "comentarios principales", lo cual pudo inflar levemente algunos pesos de
  arista (ver ejercicio 4.1).
- **Concentracion extrema en pocos videos**: el top 10 de videos concentra 93.6%
  de los comentarios (ejercicio 3.2); cualquier metrica de red, sentimiento o
  tema esta dominada por el puñado de videos mas controversiales, no por una
  muestra equilibrada de contenido guatemalteco en YouTube.

### 10.3 Descripcion, asociacion e inferencia

Lo que se puede afirmar como **descripcion**: en esta muestra de 406 comentarios
sobre 19 videos, el 61.3% del texto fue clasificado como negativo, la red esta
dominada por un componente gigante alrededor de un video, y existen 17
comunidades detectadas por Louvain con modularidad 0.777.

Lo que se puede afirmar como **asociacion** (correlacional, no causal): los
videos encontrados por busqueda tematica muestran mas "me gusta" promedio por
comentario que los encontrados navegando canales directamente; los comentarios
editados muestran, en esta muestra pequeña (18 casos), menos likes promedio que
los no editados.

Lo que **NO se puede inferir** de estos datos: que la opinion publica
guatemalteca sobre sus politicos es mayoritariamente negativa (el sesgo de
seleccion hacia contenido de escandalo lo garantiza casi por diseño); que existe
una "comunidad de comentaristas politicos" cohesionada en YouTube Guatemala (lo
que se observa es, en su mayoria, 19 audiencias en gran parte aisladas, no una
comunidad); ni que los patrones de sentimiento/participacion de estos 332
autores generalizan a la poblacion de usuarios de YouTube en Guatemala o a la
poblacion del pais. El dataset es una muestra dirigida (por consultas de
busqueda especificas), no una muestra aleatoria ni censal.

### 10.4 Conclusiones integradas

Redes, contenido, sentimiento y limitaciones cuentan la misma historia desde
distintos angulos: este es un corpus **pequeño, sesgado hacia escandalo
politico-institucional, y estructuralmente fragmentado**. La red bipartita
autor-video (ejercicio 4) y sus proyecciones (ejercicio 5) muestran una
topologia de "un hub gigante + 9 islas" (ejercicio 6); la deteccion de
comunidades (ejercicio 7) recupera basicamente esa misma fragmentacion, con la
excepcion notable de una comunidad que fusiona 3 videos de contenido de
consumidor/servicios de Quorum, sugiriendo una audiencia fiel a ese tipo de
periodismo especifico, distinta de la audiencia mas amplia y volatil del
escandalo viral. La centralidad (ejercicio 8) identifica un puñado de autores y
videos "puente" cuya remocion fragmentaria aun mas la red, perfiles utiles
para entender que sostiene la (poca) conectividad del dataset. El analisis de
sentimiento (ejercicio 9) no contradice nada de esto: el tono negativo
predominante se explica mejor por que TEMA se recolecto (corrupcion, gasto
publico) que por un animo generalizado, como lo demuestra el contraejemplo
claro del video municipal de proyeccion urbana, mayoritariamente positivo. En
conjunto, los resultados son validos como descripcion de esta muestra especifica
y como ejercicio metodologico de analisis de redes sociales, pero no deben
leerse como un retrato representativo de YouTube Guatemala ni de la opinion
publica del pais.
