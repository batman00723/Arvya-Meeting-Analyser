from ninja_extra import api_controller, ControllerBase, http_post
from myapi.models import Recipent
from myapi.schema import CreateRecipentSchema


@api_controller("/recipients", tags=["Recipients"])
class RecipientController(ControllerBase):

    @http_post("/add")
    def add_recipient(
        self,
        request,
        payload: CreateRecipentSchema
    ):

        recipient, created = Recipent.objects.get_or_create(
            email=payload.email
        )

        return {
            "id": recipient.id,
            "email": recipient.email,
            "created": created
        }