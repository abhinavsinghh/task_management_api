from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.task import TaskCreate
from app.models.task import Task
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter()

@router.post('/tasks')
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_task = Task(
        title = task.title,
        description = task.description,
        status = task.status,
        user_id = current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get('/tasks')
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Task).filter(Task.user_id == current_user.id).all()

@router.get('/tasks/{task_id}')
def get_task(task_id:int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    return task

@router.put('/tasks/{task_id}')
def update_task(
    task_id:int, task: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not db_task:
        return {'message': 'Task not found'}
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    return db_task



@router.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        return {'message' : 'Task not found'}
    
    db.delete(task)
    db.commit()

    return {'message' : 'Task Deleted'}
    




