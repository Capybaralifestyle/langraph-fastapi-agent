#!/usr/bin/env python3
"""
Robust FastAPI Code Generator with better error handling
"""

import os
import subprocess
from pathlib import Path
import re

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage


class RobustFastAPIGenerator:
    def __init__(self, model_name: str = "deepseek-r1:latest"):
        print(f"🤖 Initializing with {model_name}")
        self.llm = ChatOllama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.1,
        )
        print("✅ Generator ready!")

    def create_working_fastapi_app(self, requirements: str) -> str:
        """Create a guaranteed working FastAPI app"""
        # Use a simple template that we know works
        template = '''from fastapi import FastAPI, HTTPException
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
'''
        return template

    def enhance_with_llm(self, base_code: str, requirements: str) -> str:
        """Try to enhance the base code with LLM, but fall back to base if it fails"""
        prompt = f"""Take this working FastAPI code and enhance it based on these requirements: {requirements}

EXISTING CODE:
{base_code}

INSTRUCTIONS:
- Keep all existing functionality working
- Add any additional endpoints or features mentioned in requirements
- Maintain the same code structure and style
- Return ONLY the complete Python code
- Do not add explanations or markdown
- Ensure all syntax is valid Python

ENHANCED CODE:"""

        try:
            print("🔧 Enhancing with LLM...")
            response = self.llm.invoke([HumanMessage(content=prompt)])

            # Clean response
            enhanced_code = response.content.strip()

            # Remove thinking tags and markdown
            enhanced_code = re.sub(r'<think>.*?</think>', '', enhanced_code, flags=re.DOTALL)
            if enhanced_code.startswith("```python"):
                enhanced_code = enhanced_code[9:]
            elif enhanced_code.startswith("```"):
                enhanced_code = enhanced_code[3:]
            if enhanced_code.endswith("```"):
                enhanced_code = enhanced_code[:-3]

            enhanced_code = enhanced_code.strip()

            # Validate the enhanced code
            try:
                compile(enhanced_code, '<string>', 'exec')
                print("✅ Enhanced code is valid!")
                return enhanced_code
            except SyntaxError as e:
                print(f"⚠️  Enhanced code has syntax error: {e}")
                print("Using base template instead...")
                return base_code

        except Exception as e:
            print(f"⚠️  Enhancement failed: {e}")
            print("Using base template instead...")
            return base_code

    def create_project(self, requirements: str, project_name: str = "my_fastapi_app") -> str:
        """Create a complete FastAPI project"""
        print(f"🚀 Creating project: {project_name}")
        print(f"📝 Requirements: {requirements}")

        # Create project directory
        project_path = Path(f"output/{project_name}")
        project_path.mkdir(parents=True, exist_ok=True)

        # Start with working base code
        base_code = self.create_working_fastapi_app(requirements)

        # Try to enhance with LLM, but fall back to base if needed
        final_code = self.enhance_with_llm(base_code, requirements)

        # Write main.py
        with open(project_path / "main.py", "w") as f:
            f.write(final_code)
        print("✅ Created main.py")

        # Write requirements.txt
        requirements_txt = """fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.6
"""
        with open(project_path / "requirements.txt", "w") as f:
            f.write(requirements_txt)
        print("✅ Created requirements.txt")

        # Write README.md - FIXED VERSION
        readme_parts = [
            f"# {project_name}",
            "",
            requirements,
            "",
            "## Features",
            "",
            "- Task CRUD operations",
            "- RESTful API design",
            "- Automatic API documentation",
            "- Input validation with Pydantic",
            "- Error handling",
            "",
            "## Setup and Run",
            "",
            "```bash",
            "# Install dependencies",
            "pip install -r requirements.txt",
            "",
            "# Run the server",
            "uvicorn main:app --reload --host 0.0.0.0 --port 8000",
            "```",
            "",
            "## API Documentation",
            "",
            "Visit: http://localhost:8000/docs",
            "",
            "## Available Endpoints",
            "",
            "- `GET /` - Welcome message",
            "- `GET /tasks` - Get all tasks",
            "- `POST /tasks` - Create a new task",
            "- `GET /tasks/{task_id}` - Get specific task",
            "- `PUT /tasks/{task_id}` - Update task",
            "- `DELETE /tasks/{task_id}` - Delete task",
            "- `GET /tasks/status/completed` - Get completed tasks",
            "- `GET /tasks/status/pending` - Get pending tasks"
        ]
        readme_content = "\n".join(readme_parts)

        with open(project_path / "README.md", "w") as f:
            f.write(readme_content)
        print("✅ Created README.md")

        # Test the generated code
        self.test_project(project_path)

        return str(project_path)

    def test_project(self, project_path: Path):
        """Test if the generated code works"""
        print("🧪 Testing generated code...")

        try:
            # Test Python syntax
            with open(project_path / "main.py", "r") as f:
                code = f.read()

            # Try to compile the code
            compile(code, str(project_path / "main.py"), 'exec')
            print("✅ Python syntax is valid!")

            # Try to create virtual environment and test imports
            venv_path = project_path / "venv"
            subprocess.run([
                "python3", "-m", "venv", str(venv_path)
            ], check=True, cwd=project_path, capture_output=True)

            pip_path = venv_path / "bin" / "pip"
            subprocess.run([
                str(pip_path), "install", "-r", "requirements.txt"
            ], check=True, cwd=project_path, capture_output=True)

            python_path = venv_path / "bin" / "python"
            result = subprocess.run([
                str(python_path), "-c", "import main; print('✅ Import successful')"
            ], capture_output=True, text=True, cwd=project_path)

            if result.returncode == 0:
                print("✅ Code imports successfully!")
            else:
                print(f"⚠️  Import test failed: {result.stderr}")

        except SyntaxError as e:
            print(f"❌ Syntax error: {e}")
        except Exception as e:
            print(f"⚠️  Test error: {e}")


def main():
    generator = RobustFastAPIGenerator("qwen3:8b")

    requirements = """
    Task manager API with full CRUD operations:
    - Create, read, update, delete tasks
    - Each task has: id, title, description, completed status
    - Filter tasks by completion status
    - RESTful design with proper HTTP methods
    """

    project_path = generator.create_project(requirements, "robust_task_manager")
    print(f"\n🎉 Project created at: {project_path}")
    print(f"\n🏃 To run:")
    print(f"cd {project_path}")
    print(f"source venv/bin/activate")
    print(f"uvicorn main:app --reload")


if __name__ == "__main__":
    main()