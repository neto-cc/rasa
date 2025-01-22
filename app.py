from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# RasaサーバーのURL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "メッセージが空です"}), 400

    payload = {"sender": "user", "message": user_input}
    try:
        response = requests.post(RASA_SERVER_URL, json=payload)
        response.raise_for_status()
        rasa_response = response.json()

        if rasa_response:
            return jsonify({"response": rasa_response[0].get("text", "応答がありません")})
        else:
            return jsonify({"response": "Rasaからの応答がありません"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

