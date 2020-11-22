import requests


def plot(x):
    """
    This extracts the plot of movie with the corresponding movie imdbId.
    :param x: imdbId of the current movie
    :return: plot
    """

    if len(str(x)) == 7:
        url = 'https://www.omdbapi.com/?i=tt' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 6:
        url = 'https://www.omdbapi.com/?i=tt0' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 5:
        url = 'https://www.omdbapi.com/?i=tt00' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 4:
        url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 3:
        url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'
    else:
        url = ""

    response = requests.get(url)
    if response.json()['Response'] == "True":
        results = response.json()['Plot']
        return results

    else:
        return "nothing is working"


def movie_info(x):
    """
    This receives all the information of the movie with imdbId.
    :param x: imdbId of the movie
    :return: all the information of the movie
    """
    info = []
    if len(str(x)) == 7:
        url = 'https://www.omdbapi.com/?i=tt' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 6:
        url = 'https://www.omdbapi.com/?i=tt0' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 5:
        url = 'https://www.omdbapi.com/?i=tt00' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 4:
        url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'

    elif len(str(x)) == 3:
        url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'
    else:
        url = ""

    response = requests.get(url)
    if response.json()['Response'] == "True":
        results = response.json()['Plot']
        genre = response.json()['Genre']
        poster = response.json()['Poster']
        runtime = response.json()['Runtime']
        title = response.json()['Title']

        info.append((results, genre, runtime, poster, title))

    else:
        return "nothing is working"

    return info


if __name__ == '__main__':

    plot(x="")
