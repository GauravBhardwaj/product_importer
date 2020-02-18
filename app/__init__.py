from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import routes, models
from flask import Blueprint
bp = Blueprint('api', __name__)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from redis import Redis
import rq

app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('product-importer-tasks', connection=app.redis)