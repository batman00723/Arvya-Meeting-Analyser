from ninja_extra import api_controller, ControllerBase, http_post

@api_controller("/zoom", tags=["Zoom"])
class ZoomWebhookController(ControllerBase):

    @http_post("/webhook")
    def webhook(self, request):

        print("ZOOM WEBHOOK RECEIVED")
        print(request.body)

        return {
            "status": "success"
        }