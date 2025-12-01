from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    products = response.json()  # Convert API response to Python variable

    return render_template('index.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)
