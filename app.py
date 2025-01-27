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
    
    # Rasa サーバーの webhook URL を指定します
    rasa_response = requests.post(
        "http://0.0.0.0:5005/webhook",  # Render 上の Rasa の URL
        json={"sender": "user", "message": user_message}
    )
    
    # Rasa からの応答を取得
    bot_response = rasa_response.json()

    if bot_response:
        # Rasa から返ってきた応答の "text" を取得
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        # Rasa の応答がない場合のデフォルトメッセージ
        reply = "すみません、応答がありませんでした。"

    # チャットの応答を JSON 形式で返す
    return jsonify({"response": reply})

# アプリケーションを実行する部分
if __name__ == "__main__":
    # 環境変数 PORT が指定されていればそのポートを使用、無ければ 5000 番ポートを使用
    port = int(os.getenv("PORT", 5005))
    
    # Flask アプリケーションを実行
    app.run(host="0.0.0.0", port=port, debug=True)  # 外部アクセスを許可して、指定されたポートで実行