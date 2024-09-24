from fastapi import APIRouter, HTTPException
from models import Task, UpdateTask

from database import create_task, delete_task, get_all_tasks, get_task_by_id, update_task


task = APIRouter()


@task.get('/api/tasks')
async def get_tasks():
    tasks = await get_all_tasks()
    return tasks


@task.get('/api/tasks/{id}', response_model=Task)
async def get_task(id: str):
    task = await get_task_by_id(id)
    if task:
        return task
    raise HTTPException(404, "Task not found")


@task.post('/api/tasks', response_model=Task)
async def save_task(task: Task):
    response = await create_task(task.model_dump())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@task.put('/api/tasks/{id}', response_model=Task)
async def put_task(id: str, data: UpdateTask):
    response = await update_task(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no task with the id {id}")


@task.delete('/api/tasks/{id}')
async def remove_task(id: str):
    response = await delete_task(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no task with the id {id}")