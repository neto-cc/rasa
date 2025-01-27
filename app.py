from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # ユーザーからのメッセージを取得
    user_message = request.json.get("message")
    
    # Render で動作する Rasa サーバーの URL
    rasa_url = os.getenv("RASA_URL", "https://rasa-vt1z.onrender.com/webhook")

    # Rasa にメッセージを送信
    rasa_response = requests.post(
        rasa_url,
        json={"sender": "user", "message": user_message}
    )
    bot_response = rasa_response.json()

    # Rasa の応答を確認
    if bot_response:
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        reply = "すみません、応答がありませんでした。"

    return jsonify({"response": reply})

if __name__ == "__main__":
    # Render のポート設定を確認して、動的に設定
    port = int(os.getenv("PORT", 10000))  # デフォルトで 5000 番ポート
    app.run(host="0.0.0.0", port=port, debug=True)