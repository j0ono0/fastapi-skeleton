# Admin functions
# Run via commandline: python -m database.admin <function name> <param1> <param2> <...etc>

import sys
import inspect
from sqlalchemy.orm import sessionmaker
from . import engine as db
from server.user.models import User


def upgrade_to_superuser(id):
    session = db.SessionLocal()
    user = session.query(User).filter(User.id == id).first()
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