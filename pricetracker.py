from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def scrape_snapdeal(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_name = soup.find('h1', class_='pdp-e-i-head')
            price_element = soup.find('span', class_='payBlkBig')

            if price_element:
                price = price_element.get_text(strip=True)
                return {"product_name": product_name.text.strip(), "product_price": price}

        return {"error": "Product is currently unavailable. Please try again later."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    


def scrape_flipkart(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_name = soup.find('span', class_='B_NuCI')
            price_element = soup.find('div', class_='_30jeq3 _16Jk6d')

            if price_element:
                price = price_element.get_text(strip=True)
                return {"product_name": product_name.text.strip(), "product_price": price}

        return {"error": "Product is currently unavailable. Please try again later."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    


def scrape_amazon(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_name = soup.find('span', class_='a-size-large product-title-word-break')
            price_element = soup.find('span', class_='a-price-whole')
            symbol = soup.find('span', class_='a-price-symbol')

            if price_element:
                price = price_element.get_text(strip=True)
                return {
                    "product_name": product_name.text.strip(),
                    "product_price": symbol.text.strip() + price
                }
            else:
                return {"error": "Product not found in Amazon"}

        return {"error": "Product is currently unavailable. Please try again later."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}



@app.route('/scrape', methods=['POST'])
def handle_snapdeal_scraping():
    data = request.get_json()

    url_snap = data.get('snapdeal_url', '')
    result_snap = scrape_snapdeal(url_snap)

    
    url_flip = data.get('flipkart_url', '')
    result_flip = scrape_flipkart(url_flip)

    url_amaz = data.get('amazon_url', '')
    result_amaz = scrape_amazon(url_amaz)

    ret = {"snap": result_snap,"flip": result_flip,"amaz": result_amaz}
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True, port=5003, threaded=True)
