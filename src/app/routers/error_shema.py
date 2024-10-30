from app.db.models import ORJSONModel


class Details(ORJSONModel):
    code: int
    message: str


class ErrorMessage(ORJSONModel):
    details: Details
