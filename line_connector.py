from typing import Any, Awaitable, Callable, Dict, List, Optional, Text
from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from sanic import Blueprint, response
from sanic.request import Request
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)

class LineOutput(OutputChannel):
    def __init__(self, access_token: Text) -> None:
        self.access_token = access_token

    async def send_text_message(self, recipient_id: Text, message: Text) -> None:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {
            "to": recipient_id,
            "messages": [{"type": "text", "text": message}]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(payload)) as resp:
                if resp.status != 200:
                    logger.error(f"Failed to send message: {await resp.text()}")

class LineInput(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "line"

    def __init__(self, channel_secret: Text, access_token: Text) -> None:
        self.channel_secret = channel_secret
        self.access_token = access_token

    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[Any]]) -> Blueprint:
        line_webhook = Blueprint("line_webhook", __name__)

        @line_webhook.route("/webhook", methods=["POST"])
        async def webhook(request: Request) -> response.HTTPResponse:
            payload = request.json
            for event in payload["events"]:
                sender_id = event["source"]["userId"]
                message_text = event["message"]["text"]
                out_channel = LineOutput(self.access_token)
                user_msg = UserMessage(message_text, out_channel, sender_id, input_channel=self.name())
                await on_new_message(user_msg)
            return response.json({"status": "ok"})
        
        return line_webhook
