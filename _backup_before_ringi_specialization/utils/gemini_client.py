import os
from typing import Iterator, Optional

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


@st.cache_resource
def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY が設定されていません。")
    return genai.Client(api_key=api_key)


def has_api_key() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


def generate_stream(
    prompt: str,
    model: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
) -> Iterator[str]:
    """Gemini APIにストリーミングでリクエストし、テキストチャンクを順次yieldする。"""
    client = _get_client()
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
