import os
from typing import Iterator, Optional

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()


class RingiExtraction(BaseModel):
    subject: str
    background: str
    content: str
    budget: str
    effect: str
    schedule: str


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def resolve_api_key() -> Optional[str]:
    """サイドバーでユーザーが入力したAPIキー（セッション限定）があればそれを優先し、なければ.envの値を使う。"""
    session_key = st.session_state.get("gemini_api_key_override", "").strip()
    return session_key or os.getenv("GEMINI_API_KEY")


def has_api_key() -> bool:
    return bool(resolve_api_key())


def _client() -> genai.Client:
    api_key = resolve_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY が設定されていません。")
    return _get_client(api_key)


def generate_stream(
    prompt: str,
    model: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
) -> Iterator[str]:
    """Gemini APIにストリーミングでリクエストし、テキストチャンクを順次yieldする。"""
    client = _client()
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    stream = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text


def extract_from_quote_pdf(pdf_bytes: bytes, model: str) -> RingiExtraction:
    """見積書PDFの内容をGeminiの文書読解機能で読み取り、稟議書フォームの各項目を抽出する。"""
    client = _client()
    prompt = (
        "添付した見積書（PDF）の内容を読み取り、稟議書作成フォームに入力する項目を日本語で抽出してください。\n"
        "- subject: 稟議の件名（例:「〇〇の購入について」）\n"
        "- background: 目的・背景の下書き（見積内容から妥当と考えられる理由を簡潔に、断定しすぎない一般的な表現で）\n"
        "- content: 具体的な内容（発行元、品目・数量・単価などの要約）\n"
        "- budget: 費用・予算（税込/税抜が分かれば明記し、合計金額を記載）\n"
        "- effect: 期待される効果の下書き（簡潔に）\n"
        "- schedule: 実施時期・スケジュール（見積書に納期や有効期限の記載があればそれを使用。なければ空文字）\n"
        "見積書から読み取れない項目は無理に埋めず、空文字にしてください。"
    )
    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RingiExtraction,
            temperature=0.2,
        ),
    )
    if response.parsed is None:
        raise ValueError("見積書からの項目抽出に失敗しました。PDFの内容を確認してください。")
    return response.parsed
