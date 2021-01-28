from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database.engine import Base

# Many-to-many association table
users_groups = Table('users_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    groups = relationship("Group", secondary=users_groups, backref="members")
    

class Group(Base):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True, index=True)
    name =  Column(String, unique=True, index=True)
