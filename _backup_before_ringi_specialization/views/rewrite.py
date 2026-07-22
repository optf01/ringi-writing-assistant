import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("✏️ リライト・校正")
st.write("誤字脱字の校正から、文章表現やトーンの書き換えまで行います。")

with st.form("rewrite_form"):
    text = st.text_area("元の文章*", height=250, placeholder="校正・リライトしたい文章を貼り付けてください")
    mode = st.selectbox(
        "モード",
        [
            "校正のみ（誤字脱字・表現の誤りを修正、意味は変えない）",
            "文章表現をリライト（より読みやすく自然な文章に）",
            "トーン変更",
        ],
    )
    tone = None
    if mode == "トーン変更":
        tone = st.selectbox("変更後のトーン", ["フォーマル", "カジュアル", "丁寧", "簡潔", "説得力のある"])
    show_diff = st.checkbox("主な変更点の説明も表示する", value=True)
    submitted = st.form_submit_button("実行する", type="primary", use_container_width=True)

if submitted:
    if not text:
        st.warning("元の文章を入力してください。")
    else:
        prompt_parts = [f"【モード】{mode}"]
        if tone:
            prompt_parts.append(f"【変更後のトーン】{tone}")
        prompt_parts.append(f"【元の文章】\n{text}")
        prompt = "以下の文章を指定されたモードで修正してください。\n\n" + "\n".join(prompt_parts)

        instruction_extra = (
            "修正後の文章の後に「---」で区切り、主な変更点を箇条書きで簡潔に説明してください。"
            if show_diff
            else "修正後の文章のみを出力し、余計な説明は含めないでください。"
        )
        system_instruction = (
            "あなたは日本語の文章校正・リライトのプロです。指定されたモードに従って文章を修正してください。"
            "校正のみの場合は文意を変えず誤りのみ直し、リライトの場合はより自然で読みやすい表現に書き換え、"
            "トーン変更の場合は指定されたトーンに合わせて言い回しを調整してください。" + instruction_extra
        )
        st.divider()
        st.subheader("結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.4)
        if result:
            st.session_state["rewrite_result"] = result
elif st.session_state.get("rewrite_result"):
    st.divider()
    st.subheader("前回の結果")
    st.markdown(st.session_state["rewrite_result"])

if st.session_state.get("rewrite_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["rewrite_result"],
        file_name="rewrite_result.txt",
        mime="text/plain",
    )
