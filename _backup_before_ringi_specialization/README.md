# AI ライティングツール

Gemini APIを使った個人用のAIライティング支援ツールです。Streamlit製で、データベース・認証機能はありません。

## 機能

- 📝 ブログ記事作成
- ✉️ メール返信文生成
- 🏢 稟議書作成
- 📄 文章要約
- ✏️ リライト・校正
- 💡 タイトル・見出し生成
- 📱 SNS投稿文生成
- 🌐 翻訳

サイドバーから使用するモデル（Gemini 2.5 Flash / Pro）を切り替えられます。

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
app.py                 # エントリーポイント（ナビゲーション定義）
views/                 # 各機能のページ
  home.py
  blog.py
  email_reply.py
  ringi.py
  summarize.py
  rewrite.py
  titles.py
  sns.py
  translate.py
utils/
  gemini_client.py      # Gemini APIラッパー（ストリーミング生成）
  ui.py                 # サイドバー・共通UI処理
requirements.txt
.env                     # 自分で作成（APIキー、Gitには含めない）
```
