import pandas as pd
import numpy as np

from src.database.manager import DatabaseManager
from src.movie.movie_utils import estimate_img_url_exist


class MovieRecommence:

    def __init__(self):

        self.db_manager = DatabaseManager()
        self.rating_df, rating_matrix_df = self.db_manager.get_movie_matrix()
        self.movie_index = rating_matrix_df.columns
        self.corr_matrix = np.corrcoef(rating_matrix_df.T)

    def get_similar_movies(self, movie_title):
        """
        Returns correlation vector for a movie
        """

        movie_idx = list(self.movie_index).index(movie_title)

        return self.corr_matrix[movie_idx]

    def get_movie_recommendations(self, user_movies):
        """given a set of movies, it returns all the movies sorted by their correlation with the user"""

        similar_movies_df = pd.DataFrame()
        movie_similarities = np.zeros(self.corr_matrix.shape[0])
        for movie_id in user_movies:
            movie_similarities = movie_similarities + self.get_similar_movies(movie_id)

            similar_movies_df = pd.DataFrame({
                'title': self.movie_index,
                'sum_similarity': movie_similarities
            })

        similar_movies_df = similar_movies_df.sort_values(by=['sum_similarity'], ascending=False)
        # print(similar_movies_df)
        return similar_movies_df

    def get_user_rec(self, sample_user):
        """
        This extracts the similar movies according to the movie user rated
        :param sample_user: user id
        :return: 24 similar movies
        """
        self.rating_df[self.rating_df.user_id == sample_user].sort_values(by=['ratings'], ascending=False)

        sample_user_movies = self.rating_df[self.rating_df.user_id == sample_user].title.tolist()
        recommendations = self.get_movie_recommendations(sample_user_movies)
        l_ = 20

        # We get the top 20 recommended movies
        inner_l = l_ + 24
        rec = recommendations.title.head(inner_l)[l_:]
        #
        reviews = []

        for item in rec:

            img, im_db, rating_info = self.db_manager.get_movie_info_title(item=item)
            img_url = img[0]
            rates = []
            rate_dates = []
            for rate_info in rating_info:
                rates.append(rate_info[0])
                rate_dates.append(rate_info[1])
            max_rate = max(rates)
            rate_date = rate_dates[rates.index(max_rate)].strftime("%Y/%m/%d")
            img_url = estimate_img_url_exist(img_url=img_url)
            # x = plot(int(im_db[0]))
            reviews.append([int(im_db[0]), item, img_url, str(""), max_rate / 100, rate_date])

        return reviews


if __name__ == '__main__':

    MovieRecommence()
