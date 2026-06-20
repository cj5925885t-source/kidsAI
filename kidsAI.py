import streamlit as st
import os
from google import genai
from google.genai import types

# ==========================================
# 1. 初期設定（公開用の安全な書き方）
# ==========================================
# 💡 サーバーの設定画面（Secrets）から鍵を安全に読み込みます
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# クライアントの初期化
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="サイキッズAI", page_icon="✨", layout="centered")

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 💡【重要】このファイル（kidsAI.py）があるフォルダのパスを自動で取得します
current_dir = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 2. 画面デザイン（イラスト配置エリア）
# ==========================================

# 画像の絶対パス（確実な住所）を作成
logo_path = os.path.join(current_dir, "logo.png")
sensei_path = os.path.join(current_dir, "sensei.png")

# 💡 画像配置①：一番上のタイトルロゴ
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)
else:
    st.title("✨ サイキッズAI 先生")
    st.markdown("##### こどもの かんがえるちからを そだてる AIだよ！")
    st.warning(f"※ここにロゴを出したい場合、画像名を「logo.png」にして同じフォルダに入れてね")

st.divider()

# 先生の操作パネル
with st.container(border=True):
    st.markdown("👩‍🏫 **せんせいがそうさしてね**")
    question = st.text_input(
        label="問題を入力",
        value=""
    )

st.write("") 

# 💡 画像配置②：キャラクターと吹き出し
col_img, col_text = st.columns([1, 3])

with col_img:
    if os.path.exists(sensei_path):
        st.image(sensei_path, use_container_width=True)
    else:
        st.write("👩‍🏫\n(先生の画像)")

with col_text:
    st.markdown(f"### 🤔 もんだい\n**「{question}」**")

# マイクボタン
col_space, col_mic, col_space2 = st.columns([1, 2, 1])
with col_mic:
    st.write("👇 マイクのボタンをおしてね")
    audio_value = st.audio_input("こたえをおはなししてね")

st.divider()

# ==========================================
# 3. 実行部分
# ==========================================
if audio_value:
    st.toast("おへんじがとどいたよ！", icon="✅")
    
    with st.chat_message("user", avatar="👦"):
        st.write("（おはなしした こたえ）")
        st.audio(audio_value)
    
    with st.spinner("AIせんせいがかんがえているよ..."):
        try:
            audio_bytes = audio_value.getvalue()
            audio_part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
            
            prompt = f"""
            あなたは正しい答えのない質問に対しての子供の回答を採点する先生です。子供だからといってなんでも肯定するのではなくある程度の根拠のある意見かどうかや論理的かを判断してください。不十分であると感じたら深掘りしたり、追加で質問をしたりしてください。
            質問：『{question}』
            添付された音声データ（子どもの回答）をよく聴いて、評価を５段階評価の星の絵文字で表し、講評を全て必ずひらがなで返信してください。
            例えば
            ☆★★★★　ほし◯つ　のように必ず表示してその下に改行して講評を書いてください
            子供の名前は呼ばなくて良いです。
            星四つ以上の場合にこの問題が合格である旨を伝えてください
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt, audio_part]
            )
            
            with st.chat_message("assistant", avatar="👩‍🏫"):
                st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
