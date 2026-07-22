# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal, single-user AI tool that drafts Japanese internal approval documents (稟議書) via Streamlit and the Gemini API. No database, no auth — everything is stateless per browser session (`st.session_state`). Japanese-language UI. This started as a multi-tool writing app and was deliberately narrowed to this single purpose — don't reintroduce a multipage/multi-feature structure unless asked.

## Commands

```powershell
pip install -r requirements.txt   # install deps
streamlit run app.py              # run the app (http://localhost:8501)
python -m py_compile app.py utils/*.py   # syntax-check all files
```

There are no automated tests or linters configured in this repo.

Requires a `.env` file (copy `.env.example`) with `GEMINI_API_KEY=...` set. Without it, the page loads fine but generation shows an in-app error (see `utils/gemini_client.has_api_key`).

## Architecture

**Single-page app — no `st.Page`/`st.navigation`, no `views/` directory.** `app.py` is the entire UI: page config → injected custom CSS (dark navy/gold themed background, glass-panel form, styled buttons — see the `CUSTOM_CSS` block) → `render_sidebar()` for the model picker → a hero header → the `st.form` collecting 稟議書 fields (件名, 目的・背景, 内容, 予算, 効果, スケジュール, 決裁者, 申請者) → on submit, build a plain-text prompt and call `run_generation` with a hardcoded `system_instruction` → store the result in `st.session_state["ringi_result"]` → an `elif` branch re-renders the last result on reruns where the form wasn't just submitted → a `st.download_button` offers the result as a `.txt` file.

**Two shared modules under `utils/`:**
- `utils/gemini_client.py` — owns the `google-genai` client (`@st.cache_resource`-cached singleton) and exposes `generate_stream(prompt, model, system_instruction, temperature)`, a generator yielding text chunks from `client.models.generate_content_stream`. Also has `has_api_key()`.
- `utils/ui.py` — `render_sidebar()` renders the model picker (see `MODELS` dict — currently `gemini-flash-latest` / `gemini-pro-latest`; several dated model IDs like `gemini-2.5-flash` have since been cut off for new API keys, so prefer the `-latest` aliases or verify availability via `client.models.list()` before hardcoding a dated id) and returns the selected model id. `run_generation(prompt, model, system_instruction, temperature)` is the standard way to trigger generation: it checks for the API key, pipes `generate_stream` through `st.write_stream` (so output streams live in the UI), and returns the final string (or `None` on missing key / error, after already rendering the error).

Temperature is fixed at 0.4 for this feature (precision task — the output is a formal business document, not creative writing).

## Styling

The dark/gold visual theme lives entirely in the `CUSTOM_CSS` string in `app.py`, injected via `st.markdown(..., unsafe_allow_html=True)`. It targets Streamlit's `data-testid` attributes (`stSidebar`, `stForm`, `stFormSubmitButton`, etc.), which can shift between Streamlit versions — if styling stops applying after a `streamlit` upgrade, check whether the targeted testids still exist. The theme is deliberately fixed (doesn't follow the user's OS light/dark preference); it forces its own dark palette site-wide.

## Notes

- A pre-specialization snapshot of the multi-tool version (blog/email/summarize/rewrite/titles/SNS/translate views) is kept in `_backup_before_ringi_specialization/` for reference — not part of the running app.
