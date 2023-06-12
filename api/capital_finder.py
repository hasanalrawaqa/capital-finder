import requests
from urllib import parse
from http.server import BaseHTTPRequestHandler

def handle_request(request):
    # Parse the query parameters from the request
    query = request["query"]

    # Check if the 'country' parameter is present
    if "country" in query:
        country = parse.quote(query["country"])
        # Make a GET request to the REST Countries API to get the capital
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        data = response.json()

        # Extract the capital from the API response
        capital = data[0]["capital"]["name"]

        # Generate the response string
        response_string = f"The capital of {query['country']} is {capital}."
    # Check if the 'capital' parameter is present
    elif "capital" in query:
        capital = parse.quote(query["capital"])
        # Make a GET request to the REST Countries API to get the country
        response = requests.get(f"https://restcountries.com/v3.1/capital/{capital}")
        data = response.json()

        # Extract the country name from the API response
        country = data[0]["name"]["official"]

        # Generate the response string
        response_string = f"{capital} is the capital of {country}."
    else:
        # Invalid request, return an error message
        response_string = "Invalid request. Please provide either the 'country' or 'capital' parameter."

    return response_string

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the request URL
        url_parts = parse.urlparse(self.path)
        query = parse.parse_qs(url_parts.query)

        # Prepare the request object
        request = {
            "query": query
        }

        # Handle the request and get the response string
        response_string = handle_request(request)

        # Send the HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_string.encode())
