import csv
import io
import json
from random import choice
import time
import flask
from flask_login import logout_user
from flask_login import login_required
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

from app import app, db, models
from app.forms.login_form import LoginForm, ProductForm

from app.core.importer import push_csv_to_worker
from app.models import Product, User
from flask_sse import sse
from app.tasks.filler_tasks import get_or_create

ALLOWED_EXTENSIONS = set(['csv'])
import redis

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

red = redis.StrictRedis()

def get_red_events():
    pubsub = red.pubsub()
    pubsub.subscribe('jobs')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        data=message['data']
        data = "".join( chr(x) for x in bytearray(data))
        time.sleep(1)
        yield 'data: %s\n\n' % data


@app.route('/send')
def send_message():
    sse.publish({"message": "Hello!"}, type='rq-jobs')
    return flask.Response(get_red_events(),
                          mimetype="text/event-stream")

@app.route('/create-gb')
def createuser():
    # create app
    try:
        u1 = User(username='gb')
        u1.set_password('gb')
        db.session.add(u1)
        db.session.commit()
        return {"message": "Created"}
    except Exception:
        return {"message":"Failed"}

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('upload_file.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/upload', methods=['POST'])
def create_product():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file in request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        start_time = time.time()
        f = request.files['file']
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        push_csv_to_worker(current_user, csv_input)
        time_took = (time.time() - start_time)
        resp = jsonify({'message': 'File successfully queued for processing', 'time':str(time_took)})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@app.route('/drop-products', methods=['DELETE'])
def delete():

    try:
        rows = models.Product.query.delete()
        db.session.commit()
        return {rows:'deleted successfully'}
    except Exception:
        return {'failed'}


@app.route('/products', methods=['POST', 'GET'])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        kwargs = {'product_name':form.product_name.data,
                    'product_description':form.product_description.data,
                    'product_sku':form.product_sku.data,
                    'product_is_active':form.product_is_active.data
                  }
        get_or_create(db.session, kwargs)
        flash('Your product is now live!')
    list_products = Product.query.all()

    return render_template('products.html', title='Add/View/Update Products', form=form, products=list_products)
