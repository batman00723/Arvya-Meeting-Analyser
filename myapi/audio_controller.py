from ninja_extra import api_controller, ControllerBase, http_post
from ninja import File
from ninja.files import UploadedFile
import os
import uuid
from myapi.services.process_audio import process_audio

@api_controller("/audio", tags= ['Audio → Report'])
class AudioController(ControllerBase):
    @http_post("/analyse")
    def analyse_audio(self, request, audio_file: UploadedFile= File(...)):
        print("Agent Started")

        os.makedirs("recordings", exist_ok=True)  
        file_path = f"recordings/{uuid.uuid4()}_{audio_file.name}"
        
        try:

            with open(file_path, "wb+") as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            result = process_audio(file_path)

            return {
                "status": "success",
                "analysis": result
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
