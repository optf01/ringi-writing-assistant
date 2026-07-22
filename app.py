import streamlit as st

from utils.gemini_client import extract_from_quote_pdf
from utils.ui import render_sidebar, run_generation

st.set_page_config(page_title="稟議書作成アシスタント", page_icon="🏢", layout="centered")

CUSTOM_CSS = """
<style>
:root {
    --accent: #d4af6a;
    --accent-soft: rgba(212, 175, 106, 0.35);
    --ink: #eef1f8;
    --ink-dim: #a9b3c9;
}

.stApp {
    background:
        linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px) 0 0 / 42px 42px,
        linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px) 0 0 / 42px 42px,
        radial-gradient(ellipse 900px 500px at 12% -10%, rgba(212, 175, 106, 0.18), transparent 55%),
        radial-gradient(ellipse 900px 600px at 100% 0%, rgba(88, 121, 199, 0.24), transparent 55%),
        linear-gradient(160deg, #090d19 0%, #0f1830 45%, #16233f 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1224 0%, #111b32 100%);
    border-right: 1px solid rgba(212, 175, 106, 0.15);
}

[data-testid="stSidebar"] * {
    color: var(--ink) !important;
}

.block-container {
    max-width: 760px;
    padding-top: 2.6rem;
    padding-bottom: 4rem;
}

.hero {
    position: relative;
    text-align: center;
    margin-bottom: 1.6rem;
}

.hero .seal {
    position: absolute;
    top: -6px;
    right: 4px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: 2px solid rgba(214, 92, 92, 0.55);
    color: rgba(224, 110, 110, 0.8);
    font-size: 0.68rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.04em;
    transform: rotate(10deg);
    opacity: 0.7;
}

.hero .badge {
    width: 68px;
    height: 68px;
    margin: 0 auto 1rem auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    background: radial-gradient(circle at 32% 28%, rgba(212, 175, 106, 0.38), rgba(212, 175, 106, 0.04));
    border: 1px solid rgba(212, 175, 106, 0.45);
    box-shadow: 0 0 46px rgba(212, 175, 106, 0.25);
    animation: floatIn 0.7s ease-out;
}

.hero .kicker {
    letter-spacing: 0.24em;
    font-size: 0.72rem;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}

.hero h1 {
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 0.6rem 0;
    letter-spacing: 0.01em;
}

.hero p {
    color: var(--ink-dim);
    font-size: 0.98rem;
    margin: 0;
}

.hero .divider-line {
    width: 64px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 1.3rem auto 0 auto;
}

@keyframes floatIn {
    from { opacity: 0; transform: translateY(-8px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.upload-panel {
    background: rgba(20, 28, 48, 0.55);
    border: 1px dashed rgba(212, 175, 106, 0.35);
    border-radius: 16px;
    padding: 1.3rem 1.6rem 0.6rem 1.6rem;
    margin-bottom: 1.6rem;
    animation: fadeUp 0.6s ease-out;
}

.upload-panel .upload-title {
    color: var(--accent);
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.2rem;
}

.upload-panel .upload-desc {
    color: var(--ink-dim);
    font-size: 0.85rem;
    margin-bottom: 0.8rem;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(9, 13, 26, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

[data-testid="stForm"] {
    background: rgba(20, 28, 48, 0.65);
    border: 1px solid rgba(212, 175, 106, 0.18);
    border-radius: 18px;
    padding: 2rem 2rem 1.4rem 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
    animation: fadeUp 0.7s ease-out;
}

h1, h2, h3, h4, label, p, span, .stMarkdown {
    color: var(--ink);
}

[data-testid="stForm"] label p {
    color: var(--ink) !important;
    font-weight: 500;
}

.stTextInput input, .stTextArea textarea {
    background: rgba(9, 13, 26, 0.75) !important;
    color: var(--ink) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent-soft) !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #6c7793 !important;
}

[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #e2bd7d, #c9974a) !important;
    color: #14213b !important;
    font-weight: 700;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 0 !important;
    box-shadow: 0 8px 24px rgba(201, 151, 74, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(201, 151, 74, 0.45);
}

.stButton button {
    background: rgba(212, 175, 106, 0.12) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(212, 175, 106, 0.45) !important;
    border-radius: 8px !important;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(212, 175, 106, 0.2);
}

.stDownloadButton button {
    background: rgba(212, 175, 106, 0.12) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(212, 175, 106, 0.4) !important;
    border-radius: 8px !important;
}

.result-card {
    background: rgba(20, 28, 48, 0.65);
    border: 1px solid rgba(212, 175, 106, 0.18);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-top: 1.5rem;
    animation: fadeUp 0.5s ease-out;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

model = render_sidebar()

st.markdown(
    """
    <div class="hero">
        <div class="seal">承認</div>
        <div class="badge">🏢</div>
        <div class="kicker">Ringi Document Assistant</div>
        <h1>稟議書作成アシスタント</h1>
        <p>件名・目的・予算を入力するだけで、社内提出用の稟議書の下書きを作成します。</p>
        <div class="divider-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="upload-panel">
        <div class="upload-title">📎 見積書から自動入力（任意）</div>
        <div class="upload-desc">見積書のPDFをアップロードすると、Geminiが内容を読み取り、下のフォームに自動入力します。</div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_quote = st.file_uploader("見積書（PDF）", type=["pdf"], label_visibility="collapsed")
extract_clicked = st.button(
    "📄 見積書を解析してフォームに自動入力",
    disabled=uploaded_quote is None,
    use_container_width=True,
)

if extract_clicked and uploaded_quote is not None:
    with st.spinner("見積書を解析しています..."):
        try:
            extracted = extract_from_quote_pdf(uploaded_quote.getvalue(), model)
            st.session_state["subject"] = extracted.subject
            st.session_state["background"] = extracted.background
            st.session_state["content"] = extracted.content
            st.session_state["budget"] = extracted.budget
            st.session_state["effect"] = extracted.effect
            st.session_state["schedule"] = extracted.schedule
            st.success("見積書から項目を自動入力しました。内容を確認・編集のうえ生成してください。")
        except Exception as e:
            st.error(f"見積書の解析に失敗しました: {e}")

with st.form("ringi_form"):
    subject = st.text_input("件名*", key="subject", placeholder="例: ノートPC買い替えの件")
    background = st.text_area("目的・背景*", key="background", height=100, placeholder="例: 現行PCの動作が遅く、業務効率が低下している")
    content = st.text_area("具体的な内容（申請したいこと）*", key="content", height=100, placeholder="例: 開発部の全社員のノートPCを最新モデルに買い替えたい")
    budget = st.text_input("費用・予算（任意）", key="budget", placeholder="例: 1台20万円 × 10台 = 200万円")
    effect = st.text_area("期待される効果（任意）", key="effect", height=80, placeholder="例: 作業効率の向上、故障リスクの低減")
    schedule = st.text_input("実施時期・スケジュール（任意）", key="schedule", placeholder="例: 2026年8月中の導入を希望")
    approver = st.text_input("宛先・決裁者（任意）", key="approver", placeholder="例: 部長 佐藤様")
    applicant = st.text_input("申請者名（任意）", key="applicant", placeholder="例: 開発部 田中")
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
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("生成結果")
        result = run_generation(prompt, model, system_instruction, temperature=0.4)
        st.markdown("</div>", unsafe_allow_html=True)
        if result:
            st.session_state["ringi_result"] = result
elif st.session_state.get("ringi_result"):
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("前回の生成結果")
    st.markdown(st.session_state["ringi_result"])
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("ringi_result"):
    st.download_button(
        "テキストでダウンロード",
        st.session_state["ringi_result"],
        file_name="ringisho.txt",
        mime="text/plain",
    )
