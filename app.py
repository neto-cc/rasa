from flask import Flask, render_template, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase Firestoreの初期化
cred = credentials.Certificate("F:/line/etc/secrets/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Rasa とのやり取り
    rasa_response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "user", "message": user_message}
    )
    bot_response = rasa_response.json()

    if bot_response:
        reply = bot_response[0].get("text", "すみません、理解できませんでした。")
    else:
        reply = "すみません、応答がありませんでした。"

    # Firestoreから予約データを取得する（例）
    user_id = "user_example_id"  # 実際にはユーザーIDをトラッキングから取得
    reservation_ref = db.collection("reservations").document(user_id)
    reservation_doc = reservation_ref.get()

    if reservation_doc.exists:
        reservation_time = reservation_doc.to_dict().get("reservation_time", "未設定")
        reply += f"\nあなたの予約時間は: {reservation_time}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)

