import spacy
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# spaCyの軽量モデルを読み込む
nlp = spacy.load("en_core_web_sm")

# distilBERTのトークナイザーとモデルを読み込む
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

class ActionProcessText(Action):
    def name(self) -> str:
        return "action_process_text"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        
        # spaCyを使用してエンティティを抽出
        doc = nlp(user_message)
        entities = [ent.text for ent in doc.ents]
        
        # distilBERTを使用してテキスト分類
        inputs = tokenizer(user_message, return_tensors='pt')
        with torch.no_grad():
            logits = model(**inputs).logits
        category = torch.argmax(logits, dim=-1).item()

        # エンティティと分類結果をスロットに保存
        return [SlotSet("extracted_entities", entities), SlotSet("message_category", category)]
