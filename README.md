## Proyecto Individual Nº1
## Machine Learning Operations (MLOps)

¡Bienvenidos a mi proyecto individual de Machine Learning Operations (MLOps)!:smiley:

### Descripción del proyecto

En este proyecto, se asume el rol de un MLOps Engineer de una plataforma multinacional de videojuegos.

### ObjetivosObjetivos

- Procesar los datos disponibles mediante ETL.

- Realizar un análisis de sentimiento según las reseñas:

 1. Reseña Positiva = **2**

 2. Reseña Neutra = **1**

 3. Reseña Negativa = **0**

- Realizar el análisis exploratorio (EDA).

- Realizar un  un sistema de recomendación aplicando ML.

- Desarrollar 6 funciones:

 1. **PlayTimeGenre** : Debe devolver año con más horas jugadas para dicho género.

 2. **UserForGenre**: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

 3. **UsersRecommend**: Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

 4. **UsersNotRecommend**: Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.

 5. **SentimentAnalysis**: Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

 6. **recommend_games**: Ingresando el título del video juego, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

- Desarrollar una API  en el cual las funciones son utilizadas como consultas.

- Alojar la API utilizando un servicio en la nube.

### Resumen

Como la calidad y madurez de los datos era baja, se realizó un proceso de transformación y limpieza sobre los mismos.

Posteriormente, se se procede al análisis exploratorio de los datos (EDA), con la finalidad de encontrar los juegos y géneros más relevantes que, según el grado de importancia, se utilizarán para el sistema de recomendación.
Como resultado, el sistema de recomendación tiene las siguientes características:

- Esta alimentado por 78 títulos y 9 géneros.
- Esta basado en una relación ítem-ítem (título-título).
- Aplica la 'similitud del coseno' para las predicciones.

Por último, se desarrolló una API interactiva utilizando el framework FastAPI para disponibilizar  diferentes tipos de consultas, entre ellas, el sistema de recomendación. 
La API se deployó utilizando el servicio Render para que sea consumible desde la web. 
Puedes realizar las consultas en el siguiente enlace:

## API: https://proyecto-1-xykt.onrender.com/docs

### Flujo de trabajo

![Flujo-Readme](https://github.com/Rodzxc/Proyecto1/assets/133074545/e9ab7081-d960-4de0-a8e8-61750410cde2)

### Repositorio y archivos relevantes

En el repositorio de GitHub - Rodzxc/Proyecto1, puedes encontrar los siguientes archivos relevantes:

- EDA+CSV_ML: Contiene los códigos y las visualizaciones generadas durante el análisis exploratorio de datos. Aquí también se procesa el dataset necesario para alimentar al sistema de recomendación.

- ETL+CSV: Contiene los códigos y los detalles del procesamiento de datos necesarios para el proyecto.

- Funciones_API: Contiene los códigos correspondientes a las funciones implementadas en la API.

Además de estos archivos, el repositorio también puede contener otros recursos  adicionales utilizados en el proceso de desarrollo.

### Conclusiones

En este proyecto se ponen a prueba los conocimientos adquiridos durante el Bootcamp.
Se logra experiencia asumiendo el rol de un MLOps, familiarizandome con su trabajo y facultades.

¡Gracias por visitar mi proyecto! 
Si tienes dudas o necesitas más información, contactarme.
