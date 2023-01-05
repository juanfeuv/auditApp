import motor.motor_asyncio

def generateConection():
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    return client.local

