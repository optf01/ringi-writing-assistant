import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("📄 文章要約")
st.write("長い文章を、指定した長さ・形式で要約します。")

with st.form("summarize_form"):
    text = st.text_area("要約したい文章*", height=250, placeholder="ここに要約したい文章を貼り付けてください")
    length = st.selectbox("要約の長さ", ["一言（1文）", "短め（3行程度）", "標準（5〜7行程度）", "詳細（元の半分程度）"])
    style = st.radio("形式", ["文章形式", "箇条書き"], horizontal=True)
    submitted = st.form_submit_button("要約する", type="primary", use_container_width=True)

if submitted:
    if not text:
        st.warning("要約したい文章を入力してください。")
    else:
        prompt = (
            f"以下の文章を要約してください。\n\n"
            f"【要約の長さ】{length}\n【形式】{style}\n\n"
            f"【文章】\n{text}"
        )
        system_instruction = (
            "あなたは要約のプロです。与えられた文章の要点を漏らさず、"
            "指定された長さと形式で日本語で要約してください。原文にない情報を付け加えないでください。"
        )
        st.divider()
        st.subheader("要約結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.3)
        if result:
            st.session_state["summarize_result"] = result
elif st.session_state.get("summarize_result"):
    st.divider()
    st.subheader("前回の要約結果")
    st.markdown(st.session_state["summarize_result"])

if st.session_state.get("summarize_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["summarize_result"],
        file_name="summary.txt",
        mime="text/plain",
    )
