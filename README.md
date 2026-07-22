# 稟議書作成アシスタント

Gemini APIを使った個人用の稟議書作成ツールです。Streamlit製で、データベース・認証機能はありません。

件名・目的・予算などを入力するだけで、社内提出用の稟議書の下書きを生成します。サイドバーから使用するモデル（Gemini Flash / Pro）を切り替えられます。

## セットアップ

### 1. 依存パッケージのインストール

```powershell
pip install -r requirements.txt
```

### 2. APIキーの設定

[Google AI Studio](https://aistudio.google.com/apikey) でGemini APIキーを取得し、
プロジェクト直下に `.env` ファイルを作成してください（`.env.example` をコピーして使えます）。

```
GEMINI_API_KEY=あなたのAPIキー
```

### 3. 起動

```powershell
streamlit run app.py
```

ブラウザが自動的に開きます（開かない場合は `http://localhost:8501` にアクセス）。

## ディレクトリ構成

```
app.py                 # エントリーポイント兼稟議書作成画面（カスタムCSSによるスタイリングを含む）
utils/
  gemini_client.py      # Gemini APIラッパー（ストリーミング生成）
  ui.py                 # サイドバー（モデル選択）・共通UI処理
requirements.txt
.env                     # 自分で作成（APIキー、Gitには含めない）
```
