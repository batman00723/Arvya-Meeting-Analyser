import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.settings"
)

django.setup()

from myapi.services.transcription_service import transcribe_audio
from myapi.services.transcript_processor import process_transcript

transcript = transcribe_audio(
    "recordings/test_meeting.m4a"
)

result= process_transcript(transcript= transcript)
print(transcript)
print(result)
