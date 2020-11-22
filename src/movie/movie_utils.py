import requests


def estimate_img_url_exist(img_url):
    """
    This estimates the existance of the current image url. If the image url does not exist, then it returns the standard
    image url.
    :param img_url: the image url
    :return: image url
    """
    response = requests.get(img_url)
    if response.status_code == 404:
        img_url = "/img/no_location.png"

    return img_url


if __name__ == '__main__':
    estimate_img_url_exist(img_url="")
