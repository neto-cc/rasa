# from flask import Flask, request, jsonify
# import requests
# from flask_cors import CORS
# from google.cloud import firestore
# from google.oauth2 import service_account

# app = Flask(__name__)
# CORS(app)

# RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# # サービスアカウントの認証情報を設定
# cred = service_account.Credentials.from_service_account_file(
#     "C:\\Users\\TEMP.WIND.163\\AppData\\Local\\Programs\\Python\\Python310\\sotukennti-mu2-firebase-adminsdk-t5vyk-717cffc093.json"  # 認証情報ファイルのパスを指定
# )

# # Firestoreクライアントを作成
# db = firestore.Client(credentials=cred, project=cred.project_id)

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_message = data.get("message", "")

#     if not user_message:
#         return jsonify({"response": "エラー: 空のメッセージが送信されました"}), 400

#     # Firestoreからメッセージを検索
#     doc_ref = db.collection('message').document(user_message)  # ドキュメント名がユーザーのメッセージと一致すると仮定
#     doc = doc_ref.get()

#     if doc.exists:
#         response_text = doc.to_dict().get("response", "情報が見つかりませんでした。")
#     else:
#         response_text = "情報が見つかりませんでした。"

#     return jsonify({"response": response_text})

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORSを有効化（WordPressと通信するため）

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"  # Rasaのエンドポイント

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    # Rasaにメッセージを送信
    response = requests.post(RASA_URL, json={"sender": "user", "message": user_message})
    
    if response.status_code == 200:
        messages = response.json()
        bot_response = messages[0].get("text", "エラー: 応答がありません") if messages else "エラー: 応答がありません"
    else:
        bot_response = "エラー: Rasaと接続できません"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)