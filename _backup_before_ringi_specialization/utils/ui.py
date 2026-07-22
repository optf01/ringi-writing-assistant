import streamlit as st

from utils.gemini_client import generate_stream, has_api_key

MODELS = {
    "Gemini Flash（高速・低コスト）": "gemini-flash-latest",
    "Gemini Pro（高品質・低速）": "gemini-pro-latest",
}


def render_sidebar() -> str:
    """サイドバーにモデル選択UIを表示し、選択中のモデルIDを返す。"""
    st.sidebar.title("⚙️ 設定")

    if not has_api_key():
        st.sidebar.error("GEMINI_API_KEY が未設定です。.env を確認してください。")

    if "model_label" not in st.session_state:
        st.session_state.model_label = list(MODELS.keys())[0]

    st.session_state.model_label = st.sidebar.selectbox(
        "使用するモデル",
        list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.model_label),
    )
    st.sidebar.caption(
        "Flash: 日常的な用途に十分な速度・品質\n\nPro: より高品質だが低速・高コスト"
    )
    return MODELS[st.session_state.model_label]


def run_generation(prompt: str, model: str, system_instruction: str, temperature: float = 0.7):
    """生成を実行し、ストリーミング表示した上で結果テキストを返す。APIキー未設定時はNoneを返す。"""
    if not has_api_key():
        st.error("GEMINI_API_KEY が設定されていません。プロジェクト直下に .env を作成し、"
                  "GEMINI_API_KEY=あなたのAPIキー を記載してください。")
        return None

    try:
        result = st.write_stream(
            generate_stream(prompt, model, system_instruction=system_instruction, temperature=temperature)
        )
    except Exception as e:
        st.error(f"生成中にエラーが発生しました: {e}")
        return None

    return result
