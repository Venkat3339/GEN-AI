from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Get Hugging Face API token from environment
HF_TOKEN = 'Token value'

# Initialize the client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

@app.route("/")
def home():
    return render_template("index.html")

@app.before_request
def ignore_chrome_devtools():
    if request.path.startswith("/.well-known/appspecific"):
        return "", 404


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_input = data.get("prompt", "")

    try:
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Thinking:novita",
            messages=[{"role": "user", "content": user_input}],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
