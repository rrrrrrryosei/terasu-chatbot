import streamlit as st
import json
import os
from vertexai.language_models import ChatModel
import vertexai

# ✅ Streamlit Secrets から Google 認証情報を取得
if "GOOGLE_CREDENTIALS" in st.secrets:
    credentials_json = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

    # 一時的なファイルとして保存
    with open("/tmp/gcp_credentials.json", "w") as json_file:
        json.dump(credentials_json, json_file)

    # 環境変数として設定
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_credentials.json"
else:
    st.error("❌ Google Cloud の認証情報が設定されていません！")
    st.stop()

# ✅ Google Cloud のプロジェクト ID を設定
PROJECT_ID = credentials_json["project_id"]

# ✅ Vertex AI を初期化
vertexai.init(project=PROJECT_ID, location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison@001")

# ✅ AI チャットの関数
def chat_with_palm2(prompt):
    chat = chat_model.start_chat()
    response = chat.send_message(prompt)
    return response.text

# ✅ Streamlit の UI
st.set_page_config(page_title="てらすくん AIチャット", layout="wide")

# ✅ カスタム CSS
st.markdown(
    """
    <style>
    body {
        font-family: "Noto Sans JP", sans-serif;
        background-color: #F9F9F9;
    }
    .chat-container {
        max-width: 700px;
        margin: auto;
        padding: 20px;
        background: white;
        border-radius: 10px;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background: #DCF8C6;
        text-align: left;
    }
    .ai-message {
        background: #E9E9E9;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ アプリの UI 設計
st.title("てらすくん AIチャット 🤖")

user_input = st.text_input("メッセージを入力してください:")

if st.button("送信"):
    if user_input:
        response = chat_with_palm2(user_input)
        st.markdown(f'<div class="chat-bubble user-message">{user_input}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble ai-message">{response}</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠ メッセージを入力してください！")
