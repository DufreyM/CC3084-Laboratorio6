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
- La diferencia entre ambas es el hallazgo interesante: en general, un video con mas vistas SI tiende a tener mas comentarios (Spearman alto), pero la relacion lineal es casi nula porque dos videos rompen el patron: 'Plan 2032 Ciudad de Guatemala' tiene, por mucho, las mas vistas (~304 mil) pero un numero de comentarios apenas mediano (25); y 'Que rico come tu diputado' (Quorum) tiene, por mucho, mas comentarios que cualquier otro (161) con vistas relativamente bajas (~11.8 mil). Esto sugiere que las vistas miden alcance pasivo mientras que comentar refleja un tipo distinto de involucramiento (indignacion/controversia politica, en el caso de Quorum), que no escala linealmente con el alcance.
- Limitaciones de ambos conteos: `view_count` se congelo en el momento de la recoleccion (no representa vistas actuales) y los comentarios en este dataset son una MUESTRA (solo 19 de 293 videos tienen algun comentario), no el total real de comentarios de cada video en YouTube.

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