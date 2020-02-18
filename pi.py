from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)
# app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # create one sample user to login
    manager.run()