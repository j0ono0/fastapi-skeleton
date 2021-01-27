# Admin functions
# Run via commandline: python -m sql_app.admin <function name> <param1> <param2> <...etc>

import sys
import inspect
from sqlalchemy.orm import sessionmaker
from . import database as db
from . import models


def upgrade_to_superuser(id):
    session = db.SessionLocal()
    user = session.query(models.User).filter(models.User.id == id).first()
    try:
        user.is_superuser = True
        session.commit()
        print(f'{user.email}: Upgraded to superuser.')
    except AttributeError as e:
        print('No user exists with that id.', e)
    session.close()


if __name__ == '__main__':
    fn = locals()[sys.argv[1]]
    params = sys.argv[2:]
    fn(*params)