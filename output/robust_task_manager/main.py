from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API",
    version="1.0.0"
)

# Data Models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: Optional[bool] = None

class Task(TaskBase):
    id: str
    completed: bool = False

# In-memory storage (replace with database in production)
tasks_db = {}

@app.get("/")
async def root():
    return {"message": "Welcome to Task Manager API", "docs": "/docs"}

@app.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    """Get all tasks"""
    return list(tasks_db.values())

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    """Create a new task"""
    task_id = str(uuid.uuid4())
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=False
    )
    tasks_db[task_id] = new_task
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a specific task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    stored_task = tasks_db[task_id]
    stored_task.title = task_update.title
    if task_update.description is not None:
        stored_task.description = task_update.description
    if task_update.completed is not None:
        stored_task.completed = task_update.completed

    return stored_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a specific task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}

@app.get("/tasks/status/completed", response_model=List[Task])
async def get_completed_tasks():
    """Get all completed tasks"""
    return [task for task in tasks_db.values() if task.completed]

@app.get("/tasks/status/pending", response_model=List[Task])
async def get_pending_tasks():
    """Get all pending tasks"""
    return [task for task in tasks_db.values() if not task.completed]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)