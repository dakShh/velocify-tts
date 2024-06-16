import os
from os.path import join, dirname
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import site
location = site.getsitepackages()[0]

# path = location+"/TTS/.models.json"
path = "C:/Users/asus/anaconda3/envs/texttospeech/Lib/site-packages/TTS/.models.json"

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
print("ELEVENLABS_API_KEY: ",ELEVENLABS_API_KEY)
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

