from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')

manager =Manager(app)
migrate = Migrate(app,db)

manager.add_command('server',server)
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Category=Category)

if __name__ == '__main__':
    manager.run()