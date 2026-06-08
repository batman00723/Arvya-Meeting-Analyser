from ninja_extra import api_controller, ControllerBase, http_post
from ninja import File
from ninja.files import UploadedFile

from myapi.services.process_audio import process_audio

@api_controller("/audio", tags= ['Audio to Report'])
class AudioController(ControllerBase):
    @http_post("/analyse")
    def analyse_audio(self, request, audio_file: UploadedFile= File(...)):
        print("Agent Started")
        
        file_path= f"recordings/{audio_file.name}"

        with open(file_path, "wb+") as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        result = process_audio(file_path= file_path)

        return {
            "status": "success",
            "analysis": result
        }
