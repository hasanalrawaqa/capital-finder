from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response_string = ""
        url_path = self.path
        url_component = parse.urlsplit(url_path)
        query_var = parse.parse_qs(url_component.query)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        if 'country' in query_var:
            country = query_var['country'][0]
            url_API = f"https://restcountries.com/v3.1/name/{country}"
            result_of_request = requests.get(url_API)
            json_data = result_of_request.json()

            for data in json_data:
                capital = data["capital"][0]
                response_string = f"The capital of {country} is {capital}."

        elif "capital" in query_var:
            capital = query_var.get("capital")
            url_API = f"https://restcountries.com/v3.1/capital/{capital}"
            result_of_request = requests.get(url_API)
            json_data = result_of_request.json()

            for data in json_data:
                country = data["name"]["common"]
                response_string = f"{capital} is the capital of {country}."

        self.wfile.write(response_string.encode())

