from app.celery_worker import celery_app
from app.database import sessionlocal
from app.models.task import Task
from datetime import datetime
from app.models.user import User

@celery_app.task
def test_task():
    print("Background task executed")

    return "Success"

@celery_app.task
def check_overdue_tasks():
    print("Task started")
    print(Task.__dict__)

    db = sessionlocal()

    #overdue_tasks = db.query(Task).filter(
     #   Task.due_date < datetime.utcnow()
    #).all()
    overdue_tasks = db.query(Task).all()


    for task in overdue_tasks:
        print(f"Task {task.id}:{task.title} is overdue.")

    db.close()