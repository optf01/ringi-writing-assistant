import streamlit as st

from utils.ui import render_sidebar

render_sidebar()

st.title("✍️ AI ライティングツール")
st.write("Gemini APIを使った、個人用のライティング支援ツールです。左のメニューから使いたい機能を選んでください。")

st.divider()

tools = [
    ("📝 ブログ記事作成", "テーマや要点を入力するだけで、構成の整ったブログ記事の下書きを生成します。"),
    ("✉️ メール返信文生成", "受信したメールと返信の要点を入力すると、トーンに合わせた返信文を作成します。"),
    ("🏢 稟議書作成", "件名や目的、予算などを入力すると、社内稟議書の下書きを作成します。"),
    ("📄 文章要約", "長い文章を、指定した長さ・形式で要約します。"),
    ("✏️ リライト・校正", "誤字脱字の校正から、文章表現やトーンの書き換えまで行います。"),
    ("💡 タイトル・見出し生成", "記事の内容から、複数のタイトル案・見出し案を生成します。"),
    ("📱 SNS投稿文生成", "伝えたい内容から、プラットフォームに合わせたSNS投稿文を作成します。"),
    ("🌐 翻訳", "日本語⇔英語などの翻訳を、トーンを指定して行います。"),
]

cols = st.columns(2)
for i, (name, desc) in enumerate(tools):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(name)
            st.caption(desc)

st.divider()
st.caption("使用するモデル（Flash / Pro）はサイドバーから切り替えられます。APIキーは .env の GEMINI_API_KEY を使用します。")
