"""Request book api by book.isbn """
import requests


class ResponseError(Exception):
    """Response error"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


API_KEY = "4dc8562986mshccc0808b0cb1c09p140dedjsndf480963b592"
BASE_URL = "https://book-cover-api2.p.rapidapi.com/api/public/books/v1/cover/url"


def get_book_cover_url(isbn):
    """Get book cover by isbn"""
    if not isbn:
        return None
    querystring = {"isbn": isbn}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "book-cover-api2.p.rapidapi.com",
    }

    response = requests.get(BASE_URL, headers=headers, params=querystring, timeout=5)
    if response.status_code != 200:
        raise ResponseError(
            status_code=response.status_code, message=response.json()["message"]
        )
    book_cover_json = response.json()
    return book_cover_json["url"]
