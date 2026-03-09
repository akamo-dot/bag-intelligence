import anthropic
import os
import time
from datetime import datetime, timezone, timedelta

# 設定
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

COUNTRIES = ["日本", "アメリカ", "ヨーロッパ", "韓国", "中国"]

print(f"🚀 レポート生成開始: {TODAY}")
results = []

for country in COUNTRIES:
    print(f"🔍 {country} をAIが分析中...")
    try:
        # ツールを使わず、AIの最新知識で一旦生成（エラー回避のため）
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            messages=[{"role": "user", "content": f"{country}の2026年最新バッグトレンドを予測・分析し、HTML形式で出力してください。"}]
        )
        results.append(response.content[0].text)
    except Exception as e:
        print(f"❌ {country} でエラー: {e}")
    
    print("⏳ 待機中（60秒）...")
    time.sleep(60) # 1分待機

# 保存処理
os.makedirs("reports", exist_ok=True)
with open(f"reports/{TODAY}.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body>{''.join(results)}</body></html>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body><h1>Archive</h1><a href='reports/{TODAY}.html'>{TODAY}号</a></body></html>")

print("✅ 完了しました")
