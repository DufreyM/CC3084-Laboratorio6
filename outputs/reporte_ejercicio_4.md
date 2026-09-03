## 4.1 / 4.2 Construccion de la red bipartita

- Pares autor-video distintos (aristas): 343
- Aristas con peso > 1 (mismo autor con mas de un comentario principal en el mismo video): 40 de 343 (11.7%)
  Nota de interpretacion: parte de estos pesos altos coincide con videos donde ya se detecto (ejercicio 2.1) un numero alto de `comment_id` con formato de respuesta de YouTube (`looks_like_reply_id`); es probable que reflejen a una misma persona respondiendo varias veces DENTRO de un hilo de discusion (ej. 6 comentarios de un mismo autor en el video del Puente Belice II), no 6 comentarios independientes sin relacion entre si.

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