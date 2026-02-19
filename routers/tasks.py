from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, models, database, oauth2

router = APIRouter(
    prefix="/tasks",
    tags=['Task Operations']
)

# 1. GET TASKS (Pagination aur Search ke saath)
@router.get("/", response_model=List[schemas.TaskSchema])
def get_tasks(
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,  # Ek baar mein kitne tasks
    skip: int = 0,   # Kitne tasks chhodne hain
    search: Optional[str] = "" # Kya dhoondna hai
):
    # Query: Filter by Owner + Search + Pagination
    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).filter(
        models.Task.title.contains(search)
    ).limit(limit).offset(skip).all()
    
    return tasks

# 2. CREATE TASK
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskSchema, db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    # owner_id ko current_user se connect karna zaroori hai
    new_task = models.Task(owner_id=current_user.id, **task.dict(exclude={'id'}))
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 3. DELETE TASK
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id {id} not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    task_query.delete(synchronize_session=False)
    db.commit()
    return None

# 4. UPDATE TASK
@router.put("/{id}", response_model=schemas.TaskSchema)
def update_task(id: int, updated_task: schemas.TaskSchema, db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):

    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id {id} not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    task_query.update(updated_task.dict(exclude={'id'}), synchronize_session=False)
    db.commit()
    return task_query.first()