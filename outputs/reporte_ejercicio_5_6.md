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

La red bipartita y sus proyecciones NO son cohesivas en el sentido de 'un solo bloque conectado': ambas tienen 10 componentes conexos, y el mas grande cubre 81.5% de los nodos de la bipartita pero deja 9 componentes de un solo video cada uno, totalmente aislados del resto (ver 6.3). La proyeccion autor-autor es MUY cohesiva DENTRO de cada componente (clustering ~0.97, casi clique) pero eso es estructuralmente esperable y no implica cohesion social real entre esos autores (ver 4.5 y 5.3).

## 6.3 Perifericos y aislados

Desglose de los 10 componentes de la red bipartita:
  Componente 0: 286 nodos (10 video(s), 276 autor(es)) -> ['Capturan a ladrón que había quedado grabado mientras robaba en una parroquia de Retalhuleu', 'Caminar en una ciudad hecha para carros', 'Conferencia de Prensa del Gobierno de Guatemala. #LaRondaGt', 'Inician los trabajos de recuperación del Puente Belice II.', 'Arroz con pollo a la MONOPOLIO', 'Internet: escoger el menos malo', 'Capturan a presuntos delincuentes disfrazados de mujer señalados de cometer asalto', 'Qué rico come tu diputado', 'La cooptación de Walter Mazariegos en la USAC', 'Bloqueos en Guatemala este 31 de agosto por alza en combustibles afectan rutas principales']
  Componente 1: 26 nodos (1 video(s), 25 autor(es)) -> ['Plan 2032 Ciudad de Guatemala']
  Componente 2: 19 nodos (1 video(s), 18 autor(es)) -> ['EE.UU. envía a mexicanos deportados a Guatemala antes de su regreso a México | Noticias Telemundo']
  Componente 3: 5 nodos (1 video(s), 4 autor(es)) -> ['I’x K’at: el primer equipo guatemalteco de pelota maya, conformado únicamente por mujeres.']
  Componente 4: 4 nodos (1 video(s), 3 autor(es)) -> ['10 Preguntas a un año del Paro Nacional']
  Componente 5: 3 nodos (1 video(s), 2 autor(es)) -> ['Noticiero en Directo 1 pm, 28 de Agosto de 2026']
  Componente 6: 2 nodos (1 video(s), 1 autor(es)) -> ['¿Quiénes pagan más en Centroamérica?']
  Componente 7: 2 nodos (1 video(s), 1 autor(es)) -> ['SHAI WA: la vecina queer de Casa Presidencial']
  Componente 8: 2 nodos (1 video(s), 1 autor(es)) -> ['Edén por Salud: empleo inclusivo para personas con discapacidad en Antigua | Super - Episodio 2']
  Componente 9: 2 nodos (1 video(s), 1 autor(es)) -> ['Cruzando la ciudad a puro Transmetro']

**Interpretacion:** el componente gigante (286 nodos, 10 videos, 276 autores) muestra que esos 10 videos SI comparten audiencia entre si a traves de autores puente. Los otros 9 componentes son cada uno UN SOLO video con su propio publico exclusivo (algunos grandes, como 'Plan 2032 Ciudad de Guatemala' con 25 autores, o el video de deportaciones de Telemundo con 18): ninguno de sus comentaristas aparece comentando en ningun otro video de la muestra.
- Esto es **aislamiento observado**, no un hueco de datos: tenemos el 100% de los comentarios recolectados de esos videos y ninguno conecta con otro video.
- Pero tambien es **aislamiento posiblemente inflado por la cobertura de datos**: como el dataset solo capturo un puñado de comentarios por video (ver ejercicio 3.2) y no el historial completo de cada autor en YouTube, es esperable que autores que SI comentan en varios videos de estos canales en la vida real no aparezcan conectados aqui simplemente porque solo uno de sus comentarios entro en la muestra. No se puede distinguir con estos datos cual de las dos causas pesa mas.

**Videos-video aislados (sin ningun autor en comun con otro video):** 9 de 19.
**Autores aislados en la proyeccion autor-autor** (comentaron en un video donde fueron el unico comentarista): 4 de 332.

## 6.4 Hallazgos

- La red de participacion NO es una sola comunidad interconectada: es un hub gigante (los videos mas comentados de Quorum y del Gobierno, conectados por un puñado de autores que comentan en varios) rodeado de 9 audiencias totalmente aisladas, cada una fiel a un solo video.
- La densidad extremadamente baja de la bipartita (0.0056) y de video-video (0.064) contrasta con la densidad artificialmente alta de autor-autor (0.195, arrastrada por los cliques mecanicos); hay que leer 'densidad de la proyeccion' con cuidado, no como evidencia de cohesion social.
- La distribucion de grado extremadamente desigual (unos pocos nodos concentran casi todas las conexiones) es consistente con lo encontrado en el ejercicio 3.2 (concentracion de la participacion en pocos videos/canales): la estructura de red confirma, desde otro angulo, el mismo patron de concentracion.