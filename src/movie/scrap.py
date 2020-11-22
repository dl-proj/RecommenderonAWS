import multiprocessing as mp
import numpy as np

from src.database.manager import DatabaseManager
from src.movie.movie_utils import estimate_img_url_exist

db_manager = DatabaseManager()


def pearson(m1, m2):
    """
    This calculates the similarity of 2 movie ratings.
    :param m1: one movie rating
    :param m2: another movie rating
    :return: similarity value
    """
    m1_c = m1 - m1.mean()
    m2_c = m2 - m2.mean()
    cor = np.sum(m1_c * m2_c) / np.sqrt(np.sum(m1_c ** 2) * np.sum(m2_c ** 2))
    return cor


def get_rec(mid, all_movie, sub_movie, like):
    """
    This extracts 10 the most similar movies with the current movie.
    :param mid: the current movie_id
    :param all_movie: all the movies with movie information including rating
    :param sub_movie: the current movie
    :param like: top 10 or top 10:20
    :return: similar top 10 movies
    """
    reviews = []
    for title in sub_movie.columns:
        if title == mid:
            continue
        cor = pearson(all_movie[mid], sub_movie[title])

        if np.isnan(cor):
            continue
        else:
            name, img, im_db = db_manager.get_movie_name_img_id(movie_id=title)

            reviews.append([title, cor, name[0], img[0], im_db[0]])

    if like == 1:
        sorted_reviews = sorted(reviews, key=lambda x: x[1], reverse=True)[:10]
        for review in sorted_reviews:
            review[3] = estimate_img_url_exist(img_url=review[3])
        return sorted_reviews

    if like == 2:
        sorted_reviews = sorted(reviews, key=lambda x: x[1], reverse=False)[:10]
        for review in sorted_reviews:
            review[3] = estimate_img_url_exist(img_url=review[3])
        return sorted_reviews


if __name__ == '__main__':

    get_rec(mid="", sub_movie=[], all_movie="", like="")
