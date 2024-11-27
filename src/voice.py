import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = ""

VOICE_CHARLIE = "IKne3meq5aSn9XLyUdCD"
VOICE_ADAM = "pNInz6obpgDQGcFmaJgB"

class Voice:
    def __init__(self):
        self.client = ElevenLabs(
            api_key=ELEVENLABS_API_KEY,
        )

    def text_to_speech_stream(self, text: str) -> IO[bytes]:
    # Perform the text-to-speech conversion
        response = self.client.text_to_speech.convert(
            voice_id=VOICE_CHARLIE,
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

        # Create a BytesIO object to hold the audio data in memory
        audio_stream = BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)

        # Return the stream for further use
        return audio_stream






