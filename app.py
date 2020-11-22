import os
import time

from flask import Flask, session, render_template, request, redirect, url_for, g
from src.movie.user_recommender import MovieRecommence
from src.database.manager import DatabaseManager
from src.movie.scrap import get_rec
from src.movie.youtube import get_genre, gen_movies
from src.movie.movie_utils import estimate_img_url_exist
from settings import SERVER_PORT, SERVER_HOST, WEB_SERVER

app = Flask(__name__)
app.secret_key = os.urandom(24)
db_manager = DatabaseManager()
movie_recommence = MovieRecommence()
all_movies = db_manager.get_movie_search_data()
all_genres = get_genre()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    When user signs in, it returns the movie recommended page if user has a rated movie, or rated page so that the user
    can rate even a movie at least.
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password, user_id, sex, age = db_manager.get_login_info(username=username)
        # passw = str(password[0])

        if request.form['password'] == password:
            session['user'] = user_id
            session['password'] = request.form['password']
            session['u_sex'] = sex
            session['u_age'] = age
            session['user_name'] = username

            return redirect(url_for('protected'))

    return render_template("index.html")


@app.route('/genre')
def genre():
    """
    It gets all the genres and returns them to the search page
    :return:
    """
    if g.user:
        gen = get_genre()
        return render_template('genre.html', genres=gen)


@app.route('/genremovies/<mgenre>')
def genremovies(mgenre):
    """
    It gets the movies of specific genre and returns them to the search page
    :param mgenre:
    :return:
    """
    if g.user:
        x = str(mgenre)
        gen = gen_movies(x)
        print(gen)
        return render_template('genmov.html', movgen=gen)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    It returns the search page with all the genres
    :return:
    """
    search_result = []

    if request.method == 'POST':
        search_imdb_id = request.form.get('search')
        search_result = db_manager.get_movie_like_id(imdb_id=search_imdb_id)
        search_result = list(search_result)
        search_result[2] = estimate_img_url_exist(img_url=search_result[2])
        search_result.append(search_imdb_id)

    return render_template("search.html", res=search_result, movie_lists=all_movies, genre_lists=all_genres)


@app.route('/search/<s_genre>')
def get_movies_for_genre(s_genre):
    """
    It returns the movies of the specific genre
    :param s_genre:
    :return:
    """
    if g.user:
        genre_name = str(s_genre)
        genre_movies = []
        if genre_name == "all":
            genre_movies = all_movies
        else:
            for s_movie in all_movies:
                if genre_name in s_movie[2]:
                    genre_movies.append(s_movie)

        return render_template("search.html", res=[], movie_lists=genre_movies, genre_lists=all_genres)
    else:
        return redirect(url_for('index'))


@app.route('/srch', methods=['GET', 'POST'])
def srch():
    """

    :return:
    """
    select = request.form.get('search')
    return redirect(url_for('.movie', movie_id=str(select)))


@app.route('/logout')
def logout():
    """
    It returns the first page
    :return:
    """
    drop_session()
    return redirect(url_for('index'))


@app.route('/protected')
def protected():
    """
    It returns the 24 recommended movies similar to the movie user rated.
    :return:
    """
    if g.user:
        rating_user = db_manager.get_user_ratings(user_id=g.user)
        if rating_user:

            if g.user:
                imdbid = movie_recommence.get_user_rec(int(g.user))

                return render_template('regout.html', name=session['user_name'], imdbid=imdbid)
        else:
            return render_template("search.html", res=[], movie_lists=all_movies, genre_lists=all_genres)
    else:
        return redirect(url_for('index'))


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    """
    It returns the register page for new user
    :return:
    """
    if request.method == 'POST':
        session['name'] = request.form['username']
        session['gender'] = request.form['gender']
        session['age'] = request.form['age']
        session['occupation'] = request.form['occupation']
        session['password'] = request.form['password']
        return redirect(url_for('register'))

    return render_template("signup.html")


@app.route('/register')
def register():
    """
    When new user is registered, his information is inserted into the database
    :return:
    """

    reg_name = session['name']
    reg_gender = session['gender']
    reg_age = session['age']
    reg_master = session['occupation']
    reg_pwd = session['password']

    db_manager.register_new_user(new_age=reg_age, new_name=reg_name, new_gender=reg_gender, new_master=reg_master,
                                 new_pwd=reg_pwd)

    return redirect(url_for('index'), )


@app.route('/profile')
def profile():
    """
    It returns all the information that user rated to the movies
    :return:
    """
    if g.user:
        uid = g.user
        profile_data = db_manager.get_profile_movie_data(user_id=uid)
        profile_list = list(profile_data)

        return render_template("profile.html", name=session['user_name'], watched=profile_list)
    else:
        return redirect(url_for('index'), )


@app.route('/movie/<movie_id>')
def movie(movie_id):
    """
    It returns the your information of the specific movie, the information that others rated to that movie
    and top 10 similar movies to it
    :param movie_id:
    :return:
    """

    movie_id = movie_id.replace("(", "").replace(",", "").replace(")", "")
    if g.user:

        idx, sql_rating, notification_data, avg_rating, rated, movie_data = \
            db_manager.get_movie_info_id(movie_id=movie_id, user_id=g.user)
        all_ratings, sub_ratings = db_manager.get_ratings()
        if rated is None:
            rec = []
        else:
            rec = get_rec(idx, all_ratings, sub_ratings, 1)

        # info = movie_info(movie_id)

        return render_template("movie.html",
                               avg=avg_rating[0],
                               # link="static/"+link,
                               rec=rec,
                               minfo=movie_data,
                               sqlrating=sql_rating,
                               movie=movie_id,
                               name=session['user_name'],
                               notification=notification_data
                               )

    return redirect(url_for('index'))


@app.route('/rate/<rating>/<movie_id>')
def rate(rating, movie_id):
    """
    When user rates to new movie, it saves the corresponding information into the database.
    :param rating: the value of rating
    :param movie_id: imdbId of the movie
    :return:
    """
    if g.user:
        time_stp = int(time.time())
        movie_id = movie_id.replace("(", "").replace(",", "").replace(")", "")
        db_manager.rate_movie(movie_id=movie_id, user_id=g.user, rate_val=rating, time_stamp=time_stp)

        return redirect(url_for('.movie', movie_id=movie_id))

    return redirect(url_for("index"))


@app.route('/display')
def display_photo():
    """
    When user sign in, it reads his age and returns the photo corresponding to his age
    :return:
    """
    if g.user:
        user_age = session['u_age']
        user_sex = session['u_sex']
        sub_folder = "profile_pics/{}/".format(user_sex)
        if user_age == 1 or user_age == 18:
            filename = '1_18.png'
        else:
            filename = '{}.png'.format(str(user_age))

        return redirect(url_for('static', filename=sub_folder + filename), code=301)


@app.before_request
def before_request():
    """
    Returns the user id before sending a request
    :return:
    """
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/getsession')
def get_session():
    """

    :return:
    """
    if 'user' in session:
        return session['user']

    return 'not logged in yet'


@app.route('/dropsession')
def drop_session():
    """
    It drops the session of user
    :return:
    """
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    if WEB_SERVER:
        app.run()
    else:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
