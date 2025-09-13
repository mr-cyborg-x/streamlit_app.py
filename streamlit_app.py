import streamlit as st
from googletrans import Translator
from langdetect import detect
import json
import datetime

# ----------------------------
# 1. Load FAQ Data
# ----------------------------
faq_data = {
    "fee deadline": "The last date for paying semester fees is 30th September.",
    "scholarship form": "Scholarship forms are available in the admin office or website.",
    "timetable": "Latest timetable is available on the college website under Academics section.",
    "hostel": "For hostel related queries, please contact the hostel office."
}

# ----------------------------
# 2. Initialize translator
# ----------------------------
translator = Translator()

# ----------------------------
# 3. Helper functions
# ----------------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    return translator.translate(text, dest="en").text

def translate_back(text, lang):
    if lang == "en":
        return text
    return translator.translate(text, dest=lang).text

def get_answer(user_input):
    user_input = user_input.lower()
    for key in faq_data:
        if key in user_input:
            return faq_data[key]
    return "Sorry, I don't know that. Please contact admin office."

def log_conversation(user, bot):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user}\nBOT: {bot}\n\n")

# ----------------------------
# 4. Streamlit UI
# ----------------------------
st.set_page_config(page_title="College Multilingual Chatbot", page_icon="🎓")
st.title("🎓 College Multilingual Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if user_input := st.chat_input("Type your message..."):
    # Detect language
    lang = detect_language(user_input)

    # Translate to English
    query_en = translate_to_english(user_input)

    # Get Answer
    answer_en = get_answer(query_en)

    # Translate back to user lang
    final_answer = translate_back(answer_en, lang)

    # Store in session + logs
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    log_conversation(user_input, final_answer)

    # Display
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(final_answer)

# Download Logs
with open("chat_logs.txt", "r", encoding="utf-8") as f:
    logs = f.read()
st.download_button("📥 Download Chat Logs", logs, file_name="chat_logs.txt")
