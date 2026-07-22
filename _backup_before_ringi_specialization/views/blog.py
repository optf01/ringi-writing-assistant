import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("📝 ブログ記事作成")
st.write("テーマや条件を入力すると、構成の整ったブログ記事の下書きを生成します。")

with st.form("blog_form"):
    theme = st.text_input("テーマ・キーワード*", placeholder="例: 在宅勤務の生産性を上げる方法")
    audience = st.text_input("想定読者", placeholder="例: リモートワークを始めたばかりの会社員")
    length = st.select_slider(
        "文字数目安",
        options=["短め（500字）", "標準（1000字）", "長め（2000字）", "詳細（3000字以上）"],
        value="標準（1000字）",
    )
    tone = st.selectbox("トーン", ["フォーマル", "カジュアル", "専門的", "親しみやすい"])
    outline = st.text_area("構成の希望（任意）", placeholder="例: 導入 → 3つのポイント → まとめ、の構成にしたい")
    extra = st.text_area("追加の指示（任意）", placeholder="例: 具体例を2つ入れてほしい / SEOを意識してほしい")
    submitted = st.form_submit_button("記事を生成", type="primary", use_container_width=True)

if submitted:
    if not theme:
        st.warning("テーマ・キーワードを入力してください。")
    else:
        prompt_parts = [f"テーマ: {theme}", f"文字数目安: {length}", f"トーン: {tone}"]
        if audience:
            prompt_parts.append(f"想定読者: {audience}")
        if outline:
            prompt_parts.append(f"構成の希望: {outline}")
        if extra:
            prompt_parts.append(f"追加の指示: {extra}")
        prompt = "以下の条件でブログ記事を作成してください。\n\n" + "\n".join(prompt_parts)

        system_instruction = (
            "あなたはプロのブログライターです。与えられた条件をもとに、"
            "読みやすく構成の整ったブログ記事の下書きを日本語のMarkdown形式で作成してください。"
            "見出し(##、###)を適切に使い、導入・本文・まとめの流れを意識してください。"
        )
        st.divider()
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.85)
        if result:
            st.session_state["blog_result"] = result
elif st.session_state.get("blog_result"):
    st.divider()
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["blog_result"])

if st.session_state.get("blog_result"):
    st.download_button(
        "Markdownでダウンロード",
        st.session_state["blog_result"],
        file_name="blog_article.md",
        mime="text/markdown",
    )
