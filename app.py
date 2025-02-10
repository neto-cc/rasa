from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    rasa_response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "user", "message": user_message}
    )
    bot_response = rasa_response.json()

    if bot_response:
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        reply = "すみません、応答がありませんでした。"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)

