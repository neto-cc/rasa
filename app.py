from flask import Flask, render_template, request, jsonify
import requests
import os  # os モジュールをインポートして、環境変数を取得

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    rasa_response = requests.post(
        "https://rasa-vt1z.onrender.com/webhook",
        json={"sender": "user", "message": user_message}
    )
    bot_response = rasa_response.json()

    if bot_response:
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        reply = "すみません、応答がありませんでした。"

    return jsonify({"response": reply})

# アプリケーションを実行する部分
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # 環境変数 PORT が指定されていればそのポートを使用、無ければ 5000 番ポート
    app.run(host="0.0.0.0", port=port, debug=True)  # 外部アクセスを許可して、指定されたポートで実行