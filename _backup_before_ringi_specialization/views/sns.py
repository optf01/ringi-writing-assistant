import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("📱 SNS投稿文生成")
st.write("伝えたい内容から、プラットフォームに合わせたSNS投稿文の案を作成します。")

with st.form("sns_form"):
    content = st.text_area("伝えたい内容*", height=150, placeholder="例: 新商品のカフェラテを発売しました。期間限定で20%オフです。")
    platform = st.selectbox("プラットフォーム", ["X（旧Twitter）", "Instagram", "Facebook", "LinkedIn"])
    tone = st.selectbox("トーン", ["カジュアル・親しみやすい", "フォーマル・ビジネス", "ワクワクする・勢いのある", "落ち着いた・丁寧"])
    use_hashtags = st.checkbox("ハッシュタグを付ける", value=True)
    use_emoji = st.checkbox("絵文字を使う", value=True)
    num = st.slider("生成する案数", min_value=1, max_value=5, value=3)
    submitted = st.form_submit_button("投稿文を生成", type="primary", use_container_width=True)

if submitted:
    if not content:
        st.warning("伝えたい内容を入力してください。")
    else:
        char_limits = {
            "X（旧Twitter）": "全角140文字以内",
            "Instagram": "2200文字以内（ただし読みやすく簡潔に）",
            "Facebook": "文字数制限は緩いが簡潔に",
            "LinkedIn": "ビジネス向けに簡潔に、長すぎない範囲で",
        }
        prompt = (
            f"以下の内容で、{platform}向けの投稿文を{num}案、日本語で作成してください。\n"
            f"トーン: {tone}\n"
            f"文字数の目安: {char_limits[platform]}\n"
            f"ハッシュタグ: {'付ける' if use_hashtags else '付けない'}\n"
            f"絵文字: {'使う' if use_emoji else '使わない'}\n\n"
            f"【伝えたい内容】\n{content}"
        )
        system_instruction = (
            "あなたはSNSマーケティングのプロです。指定されたプラットフォームの特性・文字数感・"
            "文化に合わせた投稿文を、指定された案数だけ提案してください。各案は番号を振り、区切って提示してください。"
        )
        st.divider()
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.9)
        if result:
            st.session_state["sns_result"] = result
elif st.session_state.get("sns_result"):
    st.divider()
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["sns_result"])

if st.session_state.get("sns_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["sns_result"],
        file_name="sns_posts.txt",
        mime="text/plain",
    )
