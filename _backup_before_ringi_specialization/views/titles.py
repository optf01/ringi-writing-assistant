import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("💡 タイトル・見出し生成")
st.write("記事の内容や概要から、タイトル案・見出し構成案を複数生成します。")

with st.form("titles_form"):
    content = st.text_area("記事の内容・概要*", height=200, placeholder="記事本文、もしくは内容の概要を入力してください")
    gen_type = st.radio("生成するもの", ["タイトル案", "見出し構成案（記事の骨子）"], horizontal=True)
    num = st.slider("生成する案数", min_value=3, max_value=10, value=5)
    style = st.selectbox("テイスト", ["SEO重視（検索されやすさ重視）", "キャッチー・クリック率重視", "シンプル・端的"])
    submitted = st.form_submit_button("生成する", type="primary", use_container_width=True)

if submitted:
    if not content:
        st.warning("記事の内容・概要を入力してください。")
    else:
        prompt = (
            f"以下の記事内容をもとに、{gen_type}を{num}個、日本語で提案してください。\n"
            f"テイスト: {style}\n\n"
            f"【記事の内容・概要】\n{content}"
        )
        system_instruction = (
            "あなたはコンテンツマーケティングとSEOに精通した編集者です。"
            "与えられた記事内容とテイストに基づき、要求された数の案を番号付きの箇条書きで提示してください。"
            "タイトル案の場合は簡潔で魅力的なものを、見出し構成案の場合は導入からまとめまでの"
            "章立て（##見出し）を提案してください。余計な前置きは不要です。"
        )
        st.divider()
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.9)
        if result:
            st.session_state["titles_result"] = result
elif st.session_state.get("titles_result"):
    st.divider()
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["titles_result"])

if st.session_state.get("titles_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["titles_result"],
        file_name="titles.txt",
        mime="text/plain",
    )
