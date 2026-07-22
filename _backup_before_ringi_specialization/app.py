import streamlit as st

st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")

home = st.Page("views/home.py", title="ホーム", icon="🏠", default=True)
blog = st.Page("views/blog.py", title="ブログ記事作成", icon="📝")
email_reply = st.Page("views/email_reply.py", title="メール返信文生成", icon="✉️")
ringi = st.Page("views/ringi.py", title="稟議書作成", icon="🏢")
summarize = st.Page("views/summarize.py", title="文章要約", icon="📄")
rewrite = st.Page("views/rewrite.py", title="リライト・校正", icon="✏️")
titles = st.Page("views/titles.py", title="タイトル・見出し生成", icon="💡")
sns = st.Page("views/sns.py", title="SNS投稿文生成", icon="📱")
translate = st.Page("views/translate.py", title="翻訳", icon="🌐")

pg = st.navigation(
    {
        "メニュー": [home],
        "文章を作る": [blog, email_reply, ringi],
        "文章を整える": [summarize, rewrite, titles],
        "その他": [sns, translate],
    }
)

pg.run()
