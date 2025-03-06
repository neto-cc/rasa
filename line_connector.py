from rasa.core.channels.channel import InputChannel
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage
from sanic import Blueprint, response

class LineInput(InputChannel):
    def __init__(self, channel_secret: str, channel_access_token: str):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)

    def blueprint(self, on_new_message):
        line_webhook = Blueprint('line_webhook', __name__)

        @line_webhook.route('/webhook', methods=['POST'])
        async def receive_message(request):
            body = request.json
            signature = request.headers['X-Line-Signature']
            self.handler.handle(body, signature)
            return response.json({"status": "success"})

        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            user_message = event.message.text
            on_new_message(user_message)

        return line_webhook