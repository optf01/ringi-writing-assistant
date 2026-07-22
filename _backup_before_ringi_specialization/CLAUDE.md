# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal, single-user AI writing tool built with Streamlit and the Gemini API. No database, no auth — everything is stateless per browser session (`st.session_state`). Japanese-language UI.

## Commands

```powershell
pip install -r requirements.txt   # install deps
streamlit run app.py              # run the app (http://localhost:8501)
python -m py_compile app.py utils/*.py views/*.py   # syntax-check all files
```

There are no automated tests or linters configured in this repo.

Requires a `.env` file (copy `.env.example`) with `GEMINI_API_KEY=...` set. Without it, pages load fine but generation calls show an in-app error (see `utils/gemini_client.has_api_key`).

## Architecture

**Multipage routing via `st.Page`/`st.navigation`, not the `pages/` auto-discovery convention.** `app.py` is the sole entry point: it declares every page with `st.Page("views/<name>.py", title=..., icon=...)` and groups them into a nav sidebar via `st.navigation({...})`. To add a new tool, create `views/<name>.py` and register it in `app.py` — dropping a file in `views/` alone does nothing.

**Two shared modules under `utils/`, used by every view:**
- `utils/gemini_client.py` — owns the `google-genai` client (`@st.cache_resource`-cached singleton) and exposes `generate_stream(prompt, model, system_instruction, temperature)`, a generator yielding text chunks from `client.models.generate_content_stream`. Also has `has_api_key()`.
- `utils/ui.py` — `render_sidebar()` renders the model picker (Flash/Pro, see `MODELS` dict) and returns the selected model id; every view calls this first. `run_generation(prompt, model, system_instruction, temperature)` is the standard way views trigger generation: it checks for the API key, pipes `generate_stream` through `st.write_stream` (so output streams live in the UI), and returns the final string (or `None` on missing key / error, after already rendering the error).

**Per-view pattern (see any file in `views/` as a template):** each view is a standalone script run by Streamlit's page router — `model = render_sidebar()` → `st.form(...)` collects inputs → on submit, build a plain-text `prompt` from the form fields and a hardcoded `system_instruction` describing the persona/output format → `result = run_generation(...)` → store the result in `st.session_state["<feature>_result"]` → an `elif` branch re-renders the last result on reruns where the form wasn't just submitted → a `st.download_button` offers the stored result as a file. Keep this shape when adding or editing views rather than introducing a different state/flow pattern.

**Temperature is set per feature to match task type**: creative/generative tasks (blog, SNS, titles) use ~0.8–0.9; precision tasks (proofreading, translation, ringi documents, summarization) use ~0.3–0.4; email replies sit in between (~0.6).

## Adding a new writing tool

1. Create `views/<name>.py` following the per-view pattern above.
2. Register it as an `st.Page` in `app.py` and add it to the appropriate group in the `st.navigation({...})` dict (`文章を作る` / `文章を整える` / `その他`).
