import os
import io
from distutils.log import error
import mimetypes
from re import template

from app import app
from flask import render_template, request, send_file
from app.tts import syn

from dotenv import load_dotenv
load_dotenv()

from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/call/project1", methods = ["POST"])
def call_project1(): 
    if (request.form['text']):
        text = request.form['text']
        outputs = syn.tts(text)
        out = io.BytesIO()
        syn.save_wav(outputs, out)
        return send_file(out, mimetype="audio/wav")
    else:
        return "Please enter text! :)", 400
    

@app.route("/call/voicify", methods = ["POST"])
def call_voicify(): 
    if (request.form['text']):
        text = request.form['text']

        audio = client.generate(
            text=text,
            model="eleven_multilingual_v2",
            voice=Voice(
                voice_id='yHx9q5iHmtVGKONrqrIf', #dez - american
                settings=VoiceSettings(stability=0.40, similarity_boost=0.45, style=0.0, use_speaker_boost=True)
            )
        )

        audio_stream = io.BytesIO()

        for chunk in audio:
            if chunk:
                audio_stream.write(chunk)

        audio_stream.seek(0)
        return send_file(audio_stream, mimetype="audio/wav")

    else:
        return "Please enter text! :)", 400