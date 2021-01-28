from sqlalchemy.orm import Session
from . import authentication as auth
from . import models, schemas


###############################
# User

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = get_user(db, user.id)
    if db_user:
        update_data = user.dict(exclude_unset=True)
        # Transfer data to model instance
        for key, val in update_data.items():
            setattr(db_user, key, val)
        # Commit and return instance
        db.commit()
    return db_user
        

###############################
# Group

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def get_group(db: Session, group_id: str):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def group_add(db: Session, group: schemas.Group, user: schemas.User):
    db_group = db.query(models.Group).filter(models.Group.id == group.id).first()
    db_group.members.append(user)
    db.commit()
    return db_group

def group_remove(db: Session, group: schemas.Group, user: schemas.User):
    db_group = db.query(models.Group).filter(models.Group.id == group.id).first()
    db_group.members.remove(user)
    db.commit()
    return db_group