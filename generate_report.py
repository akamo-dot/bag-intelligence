import anthropic
import os
from datetime import datetime, timezone, timedelta

# 日本時間設定
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")

# キーの取得
key = os.environ.get("ANTHROPIC_API_KEY")

def run():
    if not key:
        print("❌ ANTHROPIC_API_KEY が見つかりません")
        return

    client = anthropic.Anthropic(api_key=key)
    print(f"🚀 生成開始: {TODAY}")

    try:
        # AIリクエスト
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": "2026年のバッグトレンドを3行で教えて"}]
        )
        report = message.content[0].text
        
        # 保存
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{TODAY}.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>{TODAY} Report</h1><p>{report}</p></body></html>")
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>Archive</h1><a href='reports/{TODAY}.html'>{TODAY}</a></body></html>")
            
        print("✅ 完了")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    run()
