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
  Comunidad 2: 32 nodos (3 video(s)) -> ['Caminar en una ciudad hecha para carros', 'Internet: escoger el menos malo', 'Arroz con pollo a la MONOPOLIO']
  Comunidad 3: 31 nodos (1 video(s)) -> ['Inician los trabajos de recuperación del Puente Belice II.']
  Comunidad 4: 26 nodos (1 video(s)) -> ['Plan 2032 Ciudad de Guatemala']
  Comunidad 5: 19 nodos (1 video(s)) -> ['Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt']
  Comunidad 6: 19 nodos (1 video(s)) -> ['EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo']
  Comunidad 7: 14 nodos (1 video(s)) -> ['Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto']
  Comunidad 8: 8 nodos (1 video(s)) -> ['Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales']
  Comunidad 9: 8 nodos (1 video(s)) -> ['Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu']
  Comunidad 10: 5 nodos (1 video(s)) -> ['I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.']
  Comunidad 11: 4 nodos (1 video(s)) -> ['10 Preguntas a un año del Paro Nacional']
  Comunidad 12: 3 nodos (1 video(s)) -> ['Noticiero en Directo 1 pm, 28 de Agosto de 2026']
  Comunidad 13: 2 nodos (1 video(s)) -> ['Edén por Salud: empleo inclusivo para personas con discapacidad en Antigua | Super - Episodio 2']
  Comunidad 14: 2 nodos (1 video(s)) -> ['SHAI WA: la vecina queer de Casa Presidencial']
  Comunidad 15: 2 nodos (1 video(s)) -> ['¿Quiénes pagan más en Centroamérica?']
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
- Videos/canales: [{'title': 'Caminar en una ciudad hecha para carros', 'channel_name': 'Quorum', 'category': 'News & Politics'}, {'title': 'Internet: escoger el menos malo', 'channel_name': 'Quorum', 'category': 'News & Politics'}, {'title': 'Arroz con pollo a la MONOPOLIO', 'channel_name': 'Quorum', 'category': 'News & Politics'}]
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
- **Videos articuladores**: 15 de 19 -> ['Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto', 'I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.', 'Caminar en una ciudad hecha para carros', 'La cooptación de Walter Mazariegos en la USAC', 'Qué rico come tu diputado', 'Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales', 'Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt', 'Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu', 'Inician los trabajos de recuperación del Puente Belice II.', '10 Preguntas a un año del Paro Nacional', 'Internet: escoger el menos malo', 'Plan 2032 Ciudad de Guatemala', 'Noticiero en Directo 1 pm, 28 de Agosto de 2026', 'Arroz con pollo a la MONOPOLIO', 'EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo']
  Esto incluye a casi todos los videos con comentarios: es un efecto esperado de la estructura bipartita en estrella (ver ejercicio 6), donde cada video es el unico puente hacia sus propios autores exclusivos, asi que removerlo siempre desconecta a esos autores del resto.
- **Autores puente (articulacion)**: 7 -> ['@franciscoflores3120', '@virgiliogarcia3039', '@josegil3813', '@moisesvaldez4043', '@MarcosCarillo-b1r', '@inge_vergueta', '@hashojea7348']. Estos SI son un hallazgo mas interesante: son los pocos autores que unen dos videos/comunidades que de otro modo quedarian separados (coinciden con el top de intermediacion de 8.2).

- **Participantes recurrentes** (comentaron en mas de un video, ver ejercicio 3.5): 9 autores.