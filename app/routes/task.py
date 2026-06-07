from fastapi import APIRouter 
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette import status

from app.schemas.task import TaskCreate
from app.models.task import Task
from app.database import get_db

router = APIRouter()

@router.post('/tasks')
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title = task.title,
        description = task.description,
        status = task.status
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

