"""
Movie Recomendation System
Editado por: Elisa Gabriela Machado de Lucena
"""
# importando as biliotecas utilizadas
import logging
import re
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configurando o logging
logging.basicConfig(filename='movie_recommendation.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_data(caminho_arquivo):
    """
    Lê os dados de um arquivo CSV.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame contendo os dados.
    """
    try:
        return pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        logging.error("Arquivo não encontrado: %s", caminho_arquivo)
        print("CSV não encontrado")
        return None

def clean_title(title):
    """
    Limpa os títulos dos filmes, removendo caracteres extras.

    Args:
        title (str): O título do filme.

    Returns:
        str: O título limpo.
    """
    return re.sub("[^a-zA-Z0-9 ]", "", title)

def search(title):
    """
    Encontra a semelhança entre um termo de pesquisa e os títulos dos filmes.

    Args:
        title (str): O termo de pesquisa.

    Returns:
        pandas.DataFrame: Dataframe com os filmes mais semelhantes.
    """
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    return results

def find_similar_movies(movie_id):
    """
    Encontra filmes semelhantes com base no ID do filme que gostamos.

    Args:
        movie_id (int): O ID do filme de referência.

    Returns:
        pandas.DataFrame: Dataframe com os filmes recomendados.
    """
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > 0.10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]

# Função para pesquisa interativa de filmes
def on_type(data, search_function):
    """
    Atualiza a lista de filmes recomendados com base no termo de pesquisa.

    Args:
        data (dict): Dicionário com os dados do widget de pesquisa.
        search_function (function): A função de pesquisa a ser utilizada.

    Returns:
        None
    """
    with recommendation_list:
        recommendation_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            display(search_function(title))


# Importando os datasets que serão usados
movies = read_data("movies.csv")
ratings = read_data("ratings.csv")

# Pré-processamento dos dados
movies["clean_title"] = movies["title"].apply(clean_title)
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(movies["clean_title"])

# Widget interativo para pesquisa de filmes
movie_input = widgets.Text(value='Toy Story', description='Movie Title:', disabled=False)
movie_list = widgets.Output()

movie_input.observe(lambda data: on_type(data, search), names='value')
display(movie_input, movie_list)

# Widget interativo para busca de recomendações com base no nome do filme
movie_name_input = widgets.Text(value='Toy Story', description='Movie Title:', disabled=False)
recommendation_list = widgets.Output()

movie_name_input.observe(lambda data: on_type(data, find_similar_movies), names='value')
display(movie_name_input, recommendation_list)
