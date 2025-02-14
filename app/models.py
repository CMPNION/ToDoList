from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from database import Base


# Define the User and Todo models
# The User model has an id, username, password, and todos field.
# The id field is the primary key, username is a unique string, password is a string, and todos is a relationship to the Todo model.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    todos = relationship("Todo", back_populates="owner")

# The Todo model has an id, task, completed, and owner_id field.
# The id field is the primary key, task is a string, completed is a boolean with a default value of False, and owner_id is a foreign key to the User model.
# The owner field is a relationship to the User model.
# The back_populates parameter is used to define the relationship between the User and Todo models.
# This allows us to access the todos of a user and the owner of a todo.
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")
