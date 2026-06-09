from ninja_extra import NinjaExtraAPI

from .meeting_agent import ChatOperationController
# from .zoom_webhook import ZoomWebhookController
from .audio_controller import AudioController

api_v1 = NinjaExtraAPI(version="1.0.0")

api_v1.register_controllers( ChatOperationController, AudioController)

