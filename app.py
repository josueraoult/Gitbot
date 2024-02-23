from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import List
import uvicorn
import httpx
import os

class WebhookRequestData(BaseModel):
    object: str = ""
    entry: List = []

def send_message(
    page_access_token: str,
    recipient_id: str,
    message_text: str,
    message_type: str = "UPDATE",
):
    r = httpx.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": page_access_token},
        headers={"Content-Type": "application/json"},
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": message_text},
            "messaging_type": message_type,
        },
    )
    r.raise_for_status()

app = FastAPI()

# Endpoints.
@app.get("/api/webhook")
async def verify(request: Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
        "hub.challenge"
    ):
        if (
            not request.query_params.get("hub.verify_token")
            == os.environ.get("2c361288a69c0c40ef760e2c4aa007f4")
        ):
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])

    return Response(content="Required arguments haven't passed.", status_code=400)

@app.post("/api/webhook")
async def webhook(data: WebhookRequestData):
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            for event in messaging_events:
                message = event.get("message")
                sender_id = event["sender"]["id"]

                send_message(
                    page_access_token=os.environ.get("EAAJ3opZCZBh4MBO4PQgzmxYllgslFvVXYsZApczTQWnfYAZCUXpAF1HZBiw7dZAovZBBCvAx9wCZB5J8AFq9Xtx2xCM4j2sQULYRFbUnt5Wdt9wbB6ajVA0SWs1y0sgtdE84L9tsMxv7WOmS2WoRTab4pSZBUgWSDv1hwg42BTfwLQsfbxGlmIZBwe6tPjN0R6FPqe"),
                    recipient_id=sender_id,
                    message_text=f"Received: {message['text']}",
                )

    return Response(content="ok")

def main():
    uvicorn.run(app=app)

if __name__ == "__main__":
    main()
