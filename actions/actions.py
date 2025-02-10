from typing import Any, Text, Dict, List
import firebase_admin
from firebase_admin import credentials, firestore

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# Firebase Firestore の初期化
cred = credentials.Certificate("F:/line/etc/secrets/firebase-key.json")  # サービスアカウントキーのパスを指定
firebase_admin.initialize_app(cred)
db = firestore.client()

class ActionReservationTime(Action):

    def name(self) -> Text:
        return "action_reservation_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # スロット "reserv_time" の値を取得
        time = tracker.get_slot("reserv_time")  # 安全に取得
        user_id = tracker.sender_id  # ユーザーIDを取得

        if time:
            try:
                # Firestore に予約情報を保存
                db.collection("reservations").document(user_id).set({
                    "user_id": user_id,
                    "reservation_time": time
                })

                dispatcher.utter_message(text=f"{time} に予約を完了しました！")
            except Exception as e:
                dispatcher.utter_message(text="予約の保存中にエラーが発生しました。もう一度お試しください。")
                print(f"Firestore 保存エラー: {e}")
        else:
            dispatcher.utter_message(text="予約の時間が見つかりませんでした。")

        return []
