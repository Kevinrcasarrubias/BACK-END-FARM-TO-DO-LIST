from motor.motor_asyncio import AsyncIOMotorClient
from models import Task, UpdateTask
from bson import ObjectId
from decouple import config

print(config("MONGODB_URI"))
client = AsyncIOMotorClient(config("MONGODB_URI"))
database = client.taskdatabase
collection = database.tasks

async def get_task_by_id(id):
    task = await collection.find_one({"_id": ObjectId(id)})
    return task


async def get_task_by_title(title):
    task = await collection.find_one({'title': title})
    return task


async def get_all_tasks():
    tasks = []
    cursor = collection.find({})
    async for document in cursor:
        tasks.append(Task(**document))
    return tasks

async def create_task(task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({"_id": new_task.inserted_id})
    return created_task


async def update_task(id: str, data: UpdateTask):
    task = {k: v for k, v in data.model_dump().items() if v is not None}
    await collection.update_one({'_id': ObjectId(id)}, {'$set': task})
    document = await collection.find_one({'_id': ObjectId(id)})
    return document


async def delete_task(id: str):
    await collection.delete_one({'_id': ObjectId(id)})
    return True
