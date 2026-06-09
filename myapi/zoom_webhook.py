# This zoom webhook is not used as I need zoom pro for access for zoom cloud so im switching to zoom local free tier.

import json
import hmac
import hashlib

from ninja_extra import api_controller, ControllerBase, http_post
from django.http import JsonResponse
from backend.config import settings

from myapi.services.transcript_processor import process_transcript


@api_controller("/zoom", tags=["Zoom"])
class ZoomWebhookController(ControllerBase):

    @http_post("/webhook")
    def webhook(self, request):

        body = json.loads(request.body)

        event = body.get("event")

        print("=" * 50)
        print(f"EVENT: {event}")
        print(json.dumps(body, indent=2))
        print("=" * 50)

        if event == "endpoint.url_validation":

            plain_token = body["payload"]["plainToken"]

            encrypted_token = hmac.new(
                settings.zoom_webhook_secret.get_secret_value().encode(),
                plain_token.encode(),
                hashlib.sha256
            ).hexdigest()

            return JsonResponse({
                "plainToken": plain_token,
                "encryptedToken": encrypted_token
            })
        
        elif event == "recording.completed":
            print("RECORDING COMPLETED")

        elif event == "recording.transcript_completed":
            print("TRANSCRIPT COMPLETED")
            transcript = """
                Investment Banker: Thank you for joining.

                Client: We are considering an acquisition of a healthcare company.

                Investment Banker: We estimate valuation between $50M and $70M.

                Client: What are the key risks?

                Investment Banker: Regulatory approval and integration execution.
                """

            result = process_transcript(transcript)

            print(result)


        return {
            "status": "success"
        }