from pydantic import BaseModel
from bson import ObjectId

class AuditResponse(BaseModel):
    transactionId: str
    workflowId: str
    userId: str
    clientId: str
    action: str
    prevValue: str
    currentValue: str
    createdDate: str
    modifiedDate: str

    class Config:
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'transactionId': '868add4b-42ae-4325-a583-efc13dd3e628',
                'workflowId': '6390e4e1c2c3b639b3e9b272',
                'userId': 'user2',
                'clientId': 'client1',
                'action': 'action5',
                'prevValue': 'abc',
                'currentValue': 'abcd',
                'createdDate': '01/06/2023',
                'modifiedDate': '01/06/2023',
            }
        }