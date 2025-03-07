from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    logger.info("ホームページにアクセスされました")
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    rasa_url = f"http://localhost:{os.getenv('RASA_PORT', '5005')}/webhooks/rest/webhook"

    logger.info(f"ユーザーのメッセージ: {user_message}")
    
    try:
        rasa_response = requests.post(rasa_url, json={"sender": "user", "message": user_message}, timeout=5)
        rasa_response.raise_for_status()  # HTTPエラーがある場合は例外を発生
        bot_response = rasa_response.json()

        if bot_response:
            reply = bot_response[0].get("text", "すみません、理解できませんでした。")
        else:
            reply = "すみません、応答がありませんでした。"

    except requests.exceptions.RequestException as e:
        logger.error(f"Rasa へのリクエストエラー: {e}")
        reply = "エラーが発生しました。しばらくしてからもう一度お試しください。"

    logger.info(f"Rasa の応答: {reply}")

    return jsonify({"response": reply})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render の環境変数 PORT に対応
    logger.info(f"サーバーを起動: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)