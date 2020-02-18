from flask import current_app

from app import app, db, login
import redis
import rq
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Product(db.Model):
    # product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    product_sku = db.Column(db.String(256),primary_key=True)
    product_is_active = db.Column(db.Boolean(), nullable=False)
    product_description = db.Column(db.Text, index=True)

    def __repr__(self):
        return '<User {}>'.format(self.product_name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def launch_task(self, name, description, dict_of_data):
        rq_job = current_app.task_queue.enqueue('app.tasks.filler_tasks.fill_product',
                                                dict_of_data)

        task = Task(id=rq_job.get_id(), name=name, description=description,
                    user=self, task_data=dict_of_data)
        # g.tasks.append(rq_job)


        db.session.add(task)
        # return task, rq_job

    # def get_tasks_in_progress(self):
    #     return Task.query.filter_by(user=self, complete=False).all()
    #
    # def get_task_in_progress(self, name):
    #     return Task.query.filter_by(name=name, user=self,
    #                                 complete=False).first()


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)
    task_data = db.Column(db.JSON())

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100