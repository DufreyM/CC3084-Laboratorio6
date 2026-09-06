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

Ya reportado en outputs/reporte_ejercicio_7_8.md: la Comunidad 0 ('Que rico come tu diputado') es 81% negativa, la Comunidad 1 ('cooptacion USAC') 58% negativa pero con mas mezcla (22% positiva), y la Comunidad 2 (los 3 videos de consumidor/servicios de Quorum) es la mas equilibrada del top-3 (50% negativa, 26% positiva) -- consistente con ser contenido mas informativo y menos indignante que el escandalo de los diputados.

## 9.3 Hallazgos

- El sentimiento negativo domina pero NO es uniforme: varia fuertemente por TEMA del video, no por canal en si (el mismo canal Quorum tiene desde 81% NEG hasta comentarios mas mixtos segun el video especifico).
- El unico foco de sentimiento mayoritariamente positivo (Plan 2032 Ciudad de Guatemala) esta asociado a contenido aspiracional/de futuro sobre la ciudad, comentado en buena parte por guatemaltecos en el extranjero, sugiriendo que el patron 'negativo por default' de este corpus refleja sobre todo el sesgo tematico de que dato de video se recolecto (mucho escandalo politico), no necesariamente el animo general de los usuarios de YouTube guatemaltecos (ver limitaciones, ejercicio 10).
- El video de deportaciones de Telemundo (con comentarios en ingles, ver ejercicio 3.6) tambien es mayoritariamente negativo (64%), pero con un componente de discusion polarizada visible en las respuestas en ingles captadas en el dataset (ej. discusion entre 'eugeneramirez4405' y 'rosadiaz6945').