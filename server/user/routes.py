from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database.engine import get_db
from server.metadata import tags
from . import crud, schemas, models
from . import authentication as auth
from fastapi.security import OAuth2PasswordRequestForm

# NOTE: if prefix is changes ensure the 'oauth2_scheme' url, in authentication.py is updated 
user_router = APIRouter(prefix = "/user", tags=["users"])
groups_router = APIRouter( prefix = "/group", tags=["groups"])



###############################
# user 

@user_router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@user_router.get("/me", response_model=schemas.User)
async def read_user_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@user_router.get("/{user_id: int}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.put("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@user_router.patch("/", response_model=schemas.User, dependencies=[Depends(auth.can_edit_user)])
async def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_user = crud.update_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

###############################
# Authentication
    
@user_router.post("/token", response_model=auth.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # email used as unique user identification
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


###############################
# Group

@groups_router.get("/", response_model=List[schemas.GroupInDb], tags=["groups"])
async def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@groups_router.put("/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists with this name")
    return crud.create_group(db=db, group=group)

@groups_router.patch("/add", response_model=schemas.GroupInDb)
def add_user_to_group(groupuser: schemas.GroupUser, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=groupuser.group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail="Group does not exist.")
    db_user = crud.get_user(db, user_id=groupuser.user_id)
    if  not db_user:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return crud.group_add(db, db_group, db_user)

@groups_router.patch("/remove", response_model=schemas.GroupInDb)
def remove_user_from_group(groupuser: schemas.GroupUser, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=groupuser.group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail="Group does not exist.")
    # Remove a user
    db_user = crud.get_user(db, user_id=groupuser.user_id)
    if  not db_user:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return crud.group_remove(db, db_group, db_user)

@groups_router.patch("/rename", response_model=schemas.Group)
def rename_group(group: schemas.Group, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group.id)
    if not db_group:
        raise HTTPException(status_code=400, detail="Group does not exist.")
    db_group.name = group.name
    db.commit()
    return db_group
