"""Request book api by book.isbn """
import requests

url = "https://book-cover-api2.p.rapidapi.com/api/public/books/v1/cover/url"

querystring = {"isbn": "9781526606198"}

headers = {
    "X-RapidAPI-Key": "4dc8562986mshccc0808b0cb1c09p140dedjsndf480963b592",
    "X-RapidAPI-Host": "book-cover-api2.p.rapidapi.com",
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
