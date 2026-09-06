# Laboratorio 6 - Analisis de redes sociales en YouTube (Guatemala)

**Equipo:** Leonardo Mejia, Maria Jose, Mia Fuentes | CC3084 - Data Science, UVG

**Repositorio:** https://github.com/DufreyM/CC3084-Laboratorio6


## Ejercicios 1 y 2 - Carga, integracion, calidad y limpieza

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

- view_count_text (ej. '2,390 vistas') NO se reparsea: el dataset ya trae view_count numerico (recomendado explicitamente por el enunciado); se verifico que ambas fuentes son consistentes en orden de magnitud.
- like_count_text se convierte a like_count (entero): se quitan separadores de miles (',') y espacios; los valores vacios (' ') se interpretan como 0 'me gusta' (YouTube no muestra el contador cuando es 0). Se agrega la bandera booleana like_count_missing para distinguir estas filas de un 0 explicito.
  -> 189 de 406 comentarios (46.6%) tenian like_count_text vacio.
- query_hits, keywords (videos) y dataset_sources (ambos archivos) se convierten de texto con forma de lista/lista separada por '|' a listas de Python reales.

## 2.5 texto_original y texto_limpio

texto_original se conserva intacto (con mayusculas, puntuacion y emojis) porque el analisis de sentimiento (ejercicio 9) rinde mejor con esas senales. texto_limpio es la version normalizada usada para frecuencias, n-gramas y nube de palabras.

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
## 4.1 / 4.2 Construccion de la red bipartita

- Pares autor-video distintos (aristas): 343
- Aristas con peso > 1 (mismo autor con mas de un comentario principal en el mismo video): 40 de 343 (11.7%)
  Nota de interpretacion: parte de estos pesos altos coincide con videos donde ya se detecto (ejercicio 2.1) un numero alto de comment_id con formato de respuesta de YouTube (looks_like_reply_id); es probable que reflejen a una misma persona respondiendo varias veces DENTRO de un hilo de discusion (ej. 6 comentarios de un mismo autor en el video del Puente Belice II), no 6 comentarios independientes sin relacion entre si.

- Nodos tipo autor: 332
- Nodos tipo video: 19
- Total de nodos: 351 | Total de aristas: 343
- ¿Es bipartita? True

## 4.3 Tabla de nodos y aristas

- Tabla de nodos guardada en data/processed/red_bipartita_nodos.csv (351 filas: 19 videos + 332 autores).
- Tabla de aristas guardada en data/processed/red_bipartita_aristas.csv (343 filas: source=autor, target=video, weight=num. comentarios).

**Top 5 videos por numero de autores distintos que le comentaron:**
         id                                                      titulo                                 canal  n_autores_distintos  n_comentarios
n8iP75gIpmw                                   Qué rico come tu diputado                                Quorum                  128            161
j43HgwYFKfk               La cooptación de Walter Mazariegos en la USAC                                Quorum                   49             50
6W4u8sGEnGM  Inician los trabajos de recuperación del Puente Belice II. Gobierno de la República de Guatemala                   32             45
lj983NWyAQY                               Plan 2032 Ciudad de Guatemala            Municipalidad de Guatemala                   25             25
PjmxCj-a9Hg Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt Gobierno de la República de Guatemala                   19             25

**Top 5 autores por numero de videos distintos donde comentaron:**
                      id              nombre  n_videos_distintos  n_comentarios_totales
UCvcu1kR8xMYy_I1Ty-2mV2Q       @hashojea7348                   3                      4
UCpsKOkt5iWTbenzeuq7dsmQ      @inge_vergueta                   3                      3
UCHTGCgY2l-DQJIvlA_cpa_Q @virgiliogarcia3039                   2                      3
UCbrtvygfRT6QXqWDNrOf-cA     @Alejandro00710                   2                      2
UCdFlugHJJa4l3YqWuNRmvXw  @MarcosCarillo-b1r                   2                      2

## 4.4 Visualizacion

Se guardo en outputs/figs/09_red_bipartita_completa.png. Se grafican TODOS los 351 nodos y 343 aristas (sin filtrar ni podar nada por estetica); los videos (rojo, mas grandes, etiquetados con el titulo del video, mas informativo que el canal ya que 8 de los 19 videos con comentarios son de Quorum) actuan como 'hubs' claramente visibles, rodeados de sus autores (azul, pequeños). Los autores que comentaron en mas de un video aparecen conectados a mas de un hub rojo, y son visualmente identificables como los pocos nodos azules que caen ENTRE dos o mas grupos en vez de pegados a un solo hub.

## 4.5 Interpretacion de la arista

Una arista autor-video significa UNICAMENTE que ese autor publico al menos un comentario principal en ese video, y su peso es cuantos comentarios principales publico ahi (no respuestas, ver 4.1). Esto NO implica:
- que el autor haya conversado con otros autores que comentaron el mismo video (los datos no permiten saber si se leyeron entre si, ver advertencia del enunciado sobre reply_count);
- aprobacion o rechazo del contenido del video (un comentario muy critico genera la misma arista que uno elogioso);
- ninguna relacion de amistad, seguimiento o conocimiento mutuo entre autores que comparten un video comentado; solo indica co-participacion observada en el mismo espacio publico, en la ventana de tiempo/muestra que cubre este dataset.


![09_red_bipartita_completa.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/09_red_bipartita_completa.png)

## 3.1 Descriptivos minimos

- Videos: 293 | Canales: 97 | Comentarios: 406 | Autores unicos: 332
- De los 293 videos del dataset, solo 19 (6.5%) tienen al menos un comentario en este dataset (la recoleccion de comentarios fue selectiva, no exhaustiva).

**Videos por canal:** media=3.02, mediana=1, max=32 (canal con mas videos: Gobierno de la República de Guatemala)

**Comentarios por video** (solo los 19 con al menos uno): media=21.4, mediana=7, max=161
**Autores unicos por video:** media=18.1, max=128

**Visualizaciones (view_count, a nivel video):** media=60430, mediana=1175, max=8190449
**Respuestas (reply_count, a nivel comentario):** media=0.13, max=7, comentarios con >=1 respuesta: 30 (7.4%)
**Me gusta (like_count):** media=5.73, mediana=1, max=405

**Categorias de video** (nivel video vs. nivel comentario, es decir ponderado por cuantos comentarios trajo cada categoria):
                       n_videos  n_comentarios  %_videos  %_comentarios
category                                                               
News & Politics             138            335      47.1           82.5
Entertainment                48             70      16.4           17.2
Nonprofits & Activism         3              1       1.0            0.2
Education                    19              0       6.5            0.0
Comedy                        1              0       0.3            0.0
Music                         1              0       0.3            0.0
Film & Animation              2              0       0.7            0.0
People & Blogs               66              0      22.5            0.0
Science & Technology          6              0       2.0            0.0
Sports                        1              0       0.3            0.0
Travel & Events               8              0       2.7            0.0

**Consultas de busqueda (source_query, a nivel video):**
source_query
Municipalidad de Guatemala                20
@GobiernodelaRepublicadeGuatema           18
Gobierno de Guatemala                     18
@GobiernodeGuatemala                      17
guatemala noticias                        16
@MunicipalidaddeGuatemala-1551            16
Ministerio de Comunicaciones Guatemala    16
Conred Guatemala                          15

**Hashtags:** 1 hashtags en total, en 1 de 406 comentarios (el corpus casi no usa hashtags propios; los que aparecen vienen sobre todo de las descripciones/titulos de video, no de los comentarios de la audiencia).
[('IneptoBran', 1)]

**Palabras mas frecuentes (texto_limpio, 4845 tokens en total):**
pueblo        56
guatemala     52
dinero        34
solo          33
presidente    32
país          31
trabajo       30
diputados     28
corruptos     24
hacer         23
diputado      22
excelente     21
bueno         21
pais          21
ser           20

**Bigramas mas frecuentes:**
presidente bernardo    9
bernardo arevalo       8
ciudad guatemala       6
nery rodas             5
bla bla                5
pacto corruptos        5
viva guatemala         4
busquen trabajo        4
ser diputados          4
lleva años             4
dinero pueblo          4
comida nadie           4
guatemala saludos      4
muriendo hambre        4
excelente trabajo      3

## 3.2 Concentracion de la participacion

- Los 10 videos con mas comentarios (de 19 con al menos uno, de 293 en total) concentran el 93.6% de todos los comentarios.
- Los 3 canales con mas comentarios (Quorum, Gobierno de la República de Guatemala, Noticias Telemundo) concentran el 86.5% de todos los comentarios, de solo 8 canales con algun comentario (de 97 canales en total).
- Conclusion: la participacion observada NO esta repartida entre los 293 videos del dataset, sino extremadamente concentrada en un puñado de videos/canales; cualquier conclusion sobre 'la audiencia de YouTube en Guatemala' debe leerse como participacion en ese pequeño subconjunto, no como muestra representativa (ver seccion 10, limitaciones).

## 3.3 Popularidad vs. participacion

- Correlacion de Spearman (por rango) entre view_count y numero de comentarios, a nivel video (solo los 19 con >=1 comentario): 0.81. Correlacion de Pearson (lineal): 0.07.
- La diferencia entre ambas es el hallazgo interesante: en general, un video con mas vistas SI tiende a tener mas comentarios (Spearman alto), pero la relacion lineal es casi nula porque dos videos rompen el patron: 'Plan 2032 Ciudad de Guatemala' tiene, por mucho, las mas vistas (aprox. 304 mil) pero un numero de comentarios apenas mediano (25); y 'Que rico come tu diputado' (Quorum) tiene, por mucho, mas comentarios que cualquier otro (161) con vistas relativamente bajas (aprox. 11.8 mil). Esto sugiere que las vistas miden alcance pasivo mientras que comentar refleja un tipo distinto de involucramiento (indignacion/controversia politica, en el caso de Quorum), que no escala linealmente con el alcance.
- Limitaciones de ambos conteos: view_count se congelo en el momento de la recoleccion (no representa vistas actuales) y los comentarios en este dataset son una MUESTRA (solo 19 de 293 videos tienen algun comentario), no el total real de comentarios de cada video en YouTube.

## 3.4 Visualizaciones

Graficos guardados en outputs/figs/: top canales, top videos, histograma de vistas, categoria (video vs. comentario), dispersion vistas-vs-comentarios, top palabras, top bigramas y nube de palabras (esta ultima como complemento, no como grafico principal).

## 3.5 Preguntas obligatorias

**¿Que videos y canales concentran la mayor participacion observada?**
El video 'Que rico come tu diputado' (canal Quorum) concentra el mayor numero de comentarios (161, 39.7% del total). A nivel canal, Quorum por si solo recibe 256 comentarios (63.1% del total), seguido de Gobierno de la Republica de Guatemala y Noticias Telemundo/Municipalidad de Guatemala. Ver 3.2.

**¿Existen audiencias compartidas entre videos, canales o temas?**
Si: 9 de 332 autores (2.7%) comentaron en mas de un video del dataset, lo que confirma que existe una audiencia compartida entre videos (y en varios casos entre canales distintos). Esta es precisamente la base para la red bipartita autor-video del ejercicio 4 y sus proyecciones.

**¿Que autores funcionan como puentes entre contenidos que de otra forma permanecerian separados?**
Se identifican con precision en el ejercicio 8 (centralidad de intermediacion sobre la red construida en el ejercicio 4/5), pero en este EDA ya se observa la señal: autores como @ManuelEdran, @byronpontaza y @HaroldoCastillo-rh9iw aparecen comentando en mas de un video de Quorum, y @albertoshernandez5251 concentra varios comentarios en el video del Puente Belice II del canal de Gobierno.

**¿Que temas y sentimientos caracterizan las principales comunidades de participacion?**
Se profundiza en los ejercicios 7 y 9 (comunidades y sentimiento), pero el analisis de palabras/bigramas frecuentes ya apunta a un tema dominante de critica a la clase politica y corrupcion ('pueblo', 'dinero', 'diputados', 'corruptos', 'presidente bernardo', 'pacto corruptos'), junto a un nucleo minoritario de comentarios de apoyo/orgullo nacional ('viva guatemala', 'excelente trabajo').

**¿La visibilidad medida mediante visualizaciones coincide con la participacion observada?**
Parcialmente. Por rango de posicion (Spearman=0.81) hay una asociacion positiva bastante fuerte, pero linealmente (Pearson=0.07) practicamente no hay relacion: el video mas visto del subconjunto no es el mas comentado. Ver 3.3.

**¿Que conclusiones estan limitadas por el procedimiento de recoleccion y la cobertura de los datos?**
Todas las relacionadas con 'participacion promedio' o 'temas dominantes en Guatemala': solo 19/293 videos tienen comentarios en este dataset y estan fuertemente sesgados hacia contenido politico/de noticias (ver 3.2 y seccion 10).

## 3.6 Tres preguntas adicionales

**1. ¿Los videos encontrados por busqueda tematica (source_group='topic') generan comentarios con mas 'me gusta' en promedio que los encontrados navegando directamente el canal (source_group='channel')?**
Si, la diferencia es grande: 6.32 likes promedio por comentario en videos 'topic' vs. 0.72 en videos 'channel' (363 vs. 43 comentarios respectivamente). Es coherente con que la busqueda tematica trajo videos mas virales/controversiales (ej. 'Que rico come tu diputado'), mientras que navegar canal por canal trajo mas contenido institucional con poca interaccion.

**2. ¿En que videos aparecen comentarios en ingles y que los caracteriza?**
Deteccion automatica de idioma (langdetect, poco confiable en textos muy cortos, por eso se excluyen los de menos de 20 caracteres) encuentra 10 comentarios en ingles sobre 406 evaluados. Se concentran casi todos (7 de 10) en el video 'EE.UU. envia a mexicanos deportados a Guatemala... | Noticias Telemundo': tiene sentido, es un tema de politica migratoria de EE.UU. que atrae a comentaristas angloparlantes, distinto del resto del corpus que es abrumadoramente en español.

**3. ¿Los comentarios editados reciben, en promedio, menos 'me gusta' que los no editados?**
18 de 406 comentarios (4.4%) fueron editados despues de publicarse. Reciben en promedio 2.22 likes vs. 5.89 de los no editados. Es una tendencia descriptiva sobre una muestra pequeña (18 comentarios editados), no se puede afirmar causalidad, pero es consistente con la idea de que la edicion suele ocurrir en comentarios menos visibles/con menos interaccion previa (el autor corrige sin presion de una audiencia grande observando).


![01_top_canales_comentarios.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/01_top_canales_comentarios.png)



![02_top_videos_comentarios.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/02_top_videos_comentarios.png)



![03_histograma_views.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/03_histograma_views.png)



![04_categorias_video_vs_comentario.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/04_categorias_video_vs_comentario.png)



![05_scatter_views_vs_comentarios.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/05_scatter_views_vs_comentarios.png)



![06_top_palabras.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/06_top_palabras.png)



![07_top_bigramas.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/07_top_bigramas.png)



![08_wordcloud.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/08_wordcloud.png)

## 5.1 / 5.2 Proyecciones

- Autor-autor: 332 nodos, 10732 aristas.
- Video-video: 19 nodos, 11 aristas (de un maximo posible de 171).

**Distribucion de pesos en autor-autor:** {1: 10730, 2: 2}
Casi todas las aristas (10730 de 10732) tienen peso 1, es decir, ambos autores comparten EXACTAMENTE un video. Esto es en gran parte un artefacto mecanico de que la enorme mayoria de autores (323 de 332, ver ejercicio 3.5) solo aparece comentando en un unico video de todo el dataset: cualquier arista que involucre a esos autores forzosamente tiene peso 1. Solo 2 pares de autores comparten realmente 2 videos distintos, que es la unica evidencia de participacion genuinamente cruzada entre contenidos en esta proyeccion.

## 5.4 Visualizaciones

Se guardaron 3 figuras: (10) la proyeccion autor-autor completa, que se ve como una nube densa de pequenos 'clanes' (uno por video, ver 5.2); (11) SOLO los pares de autores que comparten 2+ videos, como complemento que aisla la señal de participacion cruzada real, mucho mas legible; y (12) la proyeccion video-video completa (19 nodos, facil de leer sin filtrar nada).
## 6.1 Topologia y fragmentacion


### Red bipartita autor-video
- Nodos: 351 | Aristas: 343 | Densidad: 0.0056
- Grado: media=1.95, mediana=1.0, min=1, max=128
- Componentes conexos: 10 | Tamano del mayor: 286 (81.5% del total de nodos)
- Nodos aislados (grado 0): 0
- Transitividad (global): 0.0000 | Clustering promedio (local): 0.0000
  Nota: la transitividad de una red bipartita es SIEMPRE 0 por definicion (no puede haber triangulos entre dos tipos de nodo alternados, solo ciclos de longitud par); no es un error de calculo, es una propiedad estructural.

### Proyeccion autor-autor
- Nodos: 332 | Aristas: 10732 | Densidad: 0.1953
- Grado: media=64.65, mediana=48.0, min=0, max=183
- Componentes conexos: 10 | Tamano del mayor: 276 (83.1% del total de nodos)
- Nodos aislados (grado 0): 4
- Transitividad (global): 0.9840 | Clustering promedio (local): 0.9720
  La transitividad muy alta (0.98) confirma que la proyeccion esta dominada por cliques casi perfectos: cuando tres autores comparten aunque sea un solo video en comun, automaticamente se forma un triangulo, porque un video con N autores genera un clique completo de tamano N en la proyeccion.

### Proyeccion video-video
- Nodos: 19 | Aristas: 11 | Densidad: 0.0643
- Grado: media=1.16, mediana=1.0, min=0, max=4
- Componentes conexos: 10 | Tamano del mayor: 10 (52.6% del total de nodos)
- Nodos aislados (grado 0): 9
- Transitividad (global): 0.3158 | Clustering promedio (local): 0.1491

**Distribucion de grado**, para saber si la mayoria tiene pocas conexiones o estan concentradas en pocos nodos:
- Bipartita: el 75% de los nodos tiene grado <= 1, pero el maximo es 128 (el video 'Que rico come tu diputado', ver ejercicio 4) -> distribucion muy desigual, tipica de redes con hubs (no aleatoria/uniforme).
- Video-video: grados van de 0 a 4; 9 de 19 videos (grado 0, totalmente aislados de los demas).

## 6.2 Cohesion

La red bipartita y sus proyecciones NO son cohesivas en el sentido de 'un solo bloque conectado': ambas tienen 10 componentes conexos, y el mas grande cubre 81.5% de los nodos de la bipartita pero deja 9 componentes de un solo video cada uno, totalmente aislados del resto (ver 6.3). La proyeccion autor-autor es MUY cohesiva DENTRO de cada componente (clustering aprox. 0.97, casi clique) pero eso es estructuralmente esperable y no implica cohesion social real entre esos autores (ver 4.5 y 5.3).

## 6.3 Perifericos y aislados

Desglose de los 10 componentes de la red bipartita:
  Componente 0: 286 nodos (10 video(s), 276 autor(es)) -> ['Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto', 'Arroz con pollo a la MONOPOLIO', 'Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales', 'La cooptación de Walter Mazariegos en la USAC', 'Internet: escoger el menos malo', 'Qué rico come tu diputado', 'Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu', 'Caminar en una ciudad hecha para carros', 'Inician los trabajos de recuperación del Puente Belice II.', 'Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt']
  Componente 1: 26 nodos (1 video(s), 25 autor(es)) -> ['Plan 2032 Ciudad de Guatemala']
  Componente 2: 19 nodos (1 video(s), 18 autor(es)) -> ['EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo']
  Componente 3: 5 nodos (1 video(s), 4 autor(es)) -> ['I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.']
  Componente 4: 4 nodos (1 video(s), 3 autor(es)) -> ['10 Preguntas a un año del Paro Nacional']
  Componente 5: 3 nodos (1 video(s), 2 autor(es)) -> ['Noticiero en Directo 1 pm, 28 de Agosto de 2026']
  Componente 6: 2 nodos (1 video(s), 1 autor(es)) -> ['¿Quiénes pagan más en Centroamérica?']
  Componente 7: 2 nodos (1 video(s), 1 autor(es)) -> ['Cruzando la ciudad a puro Transmetro']
  Componente 8: 2 nodos (1 video(s), 1 autor(es)) -> ['SHAI WA: la vecina queer de Casa Presidencial']
  Componente 9: 2 nodos (1 video(s), 1 autor(es)) -> ['Edén por Salud: empleo inclusivo para personas con discapacidad en Antigua | Super - Episodio 2']

**Interpretacion:** el componente gigante (286 nodos, 10 videos, 276 autores) muestra que esos 10 videos SI comparten audiencia entre si a traves de autores puente. Los otros 9 componentes son cada uno UN SOLO video con su propio publico exclusivo (algunos grandes, como 'Plan 2032 Ciudad de Guatemala' con 25 autores, o el video de deportaciones de Telemundo con 18): ninguno de sus comentaristas aparece comentando en ningun otro video de la muestra.
- Esto es **aislamiento observado**, no un hueco de datos: tenemos el 100% de los comentarios recolectados de esos videos y ninguno conecta con otro video.
- Pero tambien es **aislamiento posiblemente inflado por la cobertura de datos**: como el dataset solo capturo un puñado de comentarios por video (ver ejercicio 3.2) y no el historial completo de cada autor en YouTube, es esperable que autores que SI comentan en varios videos de estos canales en la vida real no aparezcan conectados aqui simplemente porque solo uno de sus comentarios entro en la muestra. No se puede distinguir con estos datos cual de las dos causas pesa mas.

**Videos-video aislados (sin ningun autor en comun con otro video):** 9 de 19.
**Autores aislados en la proyeccion autor-autor** (comentaron en un video donde fueron el unico comentarista): 4 de 332.

## 6.4 Hallazgos

- La red de participacion NO es una sola comunidad interconectada: es un hub gigante (los videos mas comentados de Quorum y del Gobierno, conectados por un puñado de autores que comentan en varios) rodeado de 9 audiencias totalmente aisladas, cada una fiel a un solo video.
- La densidad extremadamente baja de la bipartita (0.0056) y de video-video (0.064) contrasta con la densidad artificialmente alta de autor-autor (0.195, arrastrada por los cliques mecanicos); hay que leer 'densidad de la proyeccion' con cuidado, no como evidencia de cohesion social.
- La distribucion de grado extremadamente desigual (unos pocos nodos concentran casi todas las conexiones) es consistente con lo encontrado en el ejercicio 3.2 (concentracion de la participacion en pocos videos/canales): la estructura de red confirma, desde otro angulo, el mismo patron de concentracion.


![10_proyeccion_autor_autor.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/10_proyeccion_autor_autor.png)



![11_proyeccion_autor_autor_filtrada.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/11_proyeccion_autor_autor_filtrada.png)



![12_proyeccion_video_video.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/12_proyeccion_video_video.png)

## Sentimiento por comentario

sentimiento
NEG    249
NEU     79
POS     78

## 7.3 Numero de comunidades, tamanos y modularidad

- Numero de comunidades: 17
- Modularidad: 0.7774 (valores > 0.3 ya se consideran estructura de comunidad fuerte; 0.78 es muy alto, esperable dado lo fragmentada que ya vimos que es la red en el ejercicio 6).
- Tamanos (de mayor a menor):
  Comunidad 0: 126 nodos (1 video(s)) -> ['Qué rico come tu diputado']
  Comunidad 1: 48 nodos (1 video(s)) -> ['La cooptación de Walter Mazariegos en la USAC']
  Comunidad 2: 32 nodos (3 video(s)) -> ['Caminar en una ciudad hecha para carros', 'Arroz con pollo a la MONOPOLIO', 'Internet: escoger el menos malo']
  Comunidad 3: 31 nodos (1 video(s)) -> ['Inician los trabajos de recuperación del Puente Belice II.']
  Comunidad 4: 26 nodos (1 video(s)) -> ['Plan 2032 Ciudad de Guatemala']
  Comunidad 5: 19 nodos (1 video(s)) -> ['EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo']
  Comunidad 6: 19 nodos (1 video(s)) -> ['Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt']
  Comunidad 7: 14 nodos (1 video(s)) -> ['Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto']
  Comunidad 8: 8 nodos (1 video(s)) -> ['Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales']
  Comunidad 9: 8 nodos (1 video(s)) -> ['Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu']
  Comunidad 10: 5 nodos (1 video(s)) -> ['I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.']
  Comunidad 11: 4 nodos (1 video(s)) -> ['10 Preguntas a un año del Paro Nacional']
  Comunidad 12: 3 nodos (1 video(s)) -> ['Noticiero en Directo 1 pm, 28 de Agosto de 2026']
  Comunidad 13: 2 nodos (1 video(s)) -> ['¿Quiénes pagan más en Centroamérica?']
  Comunidad 14: 2 nodos (1 video(s)) -> ['SHAI WA: la vecina queer de Casa Presidencial']
  Comunidad 15: 2 nodos (1 video(s)) -> ['Edén por Salud: empleo inclusivo para personas con discapacidad en Antigua | Super - Episodio 2']
  Comunidad 16: 2 nodos (1 video(s)) -> ['Cruzando la ciudad a puro Transmetro']

## 7.4 Visualizacion

Guardada en outputs/figs/13_comunidades.png: cada color es una comunidad, los nodos grandes son videos y los pequenos autores. Se observa que casi todas las comunidades coinciden con un solo video (igual que los componentes conexos del ejercicio 6.3), EXCEPTO una comunidad que fusiona 3 videos distintos de Quorum en un solo grupo (ver 7.5), lo que confirma que Louvain SI encontro una subestructura mas fina que la mera conectividad.

## 7.5 Caracterizacion


**Comunidad 0** (126 nodos: 1 video(s), 125 autor(es))
- Videos/canales: [{'title': 'Qué rico come tu diputado', 'channel_name': 'Quorum', 'category': 'News & Politics'}]
- Comentarios en esta comunidad: 161
- Palabras mas frecuentes: {'pueblo': 50, 'dinero': 27, 'diputados': 27, 'trabajo': 23, 'diputado': 22, 'sueldo': 17, 'solo': 16, 'corruptos': 14}
- Sentimiento: {'NEG': 0.81, 'NEU': 0.14, 'POS': 0.06}
- Intensidad de participacion (comentarios/autor): 1.29

**Comunidad 1** (48 nodos: 1 video(s), 47 autor(es))
- Videos/canales: [{'title': 'La cooptación de Walter Mazariegos en la USAC', 'channel_name': 'Quorum', 'category': 'News & Politics'}]
- Comentarios en esta comunidad: 50
- Palabras mas frecuentes: {'usac': 9, 'corruptos': 7, 'universidad': 6, 'estudiantes': 6, 'excelente': 5, 'información': 5, 'pueblo': 4, 'pacto': 4}
- Sentimiento: {'NEG': 0.58, 'NEU': 0.22, 'POS': 0.2}
- Intensidad de participacion (comentarios/autor): 1.06

**Comunidad 2** (32 nodos: 3 video(s), 29 autor(es))
- Videos/canales: [{'title': 'Caminar en una ciudad hecha para carros', 'channel_name': 'Quorum', 'category': 'News & Politics'}, {'title': 'Arroz con pollo a la MONOPOLIO', 'channel_name': 'Quorum', 'category': 'News & Politics'}, {'title': 'Internet: escoger el menos malo', 'channel_name': 'Quorum', 'category': 'News & Politics'}]
- Comentarios en esta comunidad: 34
- Palabras mas frecuentes: {'excelente': 10, 'empresas': 8, 'solo': 7, 'internet': 7, 'ley': 7, 'país': 5, 'aquí': 5, 'información': 4}
- Sentimiento: {'NEG': 0.5, 'POS': 0.26, 'NEU': 0.24}
- Intensidad de participacion (comentarios/autor): 1.17

**Nota sobre la comunidad multi-video (la de 'Arroz con pollo a la MONOPOLIO' + 'Internet: escoger el menos malo' + 'Caminar en una ciudad hecha para carros'):** las tres son videos de Quorum sobre temas de consumidor/servicios/movilidad urbana (no politica-escandalo como el video mas grande), y comparten un nucleo de autores fieles a ese tipo de contenido de Quorum; es la evidencia mas clara de una 'comunidad tematica' real en este dataset, distinta de simplemente 'la audiencia de un video viral'.

## 8.2 Centralidad

**Top 8 autores por intermediacion** (recurrencia + diversidad: comentan en mas de un video, de comunidades distintas):
                                        nombre     grado  intermediacion  pagerank
UCHTGCgY2l-DQJIvlA_cpa_Q   @virgiliogarcia3039  0.005714        0.231584  0.003039
UCpsKOkt5iWTbenzeuq7dsmQ        @inge_vergueta  0.008571        0.218076  0.003325
UCzZ6dDCEsLMXbc5pCFXIprw          @josegil3813  0.005714        0.176832  0.002078
UCylqlpsh8ENNM1LqgQ1KbxA          @Jel.Awesh.M  0.005714        0.089153  0.003458
UCvcu1kR8xMYy_I1Ty-2mV2Q         @hashojea7348  0.008571        0.059705  0.004536
UCjZgFEowMBrsjodqfovzdKw  @franciscoflores3120  0.005714        0.057896  0.002294
UCbrtvygfRT6QXqWDNrOf-cA       @Alejandro00710  0.005714        0.032296  0.002454
UCsUCN0Yq_UyTvKjOJLmNrnQ     @moisesvaldez4043  0.005714        0.031862  0.002477

**Top 8 videos por intermediacion** (alcance dentro de la red + capacidad de conectar audiencias distintas):
                                                                                                 titulo     grado  intermediacion  pagerank
n8iP75gIpmw                                                                   Qué rico come tu diputado  0.365714        0.565698  0.167290
PjmxCj-a9Hg                                 Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt  0.054286        0.244028  0.024898
j43HgwYFKfk                                               La cooptación de Walter Mazariegos en la USAC  0.140000        0.227474  0.063195
6W4u8sGEnGM                                  Inician los trabajos de recuperación del Puente Belice II.  0.091429        0.187622  0.042587
ndAZjHqzzT8                                                             Internet: escoger el menos malo  0.028571        0.128293  0.013282
yLZS3JiEBg8                                                              Arroz con pollo a la MONOPOLIO  0.045714        0.063668  0.020448
06mFNPU0aB8          Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto  0.037143        0.054720  0.017509
is3Mk5oC19g  Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu  0.020000        0.027655  0.009861

Para **autores**: la intermediacion alta identifica a quienes comentan en videos de comunidades distintas (puentes reales), mientras que el grado por si solo en una bipartita autor-video rara vez pasa de 2-3 para autores (nadie comenta en decenas de videos), asi que la intermediacion es mas informativa que el grado para 'diversidad de participacion' en este dataset especifico.

Para **videos**: el grado (numero de autores distintos) ya identifica alcance directo, pero la intermediacion identifica algo distinto: cuales videos, si se quitaran, fragmentarian mas la red. 'Que rico come tu diputado' domina ambas medidas (grado Y intermediacion), consistente con ser el hub central de todo el dataset.

## 8.3 Puentes y articuladores

- **Puntos de articulacion totales** (nodos cuya eliminacion desconecta la red en mas piezas): 22 de 351.
- **Videos articuladores**: 15 de 19 -> ['Caminar en una ciudad hecha para carros', 'I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.', 'Plan 2032 Ciudad de Guatemala', 'EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo', 'Inician los trabajos de recuperación del Puente Belice II.', 'Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto', 'Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales', 'La cooptación de Walter Mazariegos en la USAC', 'Noticiero en Directo 1 pm, 28 de Agosto de 2026', 'Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt', 'Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu', 'Arroz con pollo a la MONOPOLIO', 'Qué rico come tu diputado', '10 Preguntas a un año del Paro Nacional', 'Internet: escoger el menos malo']
  Esto incluye a casi todos los videos con comentarios: es un efecto esperado de la estructura bipartita en estrella (ver ejercicio 6), donde cada video es el unico puente hacia sus propios autores exclusivos, asi que removerlo siempre desconecta a esos autores del resto.
- **Autores puente (articulacion)**: 7 -> ['@josegil3813', '@hashojea7348', '@moisesvaldez4043', '@virgiliogarcia3039', '@franciscoflores3120', '@MarcosCarillo-b1r', '@inge_vergueta']. Estos SI son un hallazgo mas interesante: son los pocos autores que unen dos videos/comunidades que de otro modo quedarian separados (coinciden con el top de intermediacion de 8.2).

- **Participantes recurrentes** (comentaron en mas de un video, ver ejercicio 3.5): 9 autores.


![13_comunidades.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/13_comunidades.png)

## 9.1 Resultados generales

Distribucion de sentimiento sobre los 406 comentarios: {'NEG': 0.613, 'NEU': 0.195, 'POS': 0.192}
El corpus es mayoritariamente NEGATIVO (61.3%), consistente con el tema dominante encontrado en el ejercicio 3 (critica a la clase politica y corrupcion: 'pueblo', 'dinero', 'corruptos', ver wordcloud).

**Ejemplos (auditoria cualitativa):**
- NEG (mas confiado): "Que indignante saber como se artan estos coches y finalmente el pueblo esta ciendo dañado"
- NEU (mas confiado): "Pregúntenle si se acuerda de la marca del vino que se toma todos los días"
- POS (mas confiado): "Es un proyecto extraordinario , vamos adelante mi guate hermosa!"

## 9.2 Sentimiento por canal

sentimiento                             NEG   NEU   POS    n
channel_name                                                
Quorum                                 0.70  0.16  0.14  256
Gobierno de la República de Guatemala  0.50  0.26  0.24   70
Noticias Telemundo                     0.64  0.28  0.08   25
Municipalidad de Guatemala             0.08  0.12  0.80   25
Noti7                                  0.29  0.50  0.21   14
PrensaLibreOficial                     0.86  0.14  0.00    7
TN23 Guatemala                         0.86  0.14  0.00    7
Noticiero Guatevisión 13 Hrs.          0.50  0.50  0.00    2

El canal mas negativo es Quorum (70% NEG, arrastrado por 'Que rico come tu diputado'), y el mas positivo por MUCHO es Municipalidad de Guatemala (80% POS), impulsado enteramente por el video 'Plan 2032 Ciudad de Guatemala', donde predominan comentarios nostalgicos y de orgullo de guatemaltecos en el extranjero ('saludos desde El Salvador', 'me encantaria vivir en esa Guatemala'), un tono completamente distinto al de critica politica.

## Sentimiento por video (solo videos con >=10 comentarios, para que la proporcion sea representativa)

sentimiento   NEG   NEU   POS                                                                                             titulo    n
video_id                                                                                                                             
n8iP75gIpmw  0.81  0.14  0.06                                                                          Qué rico come tu diputado  161
j43HgwYFKfk  0.58  0.22  0.20                                                      La cooptación de Walter Mazariegos en la USAC   50
6W4u8sGEnGM  0.40  0.31  0.29                                         Inician los trabajos de recuperación del Puente Belice II.   45
PjmxCj-a9Hg  0.68  0.16  0.16                                        Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt   25
OkXlHx0hx-8  0.64  0.28  0.08  EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo   25
lj983NWyAQY  0.08  0.12  0.80                                                                      Plan 2032 Ciudad de Guatemala   25
yLZS3JiEBg8  0.56  0.12  0.31                                                                     Arroz con pollo a la MONOPOLIO   16
06mFNPU0aB8  0.29  0.50  0.21                 Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto   14
ndAZjHqzzT8  0.33  0.33  0.33                                                                    Internet: escoger el menos malo   12

Grafico guardado en outputs/figs/14_sentimiento_por_video.png.

## Sentimiento por comunidad (ver ejercicio 7.5)

Ya reportado en outputs/reporte_ejercicio_7_8.md: la Comunidad 0 ('Que rico come tu diputado') es 81% negativa, la Comunidad 1 ('cooptacion USAC') 58% negativa pero con mas mezcla (22% positiva), y la Comunidad 2 (los 3 videos de consumidor/servicios de Quorum) es la mas equilibrada del top-3 (50% negativa, 26% positiva), consistente con ser contenido mas informativo y menos indignante que el escandalo de los diputados.

## 9.3 Hallazgos

- El sentimiento negativo domina pero NO es uniforme: varia fuertemente por TEMA del video, no por canal en si (el mismo canal Quorum tiene desde 81% NEG hasta comentarios mas mixtos segun el video especifico).
- El unico foco de sentimiento mayoritariamente positivo (Plan 2032 Ciudad de Guatemala) esta asociado a contenido aspiracional/de futuro sobre la ciudad, comentado en buena parte por guatemaltecos en el extranjero, sugiriendo que el patron 'negativo por default' de este corpus refleja sobre todo el sesgo tematico de que dato de video se recolecto (mucho escandalo politico), no necesariamente el animo general de los usuarios de YouTube guatemaltecos (ver limitaciones, ejercicio 10).
- El video de deportaciones de Telemundo (con comentarios en ingles, ver ejercicio 3.6) tambien es mayoritariamente negativo (64%), pero con un componente de discusion polarizada visible en las respuestas en ingles captadas en el dataset (ej. discusion entre 'eugeneramirez4405' y 'rosadiaz6945').


![14_sentimiento_por_video.png](C:/Users/leome/OneDrive/Desktop/Universidad/CC3084-Laboratorio6/outputs/figs/14_sentimiento_por_video.png)


## 10. Interpretacion, limitaciones y conclusiones

### 10.1 Los hallazgos en el contexto de participacion y consumo en YouTube

Este dataset no describe "la audiencia de YouTube en Guatemala": describe la
participacion observada en los comentarios de **19 videos de 293 recolectados**,
casi todos de tematica politica/noticiosa. Dentro de esa ventana, el patron mas
claro es que **ver un video y comentarlo son comportamientos distintos**: el video
mas visto del subconjunto (Plan 2032 Ciudad de Guatemala, aprox. 304 mil vistas) no es
el mas comentado, y viceversa (Que rico come tu diputado, aprox. 11.8 mil vistas, 161
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
- **Seleccion por consultas de busqueda (source_query/source_group)**: el
  metodo de muestreo (topic vs. channel) determino que tipo de contenido entro al
  dataset; el ejercicio 3.6 muestra que el like promedio por comentario difiere
  6x entre ambos grupos (6.32 vs. 0.72), evidencia de que el metodo de
  recoleccion, no solo el contenido, explica parte de los patrones observados.
- **Fechas relativas**: published_text de los comentarios ("hace 2 años") no es
  una fecha exacta y depende del momento de scraping; no se pudo, por ejemplo,
  ordenar comentarios cronologicamente con precision ni analizar series de tiempo
  reales de participacion.
- **Conteos observados al momento de recoleccion**: view_count, like_count y
  reply_count son una fotografia de un instante, no el estado actual; dos
  videos "iguales" en el dataset pueden haber sido scrapeados en momentos muy
  distintos de su ciclo de vida (recien publicado vs. con años online).
- **Falta de relaciones explicitas entre autores**: como advierte el enunciado,
  reply_count no identifica a quien respondio; toda arista construida en este
  laboratorio es co-participacion (mismo video), nunca conversacion directa. El
  hallazgo de 36/406 comment_id con formato de respuesta de YouTube
  (looks_like_reply_id, ejercicio 2.1) sugiere ademas que el propio proceso de
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
