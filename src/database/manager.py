import pymysql
import pandas as pd

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USERNAME


class DatabaseManager:
    """
    This class reads the necessary information from the several tables and insert, update the value in table.
    """
    def __init__(self):
        """
        This initial function sets the database connection.
        """

        self.config = pymysql.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
        )
        self.cursor = self.config.cursor()

    def init_movies(self):
        """
        This reads the whole information from the movie table
        :return: movie table data
        """

        movie = 'SELECT * FROM movies'
        movies = pd.read_sql(movie, self.config)

        return movies

    def init_ratings(self):
        """
        This reads the whole information from the ratings table
        :return: ratings table
        """
        rating = 'SELECT * FROM ratings'
        ratings = pd.read_sql(rating, self.config)

        return ratings

    def get_ratings(self):
        """
        all_ratings: has only user_id, movie_id, ratings field of whole ratings table
        sub_ratings: first of all, get whole data of ratings table. then after getting new data by matching movie_id of
        movie table and rating table and grouping according to its size greater than 20, gets the size and mean field
        from the new data. And at last, it extracts only user_id, movie_id and ratings field.
        :return: all_ratings, sub_ratings
        """

        ratings = self.init_ratings()
        ratings.drop(['timestamp'], axis=1, inplace=True)

        all_ratings = ratings.pivot_table(index=['user_id'], columns=['movie_id'], values='ratings')

        rating2 = 'SELECT r.*, r1.size, r1.mean from ratings r ' \
                  'INNER JOIN (SELECT movie_id, COUNT(1) size, AVG(ratings) mean FROM ratings ' \
                  'GROUP BY movie_id HAVING COUNT(1) >= 20 ORDER BY 3 DESC) AS r1 ON r.movie_id = r1.movie_id'
        ratings2 = pd.read_sql(rating2, self.config)
        # ratings2.head()
        ratings2.drop(['timestamp'], axis=1, inplace=True)
        ratings2.drop(['size'], axis=1, inplace=True)
        ratings2.drop(['mean'], axis=1, inplace=True)

        sub_ratings = ratings2.pivot_table(index=['user_id'], columns=['movie_id'], values='ratings')

        return all_ratings, sub_ratings

    def get_user_ratings(self, user_id):
        """
        This reads the movie_id field from the ratings table according to user_id
        :param user_id: user_id of user
        :return: movie_id of user
        """

        self.cursor.execute('SELECT movie_id FROM ratings WHERE user_id = %s', user_id)
        movie_id_user = self.cursor.fetchone()

        return movie_id_user

    def get_movie_matrix(self):
        """
        This gets the whole data of ratings and movie table. After merging that 2 data sets, from that merged data gets
        user_id, ratings and title information.
        :return: ratings_df: merged data, ratings_matrix_df: data includes only user_id, ratings, title
        """

        ratings = self.init_ratings()
        movies = self.init_movies()
        del ratings['timestamp']

        ratings_df = pd.merge(ratings, movies, on='movie_id')[['user_id', 'title', 'movie_id', 'ratings']]

        ratings_matrix_df = ratings_df.pivot_table(values='ratings', index='user_id', columns='title')
        ratings_matrix_df.fillna(0, inplace=True)

        return ratings_df, ratings_matrix_df

    def get_youtube_movies(self):
        """
        This extracts the whole movie data, and merge it with movies genre. From the merged data, it drops img, title,
        movie_id, genre, year field to get the new movie data.
        :return: new movie data
        """

        movies_df = self.init_movies()
        new_movies_df = pd.concat([movies_df, movies_df.genre.str.get_dummies(sep='|')], axis=1)

        new_movies_df.drop(['img'], axis=1, inplace=True)
        new_movies_df.drop(['title'], axis=1, inplace=True)
        new_movies_df.drop(['movie_id'], axis=1, inplace=True)
        new_movies_df.drop(['genre'], axis=1, inplace=True)
        new_movies_df.drop(['year'], axis=1, inplace=True)

        return new_movies_df

    def get_login_info(self, username):
        """
        This extracts the user information with user_id, sex, age, password according to the name of user signed in.
        :param username: the name of user
        :return: password, user_id, sex, age
        """

        self.cursor.execute('SELECT user_id, sex, age, password FROM users WHERE name = %s', username)
        info = self.cursor.fetchone()
        user_id = int(info[0])
        sex = info[1]
        age = int(info[2])
        password = info[3]

        return password, user_id, sex, age

    def get_movie_search_data(self):
        """
        In the condition of matching the movie_id of movies and links table, this extracts the title and genre field of
        movie table and imdbId field of links table.
        :return: title of moive, imdbId of links, genre of movie
        """

        sql_search = 'SELECT DISTINCT movies.title, links.imdbId, movies.genre from movies, links ' \
                     'WHERE links.movie_id = movies.movie_id LIMIT 9300 '
        self.cursor.execute(sql_search)
        search_data = self.cursor.fetchall()

        return search_data

    def get_profile_movie_data(self, user_id):
        """
        According to user_id, and in the condition of matching the movie_id of movie, links and ratings table, this
        extracts the title of movie table, imdbId of links table and ratings and timestamp of ratings table.
        :param user_id: user_id of signed in user.
        :return: title of movie, imdbId of links, ratings and timestamp of ratings
        """

        self.cursor.execute(
            'SELECT movies.title, links.imdbId, ratings.ratings, FROM_UNIXTIME(ratings.timestamp) '
            'from movies, ratings, links '
            'WHERE user_id = %s AND movies.movie_id = ratings.movie_id AND ratings.movie_id=links.movie_id', user_id)
        data = self.cursor.fetchall()

        return data

    def get_movie_rating_info(self, user_id, movie_id):
        """
        First, according to imdbId, this extracts the movie_id of links table. Then with that movie_id and user_id,
        this extracts the ratings and timestamp of ratings table.
        :param user_id: user's id
        :param movie_id: imdbId of the current movie
        :return: movie_id, its tuple, ratings and timestamp of ratings table
        """
        self.cursor.execute('SELECT movie_id from links WHERE imdbId =%s', movie_id)
        m_id = self.cursor.fetchone()

        idx = m_id[0]

        sql2 = 'select ratings,FROM_UNIXTIME(ratings.timestamp) from ratings where user_id = %s AND movie_id = %s'
        self.cursor.execute(sql2, (user_id, idx))
        sql_rating = self.cursor.fetchone()

        return m_id, idx, sql_rating

    def get_movie_info_id(self, movie_id, user_id):
        """
        This extracts the title, year, genre, img of moive table with movie_id. Then in the condition of matching the
        movie_id of movies table and ratings table, user_id of users table and ratings table, this extracts top 10
        the name, age, sex of users table, title of movies table, ratings and timestamp of ratings table with movie_id.
        Also, it calculates the average rating of ratings with movie_id and extracts all ratings of ratings table with
        user_id and movie_id
        :param movie_id: imdbId of movie
        :param user_id: user_id of user
        :return: movie_id, ratings and timestamp of ratings table, top 10 data, average rating, all rating, movie info
        """

        m_id, idx, sql_rating = self.get_movie_rating_info(user_id=user_id, movie_id=movie_id)
        if sql_rating is None:
            sql_rating = [0, "Never Rated"]

        self.cursor.execute('SELECT title, year, genre, img from movies WHERE movie_id = %s', idx)
        movie_info = self.cursor.fetchone()

        sql3 = 'SELECT users.name, movies.title, ratings.ratings, FROM_UNIXTIME(ratings.timestamp), users.sex, ' \
               'users.age from ratings, movies, users' \
               ' WHERE ratings.movie_id=%s and movies.movie_id = ratings.movie_id and ' \
               'ratings.user_id = users.user_id LIMIT 10'
        self.cursor.execute(sql3, idx)
        notification_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Round(AVG(ratings)) from ratings where movie_id=%s', m_id[0])
        avg_rating = self.cursor.fetchone()

        self.cursor.execute('SELECT * from ratings where user_id = %s and movie_id = %s', (user_id, m_id[0]))
        rated = self.cursor.fetchone()

        return idx, sql_rating, notification_data, avg_rating, rated, movie_info

    def get_movie_name_img_id(self, movie_id):
        """
        This extracts the title and img of movie table, imdbId of links table with movie_id.
        :param movie_id: movie_id of the movie
        :return: title of movie, image of movie, imdbId of links
        """

        self.cursor.execute('SELECT title from movies WHERE movie_id =%s', (int(movie_id)))
        name = self.cursor.fetchone()
        self.cursor.execute('SELECT img from movies WHERE movie_id =%s', (int(movie_id)))
        img = self.cursor.fetchone()
        self.cursor.execute('SELECT imdbid from links WHERE movie_id =%s', (int(movie_id)))
        im_db = self.cursor.fetchone()

        return name, img, im_db

    def get_movie_like_id(self, imdb_id):
        """
        This extracts the movie_id of links table with its imdbId. Also, this extracts the year, title and img of movie
        table with its movie_id.
        :param imdb_id: imdbId of the movie
        :return: year, title, image of movie
        """

        self.cursor.execute('SELECT movie_id from links WHERE imdbId =%s', imdb_id)
        m_id = self.cursor.fetchone()

        self.cursor.execute('SELECT DISTINCT movies.year, movies.title, movies.img from movies '
                            'WHERE movie_id = %s', (int(m_id[0])))
        name = self.cursor.fetchone()

        return name

    def get_movie_info_title(self, item):
        """
        This extracts the img and movie_id of movie table with its title, then the imdbId of links table with its
        movie_id. Also this extracts the ratings and timestamp of ratings table with the above movie_id
        :param item: the title of the current movie
        :return: image of movie, imdbId of links, ratings and timestamp of ratings
        """

        self.cursor.execute('SELECT img from movies WHERE title =%s', (str(item)))
        img = self.cursor.fetchone()
        self.cursor.execute('SELECT movie_id from movies WHERE title =%s', (str(item)))
        mid = self.cursor.fetchone()
        self.cursor.execute('SELECT imdbid from links WHERE movie_id =%s', (int(mid[0])))
        im_db = self.cursor.fetchone()

        sql2 = 'select ratings, FROM_UNIXTIME(ratings.timestamp) from ratings where movie_id = %s'
        self.cursor.execute(sql2, (mid[0]))
        sql_rating = self.cursor.fetchall()

        return img, im_db, sql_rating

    def register_new_user(self, new_name, new_gender, new_age, new_master, new_pwd):
        """
        This inserts the new user with user_name, gender, age, field and password
        :param new_name: the name of user
        :param new_gender: the gender of user
        :param new_age: the age of user
        :param new_master: the field of user
        :param new_pwd: the password of user
        :return: None
        """

        self.cursor.execute('select MAX(user_id) from users')
        max_id = self.cursor.fetchone()
        self.cursor.execute('insert into users VALUES (%s,%s,%s,%s,%s,%s)', (max_id[0] + 1, new_name, new_gender,
                                                                             new_age, new_master, new_pwd))
        self.config.commit()

        return

    def rate_movie(self, movie_id, user_id, rate_val, time_stamp):
        """
        This inserts or updates the rating information with new rating and timestamp
        :param movie_id: the imdbId of the current movie
        :param user_id: the user id
        :param rate_val: the new rating value
        :param time_stamp: the current timestamp
        :return: None
        """

        self.cursor.execute('SELECT movie_id from links WHERE imdbId =%s', movie_id)
        m_id = self.cursor.fetchone()

        self.cursor.execute('SELECT * from ratings where user_id = %s and movie_id = %s', (user_id, m_id[0]))
        works = self.cursor.fetchone()

        if works is None:
            self.cursor.execute('insert into ratings VALUES (%s,%s,%s,%s)', (user_id, m_id[0], rate_val, time_stamp))
            self.config.commit()
        else:
            self.cursor.execute('update ratings set ratings = %s,timestamp = %s where user_id = %s and movie_id = %s',
                                (rate_val, time_stamp, user_id, m_id[0]))
            self.config.commit()

        return


if __name__ == '__main__':
    DatabaseManager()
