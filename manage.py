#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import application, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
application = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

application.add_command("shell", Shell(make_context=make_shell_context))
application.add_command('db', MigrateCommand)


@application.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()


if __name__ == '__main__':
    application.run()
