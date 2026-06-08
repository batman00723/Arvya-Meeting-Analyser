import json
import hmac
import hashlib
from ninja_extra import api_controller, ControllerBase, http_post
from django.http import JsonResponse
from backend.config import settings


@api_controller("/zoom", tags=["Zoom"])
class ZoomWebhookController(ControllerBase):

    @http_post("/webhook")
    def webhook(self, request):

        body = json.loads(request.body)

        event = body.get("event")

        if event == "endpoint.url_validation":

            plain_token = body["payload"]["plainToken"]

            encrypted_token = hmac.new(
                settings.zoom_webhook_secret.get_secret_value(),
                plain_token.encode(),
                hashlib.sha256
            ).hexdigest()

            return JsonResponse({
                "plainToken": plain_token,
                "encryptedToken": encrypted_token
            })

        print(body)

        return {
            "status": "success"
        }