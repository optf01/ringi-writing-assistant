import streamlit as st

from utils.ui import render_sidebar, run_generation

model = render_sidebar()

st.title("🏢 稟議書作成")
st.write("件名や目的、予算などを入力すると、社内稟議書の下書きを作成します。")

with st.form("ringi_form"):
    subject = st.text_input("件名*", placeholder="例: ノートPC買い替えの件")
    background = st.text_area("目的・背景*", height=100, placeholder="例: 現行PCの動作が遅く、業務効率が低下している")
    content = st.text_area("具体的な内容（申請したいこと）*", height=100, placeholder="例: 開発部の全社員のノートPCを最新モデルに買い替えたい")
    budget = st.text_input("費用・予算（任意）", placeholder="例: 1台20万円 × 10台 = 200万円")
    effect = st.text_area("期待される効果（任意）", height=80, placeholder="例: 作業効率の向上、故障リスクの低減")
    schedule = st.text_input("実施時期・スケジュール（任意）", placeholder="例: 2026年8月中の導入を希望")
    approver = st.text_input("宛先・決裁者（任意）", placeholder="例: 部長 佐藤様")
    applicant = st.text_input("申請者名（任意）", placeholder="例: 開発部 田中")
    submitted = st.form_submit_button("稟議書を生成", type="primary", use_container_width=True)

if submitted:
    if not subject or not background or not content:
        st.warning("件名・目的、背景・具体的な内容は必須項目です。")
    else:
        prompt_parts = [
            f"件名: {subject}",
            f"目的・背景: {background}",
            f"具体的な内容: {content}",
        ]
        if budget:
            prompt_parts.append(f"費用・予算: {budget}")
        if effect:
            prompt_parts.append(f"期待される効果: {effect}")
        if schedule:
            prompt_parts.append(f"実施時期・スケジュール: {schedule}")
        if approver:
            prompt_parts.append(f"宛先・決裁者: {approver}")
        if applicant:
            prompt_parts.append(f"申請者名: {applicant}")
        prompt = "以下の情報をもとに、社内稟議書を作成してください。\n\n" + "\n".join(prompt_parts)

        system_instruction = (
            "あなたは日本企業の総務・経理部門で稟議書作成を数多く手がけてきたプロです。"
            "与えられた情報をもとに、社内で正式に提出できる稟議書の下書きを日本語で作成してください。"
            "件名、日付（記入欄「〇年〇月〇日」のままでよい）、申請者、宛先、目的・背景、"
            "申請内容、費用、期待される効果、実施スケジュールといった一般的な稟議書の項目立てで、"
            "簡潔かつ論理的な文章にしてください。未入力の項目は無理に埋めず、"
            "適宜「（ご記入ください）」として空欄にしてください。"
        )
        st.divider()
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.4)
        if result:
            st.session_state["ringi_result"] = result
elif st.session_state.get("ringi_result"):
    st.divider()
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["ringi_result"])

if st.session_state.get("ringi_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["ringi_result"],
        file_name="ringisho.txt",
        mime="text/plain",
    )
