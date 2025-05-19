from .config import client
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(client)
db = client.college
student_collection = db.get_collection("students")
