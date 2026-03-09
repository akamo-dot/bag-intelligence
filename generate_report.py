import anthropic
import os
import time
from datetime import datetime, timezone, timedelta

# 日本時間の設定
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")

# APIキーの確認
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ エラー: ANTHROPIC_API_KEY が設定されていません。")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)

print(f"🚀 レポート生成開始: {TODAY}")

# AIへのリクエスト（シンプル版）
try:
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        messages=[{"role": "user", "content": "日本、アメリカ、韓国の2026年バッグトレンドを詳しく分析して、日本語のHTML形式で出力してください。"}]
    )
    report_content = response.content[0].text
except Exception as e:
    print(f"❌ AIリクエスト失敗: {e}")
    exit(1)

# ファイルの保存
os.makedirs("reports", exist_ok=True)
with open(f"reports/{TODAY}.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body style='background:#111;color:#eee;padding:40px;'>{report_content}</body></html>")

# index.html の更新
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body style='background:#111;color:#fff;padding:50px;'><h1>Bag Intelligence Archive</h1><a href='reports/{TODAY}.html' style='color:#C8A84B;'>{TODAY}号のレポートはこちら</a></body></html>")

print("✅ すべての処理が完了しました。")
