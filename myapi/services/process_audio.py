from myapi.services.transcription_service import transcribe_audio
from myapi.services.transcript_processor import process_transcript

def process_audio(file_path):
    print("Audio processing started")

    transcript = transcribe_audio(file_path)

    result = process_transcript(transcript)
    
    print("Audio Processed")

    return result