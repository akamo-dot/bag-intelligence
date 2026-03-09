import anthropic
import os
import re
import time
from datetime import datetime, timezone, timedelta

# --- 基本設定 ---
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")
TODAY_JP = datetime.now(JST).strftime("%Y年%m月%d日")
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

COUNTRIES = [
    {"id": "japan", "flag": "🇯🇵", "name": "日本", "queries": "バッグ 新作 ラグジュアリー 2026"},
    {"id": "usa", "flag": "🇺🇸", "name": "アメリカ", "queries": "luxury handbag new collection 2026"},
    {"id": "europe", "flag": "🇪🇺", "name": "ヨーロッパ", "queries": "European luxury bag new 2026"},
    {"id": "korea", "flag": "🇰🇷", "name": "韓国", "queries": "명품 가방 신상 2026"},
    {"id": "china", "flag": "🇨🇳", "name": "中国", "queries": "奢侈品 包包 新款 2026"},
]

def generate_section(country):
    print(f"🔍 {country['flag']} {country['name']} を調査中...")
    prompt = f"{country['flag']} {country['name']}の最新バッグトレンドを検索し、HTML形式のレポートを作成してください。説明は日本語でお願いします。今日の日付は{TODAY_JP}です。"
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}], # ツール名は最新のものに準拠
            messages=[{"role": "user", "content": prompt}]
        )
        # テキストブロックを抽出
        html_content = "".join([block.text for block in response.content if hasattr(block, 'text')])
        # マークダウンのコードブロックを削除
        return re.sub(r"```html|```", "", html_content).strip()
    except Exception as e:
        print(f"❌ エラー発生 ({country['name']}): {e}")
        return f"<p>{country['name']}のデータ取得に失敗しました。</p>"

# --- メイン処理 ---
print(f"🚀 レポート生成開始: {TODAY_JP}")
results = []
for i, country in enumerate(COUNTRIES):
    results.append(generate_section(country))
    if i < len(COUNTRIES) - 1:
        print("⏳ レート制限回避のため150秒待機します...")
        time.sleep(150)

# HTML組み立て
full_html = f"<html><body style='background:#111; color:#eee; font-family:sans-serif; padding:40px;'><h1>Weekly Bag Intelligence - {TODAY_JP}</h1>{''.join(results)}</body></html>"

# 保存
with open(f"{OUTPUT_DIR}/{TODAY}.html", "w", encoding="utf-8") as f:
    f.write(full_html)

# インデックス更新
reports = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".html")], reverse=True)
index_html = "<html><body style='background:#111; color:#fff; padding:50px;'><h1>Archive</h1>" + "".join([f"<a href='reports/{r}' style='color:#C8A84B; display:block; margin:10px 0;'>{r}</a>" for r in reports]) + "</body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ すべての処理が完了しました！")
