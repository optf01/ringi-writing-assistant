import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("🌐 翻訳")
st.write("文章を指定した言語・トーンに翻訳します。")

LANGUAGES = ["日本語", "英語", "中国語（簡体字）", "韓国語", "スペイン語", "フランス語"]

with st.form("translate_form"):
    text = st.text_area("翻訳したい文章*", height=200, placeholder="翻訳したい文章を入力してください")
    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("翻訳元の言語", ["自動判定"] + LANGUAGES)
    with col2:
        tgt_lang = st.selectbox("翻訳先の言語", LANGUAGES, index=1)
    tone = st.selectbox("トーン", ["標準", "フォーマル・ビジネス", "カジュアル・親しみやすい"])
    submitted = st.form_submit_button("翻訳する", type="primary", use_container_width=True)

if submitted:
    if not text:
        st.warning("翻訳したい文章を入力してください。")
    else:
        prompt = (
            f"以下の文章を{tgt_lang}に翻訳してください。\n"
            f"翻訳元の言語: {src_lang}\n"
            f"トーン: {tone}\n\n"
            f"【原文】\n{text}"
        )
        system_instruction = (
            "あなたはプロの翻訳者です。文脈を踏まえ、指定されたトーンで自然な訳文を作成してください。"
            "訳文のみを出力し、原文や補足説明は含めないでください。"
        )
        st.divider()
        st.subheader("翻訳結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.3)
        if result:
            st.session_state["translate_result"] = result
elif st.session_state.get("translate_result"):
    st.divider()
    st.subheader("前回の翻訳結果")
    st.markdown(st.session_state["translate_result"])

if st.session_state.get("translate_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["translate_result"],
        file_name="translation.txt",
        mime="text/plain",
    )
