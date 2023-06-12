import http.client
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if 'country' in query_params:
            country = query_params['country'][0]
            capital = get_capital_by_country(country)
            response = f"The capital of {country} is {capital}."
        elif 'capital' in query_params:
            capital = query_params['capital'][0]
            country = get_country_by_capital(capital)
            response = f"{capital} is the capital of {country}."
        else:
            response = "Invalid request."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
        return


def get_capital_by_country(country):
    conn = http.client.HTTPSConnection("restcountries.com")
    conn.request("GET", "/v3.1/name/" + country)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    country_data = json.loads(data)[0]
    capital = country_data["capital"][0]
    return capital


def get_country_by_capital(capital):
    conn = http.client.HTTPSConnection("restcountries.com")
    conn.request("GET", "/v3.1/capital/" + capital)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    countries_data = json.loads(data)
    country = countries_data[0]["name"]["official"]
    return country