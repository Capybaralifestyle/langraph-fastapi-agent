# task_manager


    Simple task manager API with:
    - GET /tasks - list all tasks
    - POST /tasks - create a task
    - GET /tasks/{id} - get specific task
    - PUT /tasks/{id} - update task
    - DELETE /tasks/{id} - delete task
    Each task has: id, title, description, completed (boolean)
    

## Setup and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Visit: http://localhost:8000/docs
