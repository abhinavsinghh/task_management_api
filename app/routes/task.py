from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from starlette import status
from app.schemas.task import TaskCreate
from app.models.task import Task
from app.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User
import json
from app.utils.redis_client import redis_client
from app.tasks import test_task, check_overdue_tasks



router = APIRouter()

@router.post('/tasks')
def create_task(task: TaskCreate, db: Session = Depends(get_db)
                #, current_user=Depends(get_current_user)
                ):
    new_task = Task(
        title = task.title,
        description = task.description,
        priority = task.priority,
        due_date = task.due_date,
        status = task.status,
        #user_id = current_user.id
    )

    db.add(new_task)
    db.commit()
    #redis_client.delete(
        #f"tasks_{current_user.id}"
    #)
    db.refresh(new_task)

    return new_task

@router.get("/tasks")
def get_tasks(
    status: str = None,
    priority: str = None,
    search: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_user)
):
    cache_key = "tasks"
    #cache_key = f"tasks_{current_user.id}"
    cached_tasks = redis_client.get(cache_key)
    if cached_tasks:
        return json.loads(cached_tasks)

    query = db.query(Task)#.filter(Task.user_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    tasks =  query.offset(skip).limit(limit).all()


    redis_client.setex(cache_key,
                       60,
                       json.dumps(
                           [
                               {
                               "id": task.id,
                               "title":task.title,
                               "description": task.description 
                                }
                           for task in tasks
                           ]
                       )
                    )
    return tasks

@router.get('/tasks/{task_id}')
def get_task(task_id:int, db: Session = Depends(get_db), #current_user=Depends(get_current_user)
             ):
    task = db.query(Task)#.filter(Task.id == task_id, Task.user_id == current_user.id).first()
    return task

@router.put('/tasks/{task_id}')
def update_task(
    task_id:int, task: TaskCreate, db: Session = Depends(get_db)
    #, current_user=Depends(get_current_user)
    ):
    db_task = db.query(Task).filter(
        Task.id == task_id
        #, Task.user_id == current_user.id
        ).first()

    if not db_task:
        return {'message': 'Task not found'}
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.due_date = task.due_date


    db.commit()
    redis_client.delete("tasks")
    #redis_client.delete(f"tasks_{current_user.id}")
    db.refresh(db_task)
    return db_task



@router.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)
                #, current_user=Depends(get_current_user)
                ):
    task = db.query(Task).filter(Task.id == task_id
                                 #, Task.user_id == current_user.id
                                 ).first()

    if not task:
        return {'message' : 'Task not found'}
    
    db.delete(task)
    db.commit()
    redis_client.delete("tasks")
    #redis_client.delete(
     #   f"tasks_{current_user.id}"
    #)

    return {'message' : 'Task Deleted'}

@router.get("/test-background")
def run_background_task():
    test_task.delay()
    return {"message": "Task queued"}




@router.get("/check_overdue")
def run_overdue_check():
    print("Endpoint hit")
    result = check_overdue_tasks.delay()
    print(result.id)
    return {"message" : {"Checking overdue tasks"}}
    




