# actions.py

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import asyncio

class ActionPerformBackgroundTask(Action):

    def name(self) -> str:
        return "action_perform_background_task"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # 長時間の処理（バックグラウンドワーク）を非同期で実行
        result = await self.long_running_task()

        # 結果をユーザーに通知
        dispatcher.utter_message(text=f"バックグラウンドタスクの結果: {result}")

        return []

    async def long_running_task(self):
        # ここでバックグラウンドで行う処理を記述
        # 例えば、外部APIの呼び出しやデータベースの操作など
        await asyncio.sleep(5)  # 例：5秒の待機
        return "タスクが完了しました！"
