"""
Stealth Interview Assistant backend (Final High-Accuracy Version)
----------------------------------------------------------------
- Start/Stop audio recording (mic or loopback)
- Transcribe speech using OpenAI Whisper (cloud)
- Generate concise AI interview answers (GPT-4o-mini)
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sounddevice as sd
import numpy as np
import tempfile, wave, os, threading, queue
from dotenv import load_dotenv
from openai import OpenAI

# ---------- CONFIG ----------
SAMPLE_RATE = 44100
DEVICE = None                     # None = default mic | "CABLE Output" for loopback
# ----------------------------

# ---- INIT ----
load_dotenv()
app = FastAPI(title="Stealth Interview Assistant API")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

recording_queue = queue.Queue()
recording_thread = None
is_recording = False


# ---------- AUDIO CAPTURE ----------
def record_stream(device=DEVICE):
    """Continuously capture audio until stopped."""
    global is_recording
    print(f"🎙️  Recording from: {device or 'default'}")
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="float32", device=device
        ) as stream:
            while is_recording:
                data, _ = stream.read(2048)
                recording_queue.put(data)
    except Exception as e:
        print(f"⚠️  Audio stream error: {e}")
    finally:
        print("🛑  Recording stopped.")


@app.get("/start")
def start_recording(mode: str = "mic"):
    """Start background recording."""
    global is_recording, recording_thread, recording_queue

    if is_recording:
        return {"status": "already recording"}

    device = None if mode == "mic" else "CABLE Output"
    recording_queue = queue.Queue()
    is_recording = True

    recording_thread = threading.Thread(
        target=record_stream, args=(device,), daemon=True
    )
    recording_thread.start()
    print("✅ Recording started.")
    return {"status": "recording started", "mode": mode}


# ---------- TRANSCRIPTION (OpenAI Whisper) ----------
def openai_transcribe(path):
    """Use OpenAI Whisper API for top-tier transcription accuracy."""
    with open(path, "rb") as f:
        resp = client.audio.transcriptions.create(model="whisper-1", file=f)
    return resp.text.strip()


@app.get("/stop")
def stop_recording():
    """Stop recording, transcribe audio, and return text."""
    global is_recording, recording_thread, recording_queue

    if not is_recording:
        return {"status": "not recording"}

    is_recording = False
    recording_thread.join(timeout=2.0)

    frames = []
    while not recording_queue.empty():
        frames.append(recording_queue.get())
    if not frames:
        return {"status": "no audio captured", "transcript": ""}

    # Combine & normalize
    audio = np.concatenate(frames, axis=0)
    audio = audio / np.max(np.abs(audio))  # normalize volume

    # Save to temp WAV
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_path = tmp.name
    with wave.open(tmp_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    tmp.close()

    # --- Transcribe with OpenAI Whisper ---
    print(f"🎧 Transcribing (OpenAI Whisper): {tmp_path}")
    try:
        transcript = openai_transcribe(tmp_path)
    except Exception as e:
        transcript = f"Transcription failed: {e}"
    finally:
        try:
            os.remove(tmp_path)
        except PermissionError:
            print("⚠️  Could not delete temp file (still in use).")

    print("✅ Transcription complete.")
    return JSONResponse({"status": "done", "transcript": transcript})


# ---------- AI RESPONSE (GPT-4o-mini) ----------
@app.post("/ai")
async def generate_ai_answer(request: Request):
    """Generate concise spoken interview answer."""
    data = await request.json()
    transcript = data.get("transcript", "")
    role = data.get("role", "data engineer")

    if not transcript.strip():
        return {"answer": "No transcript provided."}

    prompt = (
        f"You are coaching a {role} in a mock interview. "
        f"The interviewer said: '{transcript}'. "
        "Give a clear, confident 2–3 sentence spoken answer."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        answer = f"LLM call failed: {e}"

    return {"answer": answer}
