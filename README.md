# FastAPI Skeleton
A useful jumpstart for fastapi projects. 
This skeleton setup is the result of working through the fastapi tutorial. In addition are some basic user and group models with api endpoints for common crud operations.

Project layout and some functionality is influenced by Django.

## Getting started
This setup uses SQLAlchemy and Alembic for database management. A basic 'user' submodule is included.


1. Clone this repository navigate into the root folder.
   Rename the following with your project title
    + root folder
    + 'name' in setup.py (see step 3)


2. Create a virtual environment `python3 -m venv .` - note the dot! - and activate it (window command show here) `. venv\Scripts\activate`


3. Install packages from requirements.txt or follow the following: 
   + Basic fastapi requirements `pip install fastapi uvicorn[standard]`
   + Database management `pip install async-exit-stack async-generator SQLAlchemy alembic`
   + User security/authentication `pip install email-validator python-multipart python-jose[cryptography] passlib[bcrypt]`
   + Serve static files `pip install aiofiles`
   + Install this project as a package too! `pip install -e .`
The '-e' installs in 'editable' mode and it's named from the 'name' variable in setup.py. 
Installing this package will allow the import references to work correctly

4. Initialize Alembic 
   + create files `alembic init alembic`
   + In alembic.ini update this line `sqlalchemy.url = sqlite:///data.db`


5. Create database (Assumes initial models are wanted!) - See section below on Alembic

## Start server for development:

1. Navigate to project root directory

2. Launch virtual environment: `. venv\Scripts\activate`

3. Start server `uvicorn server.main:app --reload`


## Create database migration with Alembic
Refer to the Alembic docs for more detailed options. Useful/common commands:
+ Auto generate migration: `alembic revision --autogenerate -m "<insert description here>"`
+ Execute migration: `alembic upgrade head`


## Testing
From the root directory run pytest with the command `pytest`. Nice intro on how to write tests is on the (fastapi website)[https://fastapi.tiangolo.com/tutorial/testing/]


## Make the initial superuser
By default users created via the API are not superusers, they can only be upgraded by another superuser. 

An existing user's authority can be upgraded via a python 'helper function'. 
To run the function from a commandline enable the virtual env and type the following from the project root directory:
`python -m database.admin upgrade_to_superuser <user.id>`