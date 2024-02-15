
from flask import Flask, request, jsonify
from selectorlib import Extractor
import requests
from urllib.parse import urlparse
import json

app = Flask(__name__)

# Function to read data from an external JSON file ("pp.json")
def read_json_data():
    with open("personal_product.json", "r") as json_file:
        data = json.load(json_file)
    return data

# Function to handle the "SMSSPRODUCT" scenario
def smss_product(url):
    if url == "SMSSPRODUCT":
        # Return data from the external JSON file
        return read_json_data()
    else:
        return "ERROR wrong url pattern"



def scrape(url):  
    # return url
    parsed_url = urlparse(url)
    #return parsed_url.netloc


    if url == "SMSSPRODUCT":
        return read_json_data()
    parsed_url = urlparse(url)
    if "www.flipkart.com" in parsed_url.netloc:
        e = Extractor.from_yaml_file('flipcart_selectors.yml')
    else:
        e = Extractor.from_yaml_file('amazon_selectors.yml')

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None

    # Pass the HTML of the page and create
    return e.extract(r.text)

@app.route('/scrape', methods=['GET'])
def scrape_endpoint():
    # Get the 'url' parameter from the request
    url = request.args.get('url')

    # Call the scrape function with the provided URL
    data = scrape(url)

    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to scrape the data"}), 500
    
# Route for handling the "SMSSPRODUCT" scenario
@app.route('/smss_product', methods=['GET'])
def smss_product_endpoint():
    url = request.args.get('url')
    result = smss_product(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
