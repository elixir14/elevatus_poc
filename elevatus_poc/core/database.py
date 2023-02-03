import motor.motor_asyncio


from elevatus_poc.core.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)

database = getattr(client, settings.DATABASE_NAME)

user_collection = database.get_collection("user_collection")
candidate_collection = database.get_collection("candidate_collection")
