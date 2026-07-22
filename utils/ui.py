import os

import streamlit as st

from utils.gemini_client import generate_stream, has_api_key

MODELS = {
    "Gemini Flash（高速・低コスト）": "gemini-flash-latest",
    "Gemini Pro（高品質・低速）": "gemini-pro-latest",
}


def render_sidebar() -> str:
    """サイドバーにAPIキー入力・モデル選択UIを表示し、選択中のモデルIDを返す。"""
    st.sidebar.title("⚙️ 設定")

    if "gemini_api_key_override" not in st.session_state:
        st.session_state.gemini_api_key_override = ""

    st.session_state.gemini_api_key_override = st.sidebar.text_input(
        "Gemini APIキー",
        value=st.session_state.gemini_api_key_override,
        type="password",
        placeholder=".envの値を使用中" if os.getenv("GEMINI_API_KEY") else "APIキーを入力してください",
        help="ここで入力したキーはこのブラウザセッション内でのみ使用され、保存されません。"
             "空欄の場合は .env の GEMINI_API_KEY を使用します。",
    )

    if not has_api_key():
        st.sidebar.error("Gemini APIキーが未設定です。上の欄に入力するか、.env に GEMINI_API_KEY を設定してください。")

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
        st.error("Gemini APIキーが設定されていません。サイドバーの入力欄にAPIキーを入力するか、"
                  "プロジェクト直下の .env に GEMINI_API_KEY を設定してください。")
        return None

    try:
        result = st.write_stream(
            generate_stream(prompt, model, system_instruction=system_instruction, temperature=temperature)
        )
    except Exception as e:
        st.error(f"生成中にエラーが発生しました: {e}")
        return None

    return result
