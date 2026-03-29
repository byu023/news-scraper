# ニュース見出しスクレイパー

Googleニュースから日本語の最新見出しを取得して、CSVファイルに保存するツールです。

## 使い方

python3 file_test.py

## 実行結果

`news.csv` に最新のニュース見出しが保存されます。

## 使用技術

- Python 3
- requests
- BeautifulSoup4
- csv
# AI News Scraper

Google NewsのRSSから最新ニュースを取得し、Claude AIで要約してCSVに保存するツールです。

## 機能
- Google News RSSから最新5件の見出しを取得
- Claude APIで3行に要約
- 日時・見出し・要約をCSVに自動保存

## 使い方

### 1. インストール
```bash
pip install anthropic requests beautifulsoup4 lxml python-dotenv
```

### 2. APIキーの設定
`.env` ファイルを作成して以下を記述：
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 実行
```bash
python ai_news.py
```

## 使用技術
- Python
- Anthropic Claude API
- BeautifulSoup4
- Google News RSS
