import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("✉️ メール返信文生成")
st.write("受信したメールと返信したい内容を入力すると、トーンに合わせた返信文を作成します。")

with st.form("email_form"):
    original = st.text_area("受信したメール本文*", height=180, placeholder="返信元のメール本文を貼り付けてください")
    intent = st.text_area("返信の要点・伝えたいこと*", height=100, placeholder="例: 提案は承諾するが、納期を1週間伸ばしてほしい")
    tone = st.selectbox("トーン", ["丁寧・フォーマル", "ビジネスカジュアル", "親しみやすい", "謝罪・お詫び"])
    sender_name = st.text_input("差出人名（署名に使用、任意）", placeholder="例: 山田太郎")
    submitted = st.form_submit_button("返信文を生成", type="primary", use_container_width=True)

if submitted:
    if not original or not intent:
        st.warning("受信したメール本文と、返信の要点を入力してください。")
    else:
        prompt_parts = [
            f"【受信したメール本文】\n{original}",
            f"【返信で伝えたい要点】\n{intent}",
            f"【トーン】{tone}",
        ]
        if sender_name:
            prompt_parts.append(f"【差出人名】{sender_name}")
        prompt = "以下の情報をもとに、返信メールの文面を作成してください。\n\n" + "\n\n".join(prompt_parts)

        system_instruction = (
            "あなたは日本語ビジネスメール作成のプロです。受信メールの文脈と返信の要点を踏まえ、"
            "指定されたトーンに合った自然な返信メール文を作成してください。"
            "宛名・書き出しの挨拶・本文・結びの挨拶・署名を含む、そのまま送信できる完成形のメール文にしてください。"
            "差出人名が指定されない場合は署名部分を「（お名前）」としてください。"
        )
        st.divider()
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.6)
        if result:
            st.session_state["email_result"] = result
elif st.session_state.get("email_result"):
    st.divider()
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["email_result"])

if st.session_state.get("email_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["email_result"],
        file_name="email_reply.txt",
        mime="text/plain",
    )
