# backend/main.py
from dotenv import load_dotenv # <-- Add this
load_dotenv()                 # <-- Add this

from fastapi import FastAPI, WebSocket
from openai import OpenAI
import os


import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.websocket("/realtime")
async def realtime(ws: WebSocket):
    await ws.accept()
    
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1",
    }
    
    print(f"Incoming WebSocket connection. API Key present: {bool(OPENAI_API_KEY)}")
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is missing!")
        await ws.close(code=1008, reason="Missing API Key")
        return

    print(f"Connecting to OpenAI at {url}...")
    try:
        async with websockets.connect(url, additional_headers=headers) as openai_ws:
            print("Connected to OpenAI Realtime API!")
            # Initialize session
            session_update = {
                "type": "session.update",
                "session": {
                    "modalities": ["text"],
                    "input_audio_transcription": {
                        "model": "whisper-1"
                    }
                }
            }
            await openai_ws.send(json.dumps(session_update))

            async def receive_from_client():
                try:
                    while True:
                        data = await ws.receive_text()
                        # Expecting base64 audio from client
                        # Send to OpenAI
                        event = {
                            "type": "input_audio_buffer.append",
                            "audio": data
                        }
                        await openai_ws.send(json.dumps(event))
                except WebSocketDisconnect:
                    pass
                except Exception as e:
                    print(f"Client receive error: {e}")

            async def receive_from_openai():
                try:
                    async for message in openai_ws:
                        event = json.loads(message)
                        
                        # Real-time transcription events
                        if event["type"] == "conversation.item.input_audio_transcription.delta":
                            print(f"TRANSCRIPT DELTA: {event['delta']}")
                            await ws.send_json({
                                "type": "transcript",
                                "text": event["delta"]
                            })
                        elif event["type"] == "conversation.item.input_audio_transcription.completed":
                            print(f"TRANSCRIPT DONE: {event['transcript']}")
                            await ws.send_json({
                                "type": "transcript",
                                "text": "\n"
                            })
                        elif event["type"] == "error":
                            print(f"OpenAI Error: {event}")
                except Exception as e:
                    print(f"OpenAI receive error: {e}")

            await asyncio.gather(receive_from_client(), receive_from_openai())

    except websockets.exceptions.ConnectionClosed as e:
        print(f"OpenAI Connection Closed: {e.code} {e.reason}")
        await ws.close(code=1011, reason=f"OpenAI Closed: {e.code}")
    except Exception as e:
        print(f"Connection error: {e}")
        # Try to send the error to the client before closing
        try:
            await ws.close(code=1011, reason=f"Upstream Error: {str(e)[:100]}")
        except:
            pass

from pydantic import BaseModel

class AIRequest(BaseModel):
    transcript: str
    role: str
    screenshot: str = None

@app.post("/ai")
async def generate_ai_response(req: AIRequest):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        if req.screenshot:
            # Use vision model for screenshot analysis
            messages = [
                {
                    "role": "system",
                    "content": f"You are a {req.role}. When you see a coding problem in the screenshot, provide the SOLUTION CODE with a brief explanation. Do not just describe what you see - solve it! Be concise (3-5 sentences max)."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": req.transcript},
                        {"type": "image_url", "image_url": {"url": req.screenshot}}
                    ]
                }
            ]
            model = "gpt-4o"
        else:
            # Use text-only model
            messages = [
                {"role": "system", "content": f"You are an experienced {req.role} answering an interview question. Respond in FIRST PERSON as if YOU are the candidate. Be sharp, concise, and specific - give concrete technical steps you would take. Include specific tools/commands but keep it brief (4-6 sentences max). Sound confident and experienced, not verbose."},
                {"role": "user", "content": req.transcript}
            ]
            model = "gpt-4o"
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=600,
            temperature=0.7
        )
        
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        
        return {"answer": full_response}
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {"answer": f"Error: {str(e)}"}




