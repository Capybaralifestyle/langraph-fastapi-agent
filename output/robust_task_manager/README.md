# robust_task_manager


    Task manager API with full CRUD operations:
    - Create, read, update, delete tasks
    - Each task has: id, title, description, completed status
    - Filter tasks by completion status
    - RESTful design with proper HTTP methods
    

## Features

- Task CRUD operations
- RESTful API design
- Automatic API documentation
- Input validation with Pydantic
- Error handling

## Setup and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Visit: http://localhost:8000/docs

## Available Endpoints

- `GET /` - Welcome message
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/status/completed` - Get completed tasks
- `GET /tasks/status/pending` - Get pending tasks