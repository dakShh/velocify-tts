from distutils.log import error
import mimetypes
from re import template

from elevenlabs import VoiceSettings
from app import app
from flask import render_template, request, send_file
from app.tts import syn


from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

import os
import io

load_dotenv()

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
        # outputs = syn.tts(text)
        # out = io.BytesIO()
        # syn.save_wav(outputs, out)
        # return send_file(out, mimetype="audio/wav")
        # Perform the text-to-speech conversion
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        print("Streaming audio data...")

        # Create a BytesIO object to hold audio data
        audio_stream = io.BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)
        return audio_stream


    else:
        return "Please enter text! :)", 400