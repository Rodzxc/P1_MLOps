from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()


#Archivos
m = pd.read_csv('merged_df.csv')
u = pd.read_csv('merged_df_2.csv')
ml = pd.read_csv('ml_df.csv')


#Funciones

# 1
@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero : str):

    # Filtro segun genero
    df_gen = m[m.genres == genero]

    # Mensaje si el genero de entrada no esta en la colunma 'genres'
    if df_gen.empty:
        return f"No se encontraron juegos del género {genero}"

    # Agrupamiento por anio, sumo los tiempos
    df_agrupado = df_gen.groupby('year')['playtime_forever'].sum().reset_index()

    #Anio con mas tiempo de juego
    anio_max_tiempo = df_agrupado[df_agrupado['playtime_forever'] == df_agrupado['playtime_forever'].max()]

    #Resultado
    res = {
        f"El año con más horas de juego para el género '{genero}' es {anio_max_tiempo.iloc[0]['year'].astype(int)}"
        }
    return res

# 2
@app.get("/UserForGenre/{genero}")
def UserForGenre(genero: str):

    # Filtra el DataFrame por el género y no distingue mayúsculas y minúsculas
    df_gen = m[m['genres'].str.contains(genero, case=False, na=False)].copy()

    # Mensaje si el genero de entrada no esta en la colunma 'genres'
    if df_gen.empty:
        return f"No se encontraron juegos del género {genero}"

    # Encuentra al usuario con más horas jugadas
    # DF 'Genres' + 'item_id'
    df_id_titles = df_gen['item_id'].drop_duplicates()
    # Filtro de DF 'u' segun el genero, en este filtro aparecen los titulos de dicho genero
    u_filt = u[u['item_id'].isin(df_id_titles)]

    # horas por jugador
    time_df = u_filt.groupby('user_id')['playtime_forever'].sum().reset_index()
    user = time_df.sort_values(by='playtime_forever', ascending=False).head(1)
    user_max = user.iloc[0,0]

    #Calculo de horas jugadas segun el anio('year')
    acum_year = df_gen.groupby('year')['playtime_forever'].sum().reset_index()
    acum_year.rename(columns={'year': 'Año', 'playtime_forever': 'Horas'}, inplace=True)

    # Convierte los resultados en una lista de diccionarios
    lista = acum_year.to_dict(orient='records')

    # Resultado
    res = {
        f"Usuario con más horas jugadas para el género {genero}": user_max,
        "Horas jugadas por año": lista
    }

    return res



# 3
@app.get("/UsersRecommend/{year}")
def UsersRecommend(year: int):

    # Filtra el DataFrame para el año específico
    df_filtered = u[u['year'] == year]

    if df_filtered.empty:
        return f"No se encontraron juegos para ese {year}"

    # Ordena el DataFrame por la columna 'sentiment_analysis' en orden descendente
    df_sorted = df_filtered.sort_values(by='sentiment_analysis', ascending=False)

    # Filtra los juegos que tienen un valor de 'recommend' igual a True
    df_top_recommendations = df_sorted[df_sorted['recommend']]

    # Obtiene los 3 juegos más recomendados
    top_3_recommended_games = df_top_recommendations.head(3)

    # El item_id de los 3 juegos recomendados
    items = top_3_recommended_games['item_id']

    # Titulo
    titulo = m[['item_id', 'title']].drop_duplicates()

    # Puestos
    puesto = []
    for i in items:
        c = titulo[titulo['item_id'] == i]
        if not c.empty:
            puesto.append(c.iloc[0]['title'])
    # Resultado
    res = {
        f"Puesto 1": puesto[0],
        "Puesto 2": puesto[1] ,
        "Puesto 3": puesto[2]
    }
    return res

#4
@app.get("/UsersNotRecommend/{year}")
def UsersNotRecommend(year : int):

    # Filtra el DataFrame para el año específico
    df_filtered = u[u['year'] == year]

    # Ordena el DataFrame por la columna 'sentiment_analysis' en orden ascendente
    df_sorted = df_filtered.sort_values(by='sentiment_analysis', ascending=True)

    # Filtra los juegos que tienen un valor de 'recommend' igual a False
    df_top_recommendations = df_sorted[df_sorted['recommend'] == False]

    # Obtiene los 3 juegos menos recomendados
    top_3_recommended_games = df_top_recommendations.head(3)

    # El item_id de los 3 juegos recomendados
    items = top_3_recommended_games['item_id']
    
    # Titulo
    titulo = m[['item_id', 'title']].drop_duplicates()
    
    # Puestos
    puesto = []
    for i in items:
        c = titulo[titulo['item_id'] == i]
        if not c.empty:
            puesto.append(c.iloc[0]['title'])
            
    # Resultado    
    res = {}
    
    if len(puesto) > 0:
        res["Puesto 1"] = puesto[0]
    if len(puesto) > 1:
        res["Puesto 2"] = puesto[1]
    if len(puesto) > 2:
        res["Puesto 3"] = puesto[2]
    return res

# 4
@app.get("/SentimentAnalysis/{year}")
def SentimentAnalysis(year: int):

    # Filtra el DataFrame para el año específico
    df_filtered = u[u['year'] == year]

    if df_filtered.empty:
        return f'Sin datos para {year}'

    # Resultado
    res = {}
    sentiment_counts = df_filtered['sentiment_analysis'].value_counts()

    if 2 in sentiment_counts:
        res["Positivos"] = int(sentiment_counts[2])
    if 1 in sentiment_counts:
        res["Neutro"] = int(sentiment_counts[1])
    if 0 in sentiment_counts:
        res["Negativo"] = int(sentiment_counts[0])

    return res

# 5
@app.get("/recommend_games/{title}")
def recommend_games(title : str):
    
    title = title.capitalize()
    
    # Busca el índice del juego de entrada
    try:
        game_idx = ml[ml['title'] == title].index[0]
    except IndexError:
        return "El juego no se encuentra en la base de datos"

    # Excluimos la columna 'titulo_juego' antes de calcular la similitud
    X = ml.drop(columns=['title'])

    # Calcula la similitud del coseno entre los juegos
    similarities = cosine_similarity(X)

    # Ordena los juegos por similitud (excluyendo el juego de entrada)
    similar_games_indices = similarities[game_idx].argsort()[::-1][1:]

    # Recomienda los juegos más similares
    recommended_games_indices = similar_games_indices[:5]
    recommended_games = ml.loc[recommended_games_indices, 'title'].tolist()

    puestos = [1 , 2 , 3 , 4 , 5]

    diccionario_combinado = {p: j for p, j in zip(puestos, recommended_games)}

   # Mostrar el diccionario resultante
    return diccionario_combinado
