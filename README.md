# BAG INTELLIGENCE — 自動週次レポート

毎週月曜日に自動でバッグトレンドレポートを生成・公開するシステムです。

---

## セットアップ手順（約20分）

### Step 1 — GitHubアカウントを作る
https://github.com にアクセスして無料アカウントを作成

### Step 2 — このリポジトリを作る
1. GitHubにログイン後、右上の「+」→「New repository」
2. Repository name: `bag-intelligence`
3. Public を選択（GitHub Pagesを無料で使うため）
4. 「Create repository」をクリック

### Step 3 — ファイルをアップロード
1. 作成したリポジトリページで「uploading an existing file」をクリック
2. 以下の3ファイルをドラッグ＆ドロップ：
   - `generate_report.py`
   - `.github/workflows/weekly-report.yml`
   - `README.md`
3. 「Commit changes」をクリック

### Step 4 — Anthropic APIキーを設定
1. https://console.anthropic.com でAPIキーを発行（無料枠あり）
2. GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」
3. 「New repository secret」をクリック
4. Name: `ANTHROPIC_API_KEY`
5. Secret: 発行したAPIキーを貼り付け
6. 「Add secret」をクリック

### Step 5 — GitHub Pagesを有効化
1. リポジトリの「Settings」→「Pages」
2. Source: 「Deploy from a branch」
3. Branch: `main` / `/ (root)`
4. 「Save」をクリック

### Step 6 — 動作確認（手動実行）
1. リポジトリの「Actions」タブをクリック
2. 「Weekly Bag Intelligence Report」をクリック
3. 「Run workflow」→「Run workflow」をクリック
4. 数分後に完了 → `https://あなたのユーザー名.github.io/bag-intelligence/` にアクセス

---

## 自動実行スケジュール
毎週月曜日 日本時間 **午前9時** に自動実行

手動で今すぐ実行したい場合は Actions タブから「Run workflow」

---

## コスト目安
- GitHub: **無料**（パブリックリポジトリ）
- Anthropic API: 1回の生成あたり約 **$0.05〜0.15**（月4回で約**$0.5〜0.6**）

---

## ファイル構成
```
bag-intelligence/
├── index.html              ← アーカイブ一覧（自動生成）
├── reports/
│   ├── 2026-03-10.html     ← 週次レポート（自動生成）
│   ├── 2026-03-17.html
│   └── ...
├── generate_report.py      ← レポート生成スクリプト
├── .github/
│   └── workflows/
│       └── weekly-report.yml  ← 自動実行設定
└── README.md
```
