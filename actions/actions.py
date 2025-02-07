<<<<<<< HEAD
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
=======
# actions.py

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionReservationTime(Action):

    def name(self) -> Text:
        return "action_reservation_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # スロット "reserv_time" の値を取得
        time = tracker.slots.get("reserv_time")  # .get()を使用して安全に取得

        if time:
            dispatcher.utter_message(text="{}に予約を完了しました！".format(time))
        else:
            dispatcher.utter_message(text="予約の時間が見つかりませんでした。")

        return []
>>>>>>> 6e28db407aa5f152179bb61e0db2e92e4e701795
