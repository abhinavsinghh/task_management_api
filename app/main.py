from fastapi import FastAPI, Depends    
from app.database import engine, get_db
from app.models.task import Task
from app.routes.task import router
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate
from app.models.user import User
from app.routes.auth import router as auth_router


app = FastAPI()

app.include_router(router)


@app.get('/')
def home():
    return {'message': 'Task Management API'}


@app.get('/hello')
def hello():
    return {'message' : 'Hello World'}


@app.get('/tasks')
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get('/tasks/{task_id}')
def get_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.id == task_id).first()


@router.put('/tasks/{task_id}')
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        return {"error": "Task not found"}
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status

    db.commit()
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()
    return {'message': 'Deleted!'}


User.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)


app.include_router(auth_router)