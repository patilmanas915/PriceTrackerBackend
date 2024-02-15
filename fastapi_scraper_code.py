from fastapi import FastAPI, Query, HTTPException
from selectorlib import Extractor
import requests
from urllib.parse import urlparse
import json

app = FastAPI()

def read_json_data():
    with open("personal_product.json", "r") as json_file:
        data = json.load(json_file)
    return data

def scrape(url):
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

    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)

    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        raise HTTPException(status_code=500, detail="Failed to scrape the data")

    return e.extract(r.text)

@app.get('/scrape')
def scrape_endpoint(url: str = Query(..., description="URL of the product")):
    data = scrape(url)
    return data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
