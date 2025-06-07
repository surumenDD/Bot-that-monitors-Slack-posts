# main.py  --- Bolt × FastAPI 最小構成
from dotenv import load_dotenv
load_dotenv()                                      # .env 読み込み

import os
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler  # fastapi アダプタ
from fastapi import FastAPI, Request

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

# イベントハンドラ : @メンションを受け取る
@app.event("app_mention")
def handle_mention(body, say, logger):
    logger.info(f"[app_mention] payload={body}")
    user = body["event"]["user"]
    say(f"<@{user}> こんにちは！ :wave:")

# 追加で「すべての events」を拾うデバッグ用ハンドラ
@app.middleware  # ← Bolt のすべてのリクエストを横取り
def log_request(logger, body, next):
    logger.info(f"[ANY EVENT] {body}")
    return next()

# FastAPI 側
fastapi_app = FastAPI()
handler = SlackRequestHandler(app)

@fastapi_app.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, reload=True)
