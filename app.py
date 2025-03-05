from flask import Flask, render_template, request, jsonify
import requests
import os  # 環境変数を取得するために追加

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    rasa_url = f"http://localhost:{os.getenv('RASA_PORT', '5005')}/webhooks/rest/webhook"  # Rasaのポートも環境変数で設定可能
    rasa_response = requests.post(rasa_url, json={"sender": "user", "message": user_message})

    bot_response = rasa_response.json()

    if bot_response:
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        reply = "すみません、応答がありませんでした。"

    return jsonify({"response": reply})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))  # 環境変数PORTが未設定ならデフォルト3001
    app.run(host="0.0.0.0", port=port, debug=True)