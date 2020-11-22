from src.database.manager import DatabaseManager
import pandas as pd
import numpy as np

db_manager = DatabaseManager()


def get_genre():
    """
    Returns all the genres of the movies
    :return: genres
    """

    movies_df = db_manager.get_youtube_movies()
    genres = list(movies_df)
    del genres[0]

    return genres


def gen_movies(x):
    """

    :param x:
    :return:
    """
    # a.execute('SELECT title from movies where genre LIKE %s',("%" +"action" +"%"))
    # mov = a.fetchall()
    gen = str(x)
    mov = db_manager.init_movies()
    rt_df = db_manager.init_ratings()

    lens = pd.merge(mov, rt_df)

    lens.drop(['year'], axis=1, inplace=True)
    lens.drop(['img'], axis=1, inplace=True)
    # lens = lens[lens['genre'].str.contains("Crime")]

    if gen == "Action":
        lens = lens[lens['genre'].str.contains("Action")]

    elif gen == "Adventure":
        lens = lens[lens['genre'].str.contains("Adventure")]

    elif gen == "Animation":
        lens = lens[lens['genre'].str.contains("Animation")]

    elif gen == "Children":
        lens = lens[lens['genre'].str.contains("Children")]

    elif gen == "Comedy":
        lens = lens[lens['genre'].str.contains("Comedy")]

    elif gen == "Crime":
        lens = lens[lens['genre'].str.contains("Crime")]

    elif gen == "Documentary":
        lens = lens[lens['genre'].str.contains("Documentary")]

    elif gen == "Drama":
        lens = lens[lens['genre'].str.contains("Drama")]

    elif gen == "Fantasy":
        lens = lens[lens['genre'].str.contains("Fantasy")]

    elif gen == "Film-Noir":
        lens = lens[lens['genre'].str.contains("Film-Noir")]

    elif gen == "Horror":
        lens = lens[lens['genre'].str.contains("Horror")]

    elif gen == "IMAX":
        lens = lens[lens['genre'].str.contains("IMAX")]

    elif gen == "Musical":
        lens = lens[lens['genre'].str.contains("Musical")]

    elif gen == "Mystery":
        lens = lens[lens['genre'].str.contains("Mystery")]

    elif gen == "Romance":
        lens = lens[lens['genre'].str.contains("Romance")]

    elif gen == "Sci-Fi":
        lens = lens[lens['genre'].str.contains("Sci-Fi")]

    elif gen == "Thriller":
        lens = lens[lens['genre'].str.contains("Thriller")]

    elif gen == "War":
        lens = lens[lens['genre'].str.contains("War")]

    elif gen == "Western":
        lens = lens[lens['genre'].str.contains("Western")]
    else:
        return "notworking"

    movie_stats = lens.groupby('title').agg({'ratings': [np.size, np.mean]})
    movie_stats.head()
    at_least_100 = movie_stats['ratings']['size'] >= 30
    movie_stats = movie_stats[at_least_100].sort_values([('ratings', 'mean')], ascending=False)[:20]
    movie_stats.head()

    # print(movie_stats)

    # movie_stats.drop(['size'], axis=1, inplace=True)
    top_gen_mov = []
    for index, row in movie_stats.iterrows():

        img, im_db, _ = db_manager.get_movie_info_title(item=index)
        # print(imdb[0])
        top_gen_mov.append((index, img[0], im_db[0]))
        # print(topgenmov)
        # list(mov.movie_id)
        # print(name)

    return top_gen_mov


if __name__ == '__main__':
    gen_movies(x="")
