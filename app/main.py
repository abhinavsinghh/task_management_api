from fastapi import FastAPI, Depends    
from app.database import engine, get_db
from app.models.task import Task
from app.routes.task import router
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate


Task.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get('/')
def home():
    return {'message': 'Task Management API'}

@app.get('/hello')
def hello():
    return {'message' : 'Hello World'}

@router.get('/tasks')
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.get('/tasks/{task_id}')
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Task).filter(
        Task.id == task_id
    ).first()

@router.put('/tasks/{tasks_id}')
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status

    db.commit()
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    db.delete(task)
    db.commit()
    return {'message': 'Deleted!'}
