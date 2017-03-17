import re
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt, prompt_pass, Shell

from app import app, db
from apps.auth import models

# Configutation app
app.config.from_object('conf.config')

# flask-migrate instance
migrate = Migrate(app, db)
# flask-script instance
manager = Manager(app)


# shell context
def _make_context():
    return dict(app=app, db=db, models=models)


def _validuser():
    """
    Valid user data
    """
    username = prompt('Username')
    if not username:
        sys.exit('\nCould not create user: Username is obligatory')

    firstname = prompt('First name')
    if not firstname:
        sys.exit('\nCould not create user: First name is obligatory')

    lastname = prompt('Last name')
    if not lastname:
        sys.exit('\nCould not create user: Last name is obligatory')

    email = prompt('User E-Mail')
    if not email:
        sys.exit('\nCould not create user: E-Mail did not match')

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not EMAIL_REGEX.match(email):
        sys.exit('\nCould not create user: Invalid E-Mail addresss')

    password = prompt_pass('User password')
    password_confirm = prompt_pass('Confirmed password')
    if not password == password_confirm:
        sys.exit('\nCould not create user: Passwords did not match')

    return {
        'username': username,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'password': password,
    }


@manager.command
def createsuperuser():
    """
    Method for create super user
    """
    data = _validuser()
    user = models.User(
        username=data['username'],
        email=data['email'],
        first_name=data['firstname'],
        last_name=data['lastname'],
        password=data['password'],
        is_active=True,
        is_admin=True
    )

    db.session.add(user)
    db.session.commit()

    print("SuperUser created!")


@manager.command
def createuser():
    """
    Method for create user
    """
    data = _validuser()
    user = models.User(
        username=data['username'],
        email=data['email'],
        first_name=data['firstname'],
        last_name=data['lastname'],
        password=data['password'],
        is_active=True,
        is_admin=False
    )

    db.session.add(user)
    db.session.commit()

    print("User created!")


# Managers commands
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
