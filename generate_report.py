"""
Bag Intelligence Weekly Report Generator
毎週月曜日に自動実行 → reports/ に HTML を生成 → index.html を更新
"""

import anthropic
import json
import os
import re
from datetime import datetime, timezone, timedelta

# ── 設定 ──────────────────────────────────────────────
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")
TODAY_JP = datetime.now(JST).strftime("%Y年%-m月%-d日")
WEEKNUM = datetime.now(JST).strftime("VOL.%U")

OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Claude API 呼び出し（Web検索付き） ────────────────
client = anthropic.Anthropic()

SYSTEM_PROMPT = """
あなたはファッション・バッグ業界のプロアナリストです。
毎週月曜日に「BAG INTELLIGENCE」という週次トレンドレポートをHTML形式で生成します。

必ずWeb検索ツールを使って、直近1週間の最新情報を調査してから書いてください。
検索クエリ例：
- "luxury bag trends this week 2026"
- "Supreme new drop bags this week"
- "designer bag news hypebeast purseblog"
- "outdoor backpack new release 2026"

出力はHTMLのみ（```html ``` 不要）。<!DOCTYPE html>から始めてください。
日本語メインで、英語ブランド名はそのまま使用。
"""

USER_PROMPT = f"""
本日 {TODAY_JP} のBAG INTELLIGENCEウィークリーレポートを生成してください。

## 構成要件

### ページ全体
- タイトル：BAG INTELLIGENCE — {TODAY_JP}
- ナビ：LUXURY / STREET / BUSINESS / OUTDOOR の4カテゴリ
- スクロールティッカー（今週のキーワード）
- トップに「今週の総評」（300字程度）

### 各カテゴリ（それぞれ2〜3記事）
各記事カードに必ず含める：
- ブランド名
- 商品名・コレクション名
- コンセプト（イタリック）
- 説明文（100字）
- スペック表（コンセプト / サイズ / 素材 / 価格 / 原産国）
- 価格
- 「記事を読む →」ボタン + 実際のURL（Web検索で確認済みのもの）
- 出典元サイト名

### デザイン仕様（必ず守る）
- LUXURY：クリーム背景 #FAF8F4、ゴールド #9A7C3A、Playfair Display serif
- STREET：黒背景 #0F0F0F、ライムグリーン #B4F03C、DM Sans
- BUSINESS：ネイビー #1B2B4B、ブルー #2A5298、水色背景 #F5F7FB
- OUTDOOR：アースブラウン #3D2B1A、フォレストグリーン #2D5A27、生成り背景 #F4F1EC
- ヘッダー：シンプル sticky、Space Mono font
- フッター：シンプル

### 記事リンクについて
- Web検索で実際に存在を確認したURLのみ使用
- 見つからない場合はブランド公式サイト（例：supreme.com）を使用
- 絶対に架空URLを作らない

今日の日付は {TODAY}、{WEEKNUM} です。
"""

print(f"🔍 Generating report for {TODAY}...")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8000,
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
    ],
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": USER_PROMPT}]
)

# レスポンスからHTMLテキストを抽出
html_content = ""
for block in response.content:
    if block.type == "text":
        html_content += block.text

# ```html ``` が含まれていたら除去
html_content = re.sub(r'^```html\s*', '', html_content.strip())
html_content = re.sub(r'\s*```$', '', html_content.strip())

# ── ファイル保存 ──────────────────────────────────────
report_filename = f"{OUTPUT_DIR}/{TODAY}.html"
with open(report_filename, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"✅ Report saved: {report_filename}")

# ── index.html を更新（アーカイブ一覧） ──────────────
# 既存のレポート一覧を取得
existing_reports = sorted(
    [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".html") and f != "index.html"],
    reverse=True
)

archive_items = ""
for filename in existing_reports:
    date_str = filename.replace(".html", "")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        label = dt.strftime("%Y年%-m月%-d日（月）")
        vol = dt.strftime("VOL.%U")
    except Exception:
        label = date_str
        vol = ""
    
    is_latest = "★ 最新  " if filename == existing_reports[0] else ""
    archive_items += f"""
        <a href="reports/{filename}" class="report-card">
          <span class="report-badge">{is_latest}{vol}</span>
          <span class="report-date">{label}</span>
          <span class="report-arrow">→</span>
        </a>"""

index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BAG INTELLIGENCE — Archive</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Space+Mono:wght@400;700&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#111118; font-family:'Noto Sans JP',sans-serif; color:#fff; min-height:100vh; }}
.header {{ padding:48px 40px 32px; border-bottom:1px solid #222; }}
.header h1 {{ font-family:'Playfair Display',serif; font-size:clamp(32px,5vw,56px); font-weight:900; }}
.header h1 span {{ color:#C8A84B; }}
.header p {{ font-family:'Space Mono',monospace; font-size:10px; color:#555; letter-spacing:.2em; margin-top:8px; }}
.latest-btn {{
  display:inline-block; margin-top:24px;
  background:#C8A84B; color:#111; font-family:'Space Mono',monospace;
  font-size:11px; font-weight:700; letter-spacing:.15em;
  padding:12px 28px; text-decoration:none; transition:opacity .2s;
}}
.latest-btn:hover {{ opacity:.85; }}
.archive {{ padding:48px 40px; max-width:800px; }}
.archive h2 {{ font-family:'Space Mono',monospace; font-size:10px; color:#555; letter-spacing:.2em; margin-bottom:24px; }}
.report-card {{
  display:flex; align-items:center; gap:16px;
  padding:18px 0; border-bottom:1px solid #1e1e1e;
  text-decoration:none; color:#fff; transition:color .2s;
}}
.report-card:hover {{ color:#C8A84B; }}
.report-badge {{ font-family:'Space Mono',monospace; font-size:9px; color:#555; min-width:100px; }}
.report-date {{ font-size:14px; font-weight:400; flex:1; }}
.report-arrow {{ font-family:'Space Mono',monospace; color:#333; font-size:12px; }}
.report-card:hover .report-arrow {{ color:#C8A84B; }}
footer {{ padding:40px; font-family:'Space Mono',monospace; font-size:9px; color:#333; border-top:1px solid #1e1e1e; margin-top:40px; }}
</style>
</head>
<body>
<div class="header">
  <h1>BAG <span>INTELLIGENCE</span></h1>
  <p>WEEKLY BAG TREND REPORT — LUXURY / STREET / BUSINESS / OUTDOOR</p>
  {f'<a href="reports/{existing_reports[0]}" class="latest-btn">今週のレポートを読む →</a>' if existing_reports else ''}
</div>
<div class="archive">
  <h2>ARCHIVE — 全{len(existing_reports)}号</h2>
  {archive_items}
</div>
<footer>BAG INTELLIGENCE — Generated automatically every Monday · Powered by Claude + Anthropic API</footer>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"✅ index.html updated ({len(existing_reports)} reports in archive)")
print("🎉 Done!")
