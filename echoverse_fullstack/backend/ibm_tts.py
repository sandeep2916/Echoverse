import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_tts_client():
    api_key = os.getenv("TTS_API_KEY", "")
    url = os.getenv("TTS_URL", "")
    if not api_key or not url:
        raise RuntimeError("Missing TTS credentials")
    auth = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=auth)
    tts.set_service_url(url)
    return tts

def synthesize_mp3_bytes(text: str, voice: str = None) -> bytes:
    tts = get_tts_client()
    voice = voice or os.getenv("TTS_VOICE", "en-US_AllisonV3Voice")
    response = tts.synthesize(
        text=text,
        voice=voice,
        accept="audio/mp3"
    ).get_result()
    return response.content