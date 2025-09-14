from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator
from langdetect import detect
import json

# Load FAQ Data
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

translator = Translator()
app = Flask(__name__)

def get_answer(query):
    query = query.lower()
    for key in faq_data:
        if key in query:
            return faq_data[key]
    return "Sorry, please contact admin office."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.form.get("Body")
    lang = detect(incoming_msg)
    query_en = translator.translate(incoming_msg, dest="en").text
    answer_en = get_answer(query_en)
    final_answer = translator.translate(answer_en, dest=lang).text

    resp = MessagingResponse()
    resp.message(final_answer)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
