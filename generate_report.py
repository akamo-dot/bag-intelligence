"""
Bag Intelligence Weekly Report Generator — 5カ国版（日本語UI）
毎週月曜日に自動実行 → reports/ に HTML を生成 → index.html を更新
"""

import anthropic
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

client = anthropic.Anthropic()

# ── 5カ国の設定 ────────────────────────────────────────
COUNTRIES = [
    {
        "id": "japan",
        "flag": "🇯🇵",
        "name": "日本",
        "queries": {
            "LUXURY":   "バッグ 新作 ラグジュアリー 2026",
            "STREET":   "ストリート バッグ 新作 ドロップ 2026",
            "BUSINESS": "ビジネスバッグ 新作 2026",
            "OUTDOOR":  "アウトドア バックパック 新作 2026",
            "SPECIAL":  "アニメ コスプレ キャラクター バッグ 新作 2026",
        },
    },
    {
        "id": "usa",
        "flag": "🇺🇸",
        "name": "アメリカ",
        "queries": {
            "LUXURY":   "luxury handbag new collection 2026",
            "STREET":   "streetwear bag new drop 2026 hypebeast",
            "BUSINESS": "business briefcase bag new release 2026",
            "OUTDOOR":  "outdoor backpack new release 2026",
            "SPECIAL":  "novelty cosplay anime convention bag USA 2026",
        },
    },
    {
        "id": "europe",
        "flag": "🇪🇺",
        "name": "ヨーロッパ",
        "queries": {
            "LUXURY":   "European luxury bag new 2026 fashion week",
            "STREET":   "European streetwear bag drop 2026",
            "BUSINESS": "European leather business bag new 2026",
            "OUTDOOR":  "European outdoor hiking bag new 2026",
            "SPECIAL":  "Europe art designer unusual novelty bag 2026",
        },
    },
    {
        "id": "korea",
        "flag": "🇰🇷",
        "name": "韓国",
        "queries": {
            "LUXURY":   "명품 가방 신상 2026",
            "STREET":   "스트리트 가방 신상 드롭 2026",
            "BUSINESS": "비즈니스 백 신상 2026",
            "OUTDOOR":  "아웃도어 백팩 신상 2026",
            "SPECIAL":  "캐릭터 가방 덕후 코스프레 신상 2026",
        },
    },
    {
        "id": "china",
        "flag": "🇨🇳",
        "name": "中国",
        "queries": {
            "LUXURY":   "奢侈品 包包 新款 2026",
            "STREET":   "潮流 包包 新品 2026",
            "BUSINESS": "商务包 新款 2026",
            "OUTDOOR":  "户外背包 新款 2026",
            "SPECIAL":  "动漫 二次元 周边 包包 新款 2026",
        },
    },
]

CAT_LABEL = {
    "LUXURY":   "ラグジュアリー",
    "STREET":   "ストリート",
    "BUSINESS": "ビジネス",
    "OUTDOOR":  "アウトドア",
    "SPECIAL":  "スペシャル",
}

# ── 各国セクションのHTML生成 ────────────────────────────
def generate_country_section(country):
    cid = country["id"]
    flag = country["flag"]
    name = country["name"]
    queries = country["queries"]

    search_list = "\n".join([
        f'- {CAT_LABEL[cat]}（{cat}）: "{q}"'
        for cat, q in queries.items()
    ])

    prompt = f"""
{flag} {name}のバッグトレンドレポートを生成してください。

## 手順
1. 以下の検索クエリでWeb検索を実行して最新情報を収集する
{search_list}

2. 各カテゴリ2〜3件の記事を選び、以下のHTML形式で出力する

## 出力ルール
- HTMLのみ出力（コードブロック不要、<!DOCTYPE>不要）
- 説明文はすべて日本語
- 画像URLは実際に存在するものだけ使用。不明な場合はimgタグを省略
- 記事URLは実際に存在するものだけ使用。不明な場合はブランド公式サイト
- 架空のURLは絶対に使わない
- SPECIALカテゴリはアニメ・コスプレ・キャラクター・ユニークなバッグを特集

## 出力HTML構造

<section class="category" id="{cid}-luxury">
  <h3 class="cat-title luxury-title">ラグジュアリー</h3>
  <div class="cards">
    <article class="card">
      <div class="card-img">
        <img src="[実際の画像URL]" alt="商品名" onerror="this.parentElement.classList.add('no-img');this.remove();">
      </div>
      <div class="card-body">
        <span class="brand">[ブランド名]</span>
        <h4 class="product">[商品名]</h4>
        <p class="concept"><em>[コンセプト1行]</em></p>
        <p class="desc">[説明文100字（日本語）]</p>
        <table class="specs">
          <tr><th>カテゴリ</th><td>[カテゴリ]</td></tr>
          <tr><th>サイズ</th><td>[サイズ]</td></tr>
          <tr><th>素材</th><td>[素材]</td></tr>
          <tr><th>価格</th><td>[価格]</td></tr>
          <tr><th>産地</th><td>[原産国]</td></tr>
        </table>
        <div class="card-footer">
          <span class="source">[出典サイト名]</span>
          <a href="[記事URL]" class="read-btn" target="_blank">記事を読む →</a>
        </div>
      </div>
    </article>
  </div>
</section>

<section class="category" id="{cid}-street">
  <h3 class="cat-title street-title">ストリート</h3>
  <div class="cards">
    <!-- 同様の記事カード × 2〜3 -->
  </div>
</section>

<section class="category" id="{cid}-business">
  <h3 class="cat-title business-title">ビジネス</h3>
  <div class="cards"><!-- 記事カード --></div>
</section>

<section class="category" id="{cid}-outdoor">
  <h3 class="cat-title outdoor-title">アウトドア</h3>
  <div class="cards"><!-- 記事カード --></div>
</section>

<section class="category" id="{cid}-special">
  <h3 class="cat-title special-title">スペシャル（アニメ・コスプレ・ユニーク）</h3>
  <div class="cards"><!-- 記事カード --></div>
</section>

今日の日付: {TODAY_JP}
"""

    print(f"  🔍 {flag} {name} を調査中...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    html = ""
    for block in response.content:
        if block.type == "text":
            html += block.text

    html = re.sub(r'^```html\s*', '', html.strip())
    html = re.sub(r'\s*```$', '', html.strip())
    return html


# ── 全国セクションを生成 ────────────────────────────────
print(f"🚀 BAG INTELLIGENCE 5カ国版 生成開始: {TODAY_JP}")

country_sections = {}
for country in COUNTRIES:
    country_sections[country["id"]] = generate_country_section(country)
    print(f"  ✅ {country['flag']} {country['name']} 完了")


# ── タブボタンとコンテンツを組み立て ──────────────────
tab_buttons = ""
tab_contents = ""

for i, country in enumerate(COUNTRIES):
    cid = country["id"]
    active_btn = "active" if i == 0 else ""
    active_pane = "active" if i == 0 else ""

    tab_buttons += f'''
      <button class="tab-btn {active_btn}" onclick="switchTab('{cid}')" id="btn-{cid}">
        <span class="tab-flag">{country["flag"]}</span>
        <span class="tab-name">{country["name"]}</span>
      </button>'''

    tab_contents += f'''
    <div class="tab-pane {active_pane}" id="pane-{cid}">
      <div class="country-header">
        <span class="country-flag-lg">{country["flag"]}</span>
        <h2 class="country-title">{country["name"]}のバッグトレンド</h2>
        <span class="country-date">{TODAY_JP} — {WEEKNUM}</span>
      </div>
      <div class="cat-nav">
        <a href="#{cid}-luxury">ラグジュアリー</a>
        <a href="#{cid}-street">ストリート</a>
        <a href="#{cid}-business">ビジネス</a>
        <a href="#{cid}-outdoor">アウトドア</a>
        <a href="#{cid}-special">スペシャル</a>
      </div>
      {country_sections[cid]}
    </div>'''


# ── 完全なHTMLを組み立て ────────────────────────────────
full_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BAG INTELLIGENCE — {TODAY_JP} {WEEKNUM}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Space+Mono:wght@400;700&family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{background:#0D0D12;color:#E8E4DC;font-family:'Noto Sans JP',sans-serif;min-height:100vh;}}

.site-header{{
  position:sticky;top:0;z-index:100;
  background:#0D0D12cc;backdrop-filter:blur(12px);
  border-bottom:1px solid #222;
  padding:16px 32px;
  display:flex;align-items:center;justify-content:space-between;
}}
.logo{{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;letter-spacing:.05em;}}
.logo span{{color:#C8A84B;}}
.logo-sub{{font-family:'Space Mono',monospace;font-size:9px;color:#555;letter-spacing:.2em;margin-top:2px;}}
.header-date{{font-family:'Space Mono',monospace;font-size:10px;color:#444;}}

.ticker{{
  background:#111116;border-top:1px solid #1e1e1e;border-bottom:1px solid #1e1e1e;
  padding:10px 0;overflow:hidden;white-space:nowrap;
  font-family:'Space Mono',monospace;font-size:10px;color:#444;letter-spacing:.15em;
}}
.ticker-inner{{display:inline-block;animation:ticker 40s linear infinite;}}
@keyframes ticker{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}

.tabs{{
  display:flex;gap:0;padding:0 32px;
  border-bottom:1px solid #1e1e1e;
  overflow-x:auto;background:#0D0D12;
}}
.tab-btn{{
  display:flex;align-items:center;gap:8px;
  padding:16px 28px;
  background:transparent;border:none;border-bottom:2px solid transparent;
  color:#555;font-family:'Noto Sans JP',sans-serif;font-size:13px;
  cursor:pointer;transition:all .2s;white-space:nowrap;
}}
.tab-btn:hover{{color:#aaa;}}
.tab-btn.active{{color:#C8A84B;border-bottom-color:#C8A84B;}}
.tab-flag{{font-size:20px;}}
.tab-name{{font-weight:500;}}

.tab-pane{{display:none;padding:40px 32px;max-width:1200px;margin:0 auto;}}
.tab-pane.active{{display:block;}}

.country-header{{
  display:flex;align-items:center;gap:16px;
  margin-bottom:28px;padding-bottom:24px;
  border-bottom:1px solid #222;
}}
.country-flag-lg{{font-size:44px;}}
.country-title{{font-family:'Playfair Display',serif;font-size:30px;font-weight:700;}}
.country-date{{font-family:'Space Mono',monospace;font-size:10px;color:#555;margin-left:auto;}}

.cat-nav{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:36px;}}
.cat-nav a{{
  padding:7px 18px;border:1px solid #2a2a2a;color:#666;
  font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.1em;
  text-decoration:none;transition:all .2s;
}}
.cat-nav a:hover{{border-color:#C8A84B;color:#C8A84B;}}

.category{{margin-bottom:60px;}}
.cat-title{{
  font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.2em;
  padding:10px 0;margin-bottom:24px;border-bottom:2px solid;
}}
.luxury-title{{color:#9A7C3A;border-color:#9A7C3A;}}
.street-title{{color:#B4F03C;border-color:#B4F03C;}}
.business-title{{color:#2A5298;border-color:#4A72B8;}}
.outdoor-title{{color:#5A9A4A;border-color:#5A9A4A;}}
.special-title{{color:#C850C0;border-color:#C850C0;}}

.cards{{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:20px;
}}

.card{{
  background:#131318;border:1px solid #1e1e1e;
  overflow:hidden;transition:transform .2s,border-color .2s;
}}
.card:hover{{transform:translateY(-3px);border-color:#333;}}
.card-img{{
  width:100%;height:220px;overflow:hidden;
  background:linear-gradient(135deg,#1a1a24,#2a2a34);
  display:flex;align-items:center;justify-content:center;
}}
.card-img img{{width:100%;height:100%;object-fit:cover;display:block;}}
.card-img.no-img::after{{
  content:'NO IMAGE';
  font-family:'Space Mono',monospace;font-size:9px;color:#333;letter-spacing:.2em;
}}
.card-body{{padding:20px;}}
.brand{{
  font-family:'Space Mono',monospace;font-size:9px;
  color:#555;letter-spacing:.15em;text-transform:uppercase;
}}
.product{{font-size:16px;font-weight:700;margin:6px 0 8px;line-height:1.4;}}
.concept{{font-size:12px;color:#888;margin-bottom:10px;font-style:italic;}}
.desc{{font-size:13px;color:#aaa;line-height:1.7;margin-bottom:16px;}}

.specs{{width:100%;border-collapse:collapse;font-size:11px;margin-bottom:16px;}}
.specs th{{
  width:28%;padding:5px 8px;
  background:#1a1a20;color:#555;
  font-family:'Noto Sans JP',sans-serif;font-weight:400;text-align:left;
}}
.specs td{{padding:5px 8px;color:#ccc;border-bottom:1px solid #1e1e1e;}}

.card-footer{{display:flex;align-items:center;justify-content:space-between;margin-top:8px;}}
.source{{font-family:'Space Mono',monospace;font-size:9px;color:#444;}}
.read-btn{{
  padding:7px 16px;background:transparent;border:1px solid #333;
  color:#888;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
  text-decoration:none;transition:all .2s;
}}
.read-btn:hover{{background:#C8A84B;border-color:#C8A84B;color:#111;}}

footer{{
  padding:32px;text-align:center;
  font-family:'Space Mono',monospace;font-size:9px;color:#333;
  border-top:1px solid #1e1e1e;margin-top:40px;
}}
</style>
</head>
<body>

<header class="site-header">
  <div>
    <div class="logo">BAG <span>INTELLIGENCE</span></div>
    <div class="logo-sub">週次グローバルバッグトレンドレポート</div>
  </div>
  <div class="header-date">{TODAY_JP} — {WEEKNUM}</div>
</header>

<div class="ticker">
  <span class="ticker-inner">
    ★ 今週のキーワード &nbsp;｜&nbsp; ラグジュアリー &nbsp;｜&nbsp; ストリート &nbsp;｜&nbsp; ビジネス &nbsp;｜&nbsp; アウトドア &nbsp;｜&nbsp; アニメ・コスプレ &nbsp;｜&nbsp; 🇯🇵 日本 &nbsp;｜&nbsp; 🇺🇸 アメリカ &nbsp;｜&nbsp; 🇪🇺 ヨーロッパ &nbsp;｜&nbsp; 🇰🇷 韓国 &nbsp;｜&nbsp; 🇨🇳 中国 &nbsp;｜&nbsp; ★ 今週のキーワード &nbsp;｜&nbsp; ラグジュアリー &nbsp;｜&nbsp; ストリート &nbsp;｜&nbsp; ビジネス &nbsp;｜&nbsp; アウトドア &nbsp;｜&nbsp; アニメ・コスプレ &nbsp;｜&nbsp; 🇯🇵 日本 &nbsp;｜&nbsp; 🇺🇸 アメリカ &nbsp;｜&nbsp; 🇪🇺 ヨーロッパ &nbsp;｜&nbsp; 🇰🇷 韓国 &nbsp;｜&nbsp; 🇨🇳 中国 &nbsp;｜&nbsp;
  </span>
</div>

<nav class="tabs">
  {tab_buttons}
</nav>

<main>
  {tab_contents}
</main>

<footer>
  BAG INTELLIGENCE — {TODAY_JP} {WEEKNUM}<br>
  毎週月曜日に自動生成 · Powered by Claude AI + Anthropic API + GitHub Actions
</footer>

<script>
function switchTab(id) {{
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('pane-' + id).classList.add('active');
  document.getElementById('btn-' + id).classList.add('active');
  window.scrollTo({{top: 0, behavior: 'smooth'}});
}}
</script>

</body>
</html>'''

# ── ファイル保存 ──────────────────────────────────────
report_filename = f"{OUTPUT_DIR}/{TODAY}.html"
with open(report_filename, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"✅ レポート保存: {report_filename}")

# ── index.html を更新 ──────────────────────────────────
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
    archive_items += f'''
        <a href="reports/{filename}" class="report-card">
          <span class="report-badge">{is_latest}{vol}</span>
          <span class="report-date">{label}</span>
          <span class="report-arrow">→</span>
        </a>'''

index_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BAG INTELLIGENCE — アーカイブ</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Space+Mono:wght@400;700&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#111118;font-family:'Noto Sans JP',sans-serif;color:#fff;min-height:100vh;}}
.header{{padding:48px 40px 32px;border-bottom:1px solid #222;}}
.header h1{{font-family:'Playfair Display',serif;font-size:clamp(32px,5vw,56px);font-weight:900;}}
.header h1 span{{color:#C8A84B;}}
.header p{{font-family:'Space Mono',monospace;font-size:10px;color:#555;letter-spacing:.2em;margin-top:8px;}}
.flags{{font-size:28px;margin-top:12px;letter-spacing:6px;}}
.latest-btn{{
  display:inline-block;margin-top:24px;
  background:#C8A84B;color:#111;font-family:'Space Mono',monospace;
  font-size:11px;font-weight:700;letter-spacing:.15em;
  padding:12px 28px;text-decoration:none;transition:opacity .2s;
}}
.latest-btn:hover{{opacity:.85;}}
.archive{{padding:48px 40px;max-width:800px;}}
.archive h2{{font-family:'Space Mono',monospace;font-size:10px;color:#555;letter-spacing:.2em;margin-bottom:24px;}}
.report-card{{
  display:flex;align-items:center;gap:16px;
  padding:18px 0;border-bottom:1px solid #1e1e1e;
  text-decoration:none;color:#fff;transition:color .2s;
}}
.report-card:hover{{color:#C8A84B;}}
.report-badge{{font-family:'Space Mono',monospace;font-size:9px;color:#555;min-width:100px;}}
.report-date{{font-size:14px;flex:1;}}
.report-arrow{{font-family:'Space Mono',monospace;color:#333;font-size:12px;}}
.report-card:hover .report-arrow{{color:#C8A84B;}}
footer{{padding:40px;font-family:'Space Mono',monospace;font-size:9px;color:#333;border-top:1px solid #1e1e1e;margin-top:40px;}}
</style>
</head>
<body>
<div class="header">
  <h1>BAG <span>INTELLIGENCE</span></h1>
  <p>週次グローバルバッグトレンドレポート — 日本・アメリカ・ヨーロッパ・韓国・中国</p>
  <div class="flags">🇯🇵🇺🇸🇪🇺🇰🇷🇨🇳</div>
  {f'<a href="reports/{existing_reports[0]}" class="latest-btn">今週のレポートを読む →</a>' if existing_reports else ''}
</div>
<div class="archive">
  <h2>アーカイブ — 全{len(existing_reports)}号</h2>
  {archive_items}
</div>
<footer>BAG INTELLIGENCE — 毎週月曜日に自動生成 · Powered by Claude AI + GitHub Actions</footer>
</body>
</html>'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"✅ index.html 更新完了（{len(existing_reports)}号）")
print("🎉 完了！")
