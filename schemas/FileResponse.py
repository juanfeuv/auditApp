from pydantic import BaseModel
from bson import ObjectId

class FileResponse(BaseModel):
    message: str

    class Config:
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "message": "audit_data.csv uploaded!",
            }
        }