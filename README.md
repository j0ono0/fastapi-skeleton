# Development notes

## Getting started
This setup uses SQLAlchemy and Alembic for database stuff.

1. Clone this repository navigate into the root folder.
   Rename the following with your project title
    + root folder
    + 'name' in setup.py (see step 3)

2. Create a virtual environment `python3 -m venv .` and activate it (window command show here) `. venv\Scripts\activate`

3. Install packages `pip install fastapi uvicorn[standard] async-exit-stack async-generator SQLAlchemy alembic email-validator python-multipart python-jose[cryptography] passlib[bcrypt] aiofiles`. Install this project too so that the imports all function correctly `pip install -e .`. Note the '-e', that installs in 'editable' mode and it's named from the 'name' variable in setup.py.
   + python-multipart: OAuth2 uses form data
   + python-jose: JWT security tokens
   + passlib[bcrypt]: password hashing
   + aiofiles: required for fastapi to serve static files


4. Initialize Alembic 
   + create files `alembic init alembic`
   + In alembic.ini update this line `sqlalchemy.url = sqlite:///data.db`

5. Create database (Assumes initial models are wanted!)
   + Create a db migration `alembic revision --autogenerate -m "<insert description here>"`
   + Execute this migration `alembic upgrade head`


## Start server for development:

1. Navigate to project root directory

2. Launch virtual environment: `. venv\Scripts\activate`

3. Start server `uvicorn server.main:app --reload`


## Create database migration with Alembic
Refer to the Alembic docs for more detailed options. Useful/common commands:
+ Auto generate migration: `alembic revision --autogenerate -m "<insert description here>"`
+ Execute migration: `alembic upgrade head`

## Testing
From the root directory run pytest with the command `pytest`. Nice intro on how to write tests  on the (fastapi website)[https://fastapi.tiangolo.com/tutorial/testing/]

## Make the initial superuser
By default users created via the API are not superusers, they can only be upgraded by another superuser. 

An existing user's authority can be upgraded via a python 'helper function'. To run the function from a commandline enable the virtual env and type the following from the project root directory:
`python -m database.admin upgrade_to_superuser <user.id>`