import streamlit as st
from vertexai.language_models import ChatModel

# Streamlit のページ設定
st.set_page_config(page_title="てらすくん AIチャット", layout="wide")

# Google Cloud の設定
PROJECT_ID = "your-google-project-id"  # ここを自分のプロジェクト ID に変更

# Vertex AI のモデルをロード
chat_model = ChatModel.from_pretrained("chat-bison@001")

# AI チャットの関数
def chat_with_palm2(prompt):
    chat = chat_model.start_chat()
    response = chat.send_message(prompt)
    return response.text

# カスタム CSS
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

# アプリのUI
st.title("てらすくん AIチャット")

user_input = st.text_input("メッセージを入力してください:")

if st.button("送信"):
    response = chat_with_palm2(user_input)
    st.markdown(f'<div class="chat-bubble user-message">{user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble ai-message">{response}</div>', unsafe_allow_html=True)
